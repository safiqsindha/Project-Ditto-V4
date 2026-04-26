"""
Set up v4 chain directories for the scorer.

Creates:
  data/v4_pokemon_chains/real/pokemon/{chain_id}.jsonl     (symlinks to mirror)
  data/v4_pokemon_chains/shuffled/pokemon/{chain_id}.jsonl (symlinks to v1 shuffled)

The scorer (v3's score_all) expects:
  {chains_real_dir}/{source}/{chain_id}.jsonl
  {chains_shuffled_dir}/{source}/{chain_id}.jsonl

This script creates the right directory structure as symlinks so the original
files are not duplicated. Run once before Session 2 pilot scoring.

Inputs:
  data/v1_chains_mirror/     — v4's mirrored real chains
  v4_chain_selection.json    — the 1,200 selected chain IDs
  V1_SHUFFLED_DIR            — path to v1's pre-generated shuffled chains
                               (set via --v1-shuffled or the V1_SHUFFLED_DIR env var)

Usage
-----
  python scripts/setup_v4_chains.py \
    --v1-shuffled "/path/to/Ditto/chains/shuffled"
"""

from __future__ import annotations

import json
import os
import pathlib
import sys

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
MIRROR_DIR = PROJECT_ROOT / "data" / "v1_chains_mirror"
SELECTION_PATH = PROJECT_ROOT / "v4_chain_selection.json"
CHAINS_DIR = PROJECT_ROOT / "data" / "v4_pokemon_chains"
REAL_DIR = CHAINS_DIR / "real" / "pokemon"
SHUFFLED_DIR = CHAINS_DIR / "shuffled" / "pokemon"
SHUFFLE_SEEDS = [42, 1337, 7919]


def setup(v1_shuffled_dir: pathlib.Path) -> None:
    REAL_DIR.mkdir(parents=True, exist_ok=True)
    SHUFFLED_DIR.mkdir(parents=True, exist_ok=True)

    with open(SELECTION_PATH) as f:
        selection = json.load(f)
    chain_ids = selection["chain_ids"]

    real_ok = real_missing = shuf_ok = shuf_missing = 0

    for cid in chain_ids:
        # Real chain symlink
        src = MIRROR_DIR / f"{cid}.jsonl"
        dst = REAL_DIR / f"{cid}.jsonl"
        if src.exists():
            if not dst.exists():
                dst.symlink_to(src.resolve())
            real_ok += 1
        else:
            print(f"[setup] WARN: real chain not found: {src}")
            real_missing += 1

        # Shuffled chain symlinks (one per shuffle seed)
        for seed in SHUFFLE_SEEDS:
            shuf_cid = f"{cid}_shuffled_{seed}"
            shuf_src = v1_shuffled_dir / f"{shuf_cid}.jsonl"
            shuf_dst = SHUFFLED_DIR / f"{shuf_cid}.jsonl"
            if shuf_src.exists():
                if not shuf_dst.exists():
                    shuf_dst.symlink_to(shuf_src.resolve())
                shuf_ok += 1
            else:
                print(f"[setup] WARN: shuffled chain not found: {shuf_src}")
                shuf_missing += 1

    print(f"\n[setup] Real chains:     {real_ok} linked, {real_missing} missing")
    print(f"[setup] Shuffled chains: {shuf_ok} linked, {shuf_missing} missing")
    print(f"[setup] Directories created:")
    print(f"  {REAL_DIR}")
    print(f"  {SHUFFLED_DIR}")

    if real_missing or shuf_missing:
        print(f"\n[setup] WARN: {real_missing + shuf_missing} chains missing — "
              f"check v1_shuffled_dir path and mirror completeness")
    else:
        print(f"\n[setup] OK — all {len(chain_ids)} real + "
              f"{len(chain_ids) * len(SHUFFLE_SEEDS)} shuffled chains linked")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="scripts.setup_v4_chains")
    parser.add_argument(
        "--v1-shuffled", type=pathlib.Path,
        default=pathlib.Path(os.environ.get("V1_SHUFFLED_DIR", "")),
        help="Path to v1's chains/shuffled/ directory",
    )
    args = parser.parse_args()

    if not args.v1_shuffled or not args.v1_shuffled.exists():
        print(f"ERROR: --v1-shuffled path not found: {args.v1_shuffled}")
        print("Set V1_SHUFFLED_DIR env var or pass --v1-shuffled explicitly.")
        sys.exit(1)

    setup(args.v1_shuffled)
