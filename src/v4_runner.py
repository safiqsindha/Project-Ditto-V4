"""
v4 evaluation runner.

Wraps v3's batch runner for the single-cell v4 configuration:
  - Source: "pokemon" (v1 Pokémon Showdown chains)
  - Model: Claude Haiku 4.5 only
  - Chains: loaded from data/v1_chains_mirror/, filtered to v4_chain_selection.json
  - Shuffled chains: generated on-the-fly using v3's shuffler (seeds 42, 1337, 7919)
  - Output: results/raw/phase1/{config}/pokemon/ (real) + shuffled counterparts

v3 code is NOT modified. This script imports v3's batch infrastructure via
sys.path and patches module-level constants as needed.

Usage
-----
  # Dry run (count calls, preview first prompt):
  python -m src.v4_runner --dry-run

  # Pilot (50 chains, primary config only):
  python -m src.v4_runner --batch --n 50 --config primary --out results/raw/pilot

  # Full evaluation (1200 chains, all 3 configs):
  python -m src.v4_runner --batch --out results/raw/phase1
"""

from __future__ import annotations

import json
import pathlib
import sys
import time
from pathlib import Path

from dotenv import load_dotenv, dotenv_values

# ---------------------------------------------------------------------------
# Vendor path setup — load v3 modules by path to avoid src namespace conflict
# ---------------------------------------------------------------------------

import importlib.util  # noqa: E402

_V3_SRC = pathlib.Path(__file__).parent.parent / "vendor" / "v3" / "src"


def _load_v3(name: str):
    key = f"src.{name}"
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, _V3_SRC / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod


import anthropic  # noqa: E402

# Load v3 modules in dependency order (each must be in sys.modules before
# any module that imports it is exec'd).
_v3_normalize = _load_v3("normalize")
_v3_prompt = _load_v3("prompt_builder")
_v3_runner = _load_v3("runner")

PROMPT_VERSION = _v3_prompt.PROMPT_VERSION
SYSTEM_PROMPT = _v3_prompt.SYSTEM_PROMPT
build_prompt = _v3_prompt.build_prompt
cutoff_rendered = _v3_prompt.cutoff_rendered

# ---------------------------------------------------------------------------
# v4 constants
# ---------------------------------------------------------------------------

SOURCE = "pokemon"
MODEL_NAME = "haiku"
MODEL_ID = "claude-haiku-4-5-20251001"

# Full evaluation matrix (matches SPEC.md §Models and Evaluation Parameters)
EVAL_CONFIGS: list[dict] = [
    {"temperature": 0.0, "seed": 42,   "label": "primary"},
    {"temperature": 0.5, "seed": 1337, "label": "variance1"},
    {"temperature": 0.5, "seed": 7919, "label": "variance2"},
]
SHUFFLE_SEEDS: list[int] = [42, 1337, 7919]

_BATCH_POLL_INTERVAL = 60
_BATCH_TERMINAL_STATUSES = frozenset({"ended", "canceled", "expired", "failed"})
_MAX_BATCH_SIZE = 10_000
_CUSTOM_ID_SEP = "-"


# ---------------------------------------------------------------------------
# Chain loading
# ---------------------------------------------------------------------------

def load_selected_chains(
    chains_dir: Path,
    selection_path: Path,
    n: int | None = None,
) -> list[dict]:
    """Load the pre-registered chain selection from the v1 mirror."""
    with open(selection_path) as f:
        sel = json.load(f)
    chain_ids = sel["chain_ids"]
    if n is not None:
        chain_ids = chain_ids[:n]

    chains = []
    for cid in chain_ids:
        p = chains_dir / f"{cid}.jsonl"
        if not p.exists():
            print(f"[v4_runner] WARN: missing chain {cid}")
            continue
        with open(p) as f:
            chains.append(json.loads(f.readline().strip()))
    return chains


# ---------------------------------------------------------------------------
# Prompt building (reuses v3's logic exactly)
# ---------------------------------------------------------------------------

def _build_prompt_for_chain(chain: dict) -> tuple[str, int]:
    """Return (user_message, cutoff_k). Mirrors v3's _build_user_message."""
    rendered: str = chain["rendered"]
    import re
    total_steps = len(re.findall(r"Step \d+", rendered))
    cutoff_k = chain.get("cutoff_k") or max(1, total_steps // 2)
    truncated = cutoff_rendered(rendered, cutoff_k)
    return build_prompt(truncated, cutoff_k), cutoff_k


# ---------------------------------------------------------------------------
# Result saving (mirrors v3's _save_results)
# ---------------------------------------------------------------------------

def _save_result(
    chain_id: str,
    cutoff_k: int,
    temperature: float,
    seed: int,
    response_text: str,
    output_dir: Path,
    config_label: str,
) -> None:
    result = {
        "chain_id": chain_id,
        "model": MODEL_NAME,
        "seed": seed,
        "source": SOURCE,
        "cutoff_k": cutoff_k,
        "response": response_text,
        "prompt_version": PROMPT_VERSION,
        "temperature": temperature,
    }
    out = output_dir / config_label / SOURCE
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{MODEL_NAME}_{seed}_{chain_id}_T{temperature}.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)


# ---------------------------------------------------------------------------
# Batch runner
# ---------------------------------------------------------------------------

def _make_custom_id(seed: int, chain_id: str) -> str:
    return f"{MODEL_NAME}{_CUSTOM_ID_SEP}{seed}{_CUSTOM_ID_SEP}{chain_id}"


def run_batch(
    real_chains: list[dict],
    output_dir: Path,
    configs: list[dict] | None = None,
    dry_run: bool = False,
) -> dict:
    """
    Submit Anthropic Batches API calls for all real × shuffled × configs.

    For each real chain: 1 real call + 3 shuffled calls (shuffle seeds 42, 1337, 7919).
    For each config: 1,200 chains × 4 conditions = 4,800 calls per config.
    Total for all 3 configs: 14,400 calls.
    """
    if configs is None:
        configs = EVAL_CONFIGS

    env_vals = dotenv_values(pathlib.Path(__file__).parent.parent / ".env")
    client = anthropic.Anthropic(api_key=env_vals.get("ANTHROPIC_API_KEY"))

    # Build request list and metadata index
    all_requests: dict[str, list] = {cfg["label"]: [] for cfg in configs}
    chain_meta: dict[str, dict] = {}

    # Path to v1's pre-rendered shuffled chains (set up by scripts/setup_v4_chains.py).
    # v3's shuffler does NOT regenerate the `rendered` field, so on-the-fly shuffles
    # would submit the real chain's rendering as the "shuffled" prompt. v1's pre-gen
    # shuffles use the same seeds (42, 1337, 7919) and have constraints identical to
    # what shuffle_chain() produces, but with correctly-rendered prompt text.
    shuffled_chains_dir = pathlib.Path("data/v4_pokemon_chains/shuffled/pokemon")

    def _load_v1_shuffled(real_cid: str, shuf_seed: int) -> dict:
        path = shuffled_chains_dir / f"{real_cid}_shuffled_{shuf_seed}.jsonl"
        with open(path) as f:
            return json.loads(f.readline().strip())

    for chain in real_chains:
        real_cid = chain["chain_id"]
        real_msg, cutoff_k = _build_prompt_for_chain(chain)

        # Load v1's pre-rendered shuffled variants (correct rendered field)
        shuffled_chains = {seed: _load_v1_shuffled(real_cid, seed) for seed in SHUFFLE_SEEDS}

        for cfg in configs:
            temp = cfg["temperature"]
            seed = cfg["seed"]
            label = cfg["label"]

            # Real chain call
            real_custom_id = _make_custom_id(seed, real_cid)
            chain_meta[real_custom_id] = {
                "chain_id": real_cid, "cutoff_k": cutoff_k,
                "temperature": temp, "seed": seed, "config_label": label,
            }
            all_requests[label].append({
                "custom_id": real_custom_id,
                "params": {
                    "model": MODEL_ID, "max_tokens": 50,
                    "temperature": temp, "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": real_msg}],
                },
            })

            # Shuffled chain calls (one per shuffle seed)
            for shuf_seed in SHUFFLE_SEEDS:
                shuf_chain = shuffled_chains[shuf_seed]
                shuf_cid = shuf_chain["chain_id"]
                shuf_msg, shuf_cutoff = _build_prompt_for_chain(shuf_chain)
                shuf_custom_id = _make_custom_id(seed, shuf_cid)
                chain_meta[shuf_custom_id] = {
                    "chain_id": shuf_cid, "cutoff_k": shuf_cutoff,
                    "temperature": temp, "seed": seed, "config_label": label,
                }
                all_requests[label].append({
                    "custom_id": shuf_custom_id,
                    "params": {
                        "model": MODEL_ID, "max_tokens": 50,
                        "temperature": temp, "system": SYSTEM_PROMPT,
                        "messages": [{"role": "user", "content": shuf_msg}],
                    },
                })

    total = sum(len(v) for v in all_requests.values())
    print(f"[v4_runner] {total} total requests across {len(configs)} configs")
    for label, reqs in all_requests.items():
        print(f"  {label}: {len(reqs)} requests")

    if dry_run:
        # Preview first prompt
        first_reqs = next(iter(all_requests.values()))
        if first_reqs:
            first = first_reqs[0]
            print(f"\n[dry-run] first custom_id: {first['custom_id']}")
            print(f"[dry-run] prompt preview:\n{first['params']['messages'][0]['content'][:300]}...")
        print(f"\n[dry-run] estimated cost: ~${total * 0.0015:.2f} (rough Haiku batch rate)")
        return {"dry_run": True, "total_requests": total}

    # Submit and poll
    stats: dict = {"submitted": total, "completed": 0, "errors": 0}
    for label, requests in all_requests.items():
        batch_ids = []
        for i in range(0, len(requests), _MAX_BATCH_SIZE):
            chunk = requests[i:i + _MAX_BATCH_SIZE]
            batch = client.messages.batches.create(requests=chunk)
            batch_ids.append(batch.id)
            print(f"[v4_runner] submitted batch {batch.id} ({len(chunk)} requests) [{label}]")

        for batch_id in batch_ids:
            while True:
                batch = client.messages.batches.retrieve(batch_id)
                if batch.processing_status in _BATCH_TERMINAL_STATUSES:
                    if batch.processing_status != "ended":
                        print(f"[v4_runner] WARN: batch {batch_id} terminated as "
                              f"{batch.processing_status!r}")
                    break
                print(f"[v4_runner] batch {batch_id} [{label}] status={batch.processing_status}")
                time.sleep(_BATCH_POLL_INTERVAL)

        for batch_id in batch_ids:
            for result in client.messages.batches.results(batch_id):
                cid = result.custom_id
                meta = chain_meta.get(cid)
                if meta is None:
                    print(f"[v4_runner] WARN: unrecognized custom_id {cid!r}")
                    stats["errors"] += 1
                    continue
                if result.result.type == "succeeded":
                    response_text = _v3_runner._extract_response_text(
                        result.result.message.content
                    )
                    _save_result(
                        meta["chain_id"], meta["cutoff_k"],
                        meta["temperature"], meta["seed"],
                        response_text, output_dir, meta["config_label"],
                    )
                    stats["completed"] += 1
                else:
                    print(f"[v4_runner] batch error for {cid}: {result.result}")
                    stats["errors"] += 1

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="src.v4_runner")
    parser.add_argument("--chains-dir", type=Path,
                        default=Path("data/v1_chains_mirror"))
    parser.add_argument("--selection", type=Path,
                        default=Path("v4_chain_selection.json"))
    parser.add_argument("--out", type=Path,
                        default=Path("results/raw/phase1"))
    parser.add_argument("-n", type=int, default=None,
                        help="Limit to first N chains (pilot / dry-run)")
    parser.add_argument("--config", choices=["primary", "variance1", "variance2", "all"],
                        default="all")
    parser.add_argument("--batch", action="store_true",
                        help="Use Anthropic Messages Batches API")
    parser.add_argument("--dry-run", action="store_true",
                        help="Count calls and preview prompt without calling API")
    args = parser.parse_args()

    config_map = {c["label"]: c for c in EVAL_CONFIGS}
    if args.config == "all":
        selected_configs = EVAL_CONFIGS
    else:
        selected_configs = [config_map[args.config]]

    chains = load_selected_chains(args.chains_dir, args.selection, n=args.n)
    print(f"[v4_runner] loaded {len(chains)} chains")

    if not args.batch and not args.dry_run:
        print("[v4_runner] ERROR: synchronous mode not supported. Use --batch or --dry-run.")
        sys.exit(1)

    result = run_batch(chains, args.out, configs=selected_configs, dry_run=args.dry_run)
    print(f"\n[v4_runner] done: {result}")
