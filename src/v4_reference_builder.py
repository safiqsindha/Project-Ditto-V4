"""
v4 reference distribution builder.

Wraps v3's ReferenceDistribution.build_from_chains with two v4-specific needs:

1. Configurable current_phase default — v3 hardcodes "phase_opening" (chess
   vocabulary). v1 chains use "vs_unit_a", "forced_switch_required", etc.
   This module patches extract_state_signature at call time so the default
   can be tested without modifying v3 source.

2. Pilot candidate scan — builds distributions under several candidate defaults
   and reports level-0/1 coverage for each, so the pilot can select the best.

Usage
-----
  # Pilot scan (Session 2):
  python -m src.v4_reference_builder --scan \
    --chains-dir data/v1_chains_mirror \
    --selection v4_chain_selection.json \
    --pilot-n 50

  # Full build (after pilot selects default):
  python -m src.v4_reference_builder \
    --chains-dir data/v1_chains_mirror \
    --selection v4_chain_selection.json \
    --default-phase vs_unit_a \
    --out data/reference_v4_pokemon_full.pkl \
    --coverage-out data/reference_v4_pokemon_full.coverage.json
"""

from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

# ---------------------------------------------------------------------------
# Vendor path setup — load v3 modules by path to avoid src namespace conflict
# ---------------------------------------------------------------------------

import importlib.util  # noqa: E402

_V3_SRC = pathlib.Path(__file__).parent.parent / "vendor" / "v3" / "src"


def _load_v3(name: str):
    """Load a v3 src module by file path and register it as src.{name}."""
    key = f"src.{name}"
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, _V3_SRC / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod


_v3_ref = _load_v3("reference")
ReferenceDistribution = _v3_ref.ReferenceDistribution

# Default candidates to test during pilot scan. "phase_opening" is v3's
# default (won't appear in v1 data but establishes a coverage baseline).
# "vs_unit_a" is the most common v1 to_phase value (~23% of SGT events).
CANDIDATE_DEFAULTS: list[str] = [
    "vs_unit_a",
    "forced_switch_required",
    "vs_unit_b",
    "phase_opening",   # v3 default — baseline comparison
    "unknown",
]


def _load_selected_chains(
    chains_dir: pathlib.Path,
    selection_path: pathlib.Path,
    n: int | None = None,
) -> list[dict]:
    """Load chains from mirror filtered to the pre-registered selection."""
    with open(selection_path) as f:
        selection = json.load(f)
    chain_ids = selection["chain_ids"]
    if n is not None:
        chain_ids = chain_ids[:n]

    chains = []
    for cid in chain_ids:
        p = chains_dir / f"{cid}.jsonl"
        if not p.exists():
            print(f"[v4_ref] WARN: chain not found: {p}")
            continue
        with open(p) as f:
            chains.append(json.loads(f.readline().strip()))
    return chains


def _make_patched_extract(default_phase: str):
    """Return a version of extract_state_signature with a custom default_phase."""
    original = _v3_ref.extract_state_signature

    def patched(constraints, cutoff_k, backoff_level=0):
        # Identical logic to v3 except the hardcoded "phase_opening" default
        # is replaced with default_phase.
        if not constraints or cutoff_k <= 0:
            if backoff_level == 0:
                return (default_phase, "unknown", 4, "unknown")
            if backoff_level == 1:
                return (default_phase, "unknown", 4)
            if backoff_level == 2:
                return (default_phase, "unknown")
            return (default_phase,)

        window = constraints[:cutoff_k]
        current_phase = default_phase
        for c in reversed(window):
            if c.get("type") == "SubGoalTransition":
                current_phase = c.get("to_phase", default_phase)
                break

        last_constraint = window[-1]
        last_move_type = last_constraint.get("type", "unknown")

        resource_bracket = 4
        for c in reversed(window):
            if c.get("type") == "ResourceBudget":
                resource_bracket = _v3_ref._resource_bracket(c.get("amount", 1.0))
                break

        entity_label = _v3_ref.extract_entity_from_constraint(last_constraint) or "unknown"

        if backoff_level == 0:
            return (current_phase, last_move_type, resource_bracket, entity_label)
        elif backoff_level == 1:
            return (current_phase, last_move_type, resource_bracket)
        elif backoff_level == 2:
            return (current_phase, last_move_type)
        else:
            return (current_phase,)

    return patched, original


def build_with_default(
    chains: list[dict],
    source: str,
    default_phase: str,
) -> ReferenceDistribution:
    """Build a reference distribution using the specified current_phase default."""
    patched, original = _make_patched_extract(default_phase)
    _v3_ref.extract_state_signature = patched
    try:
        dist = ReferenceDistribution.build_from_chains(chains, source)
    finally:
        _v3_ref.extract_state_signature = original
    return dist


def scan_candidate_defaults(
    chains: list[dict],
    source: str,
    candidates: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Build a reference distribution for each candidate default and report coverage.

    Returns a list of dicts sorted by non_max_backoff_fraction descending.
    """
    if candidates is None:
        candidates = CANDIDATE_DEFAULTS

    results = []
    for candidate in candidates:
        dist = build_with_default(chains, source, candidate)
        cov = dist.check_coverage(chains)
        results.append({
            "default_phase": candidate,
            "total_chains": cov.get("total_chains", 0),
            "non_max_backoff_fraction": cov.get("non_max_backoff_fraction", 0.0),
            "level_counts": cov.get("level_counts", {}),
            "passes_90pct": cov.get("non_max_backoff_fraction", 0.0) >= 0.90,
        })

    results.sort(key=lambda x: -x["non_max_backoff_fraction"])
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="src.v4_reference_builder")
    parser.add_argument("--chains-dir", type=pathlib.Path,
                        default=pathlib.Path("data/v1_chains_mirror"))
    parser.add_argument("--selection", type=pathlib.Path,
                        default=pathlib.Path("v4_chain_selection.json"))
    parser.add_argument("--pilot-n", type=int, default=None,
                        help="Use only the first N chains (pilot mode)")
    parser.add_argument("--scan", action="store_true",
                        help="Scan candidate defaults and report coverage (pilot step)")
    parser.add_argument("--default-phase", type=str, default="vs_unit_a",
                        help="current_phase default to use for building (non-scan mode)")
    parser.add_argument("--out", type=pathlib.Path,
                        default=pathlib.Path("data/reference_v4_pokemon_full.pkl"))
    parser.add_argument("--coverage-out", type=pathlib.Path,
                        default=pathlib.Path("data/reference_v4_pokemon_full.coverage.json"))
    args = parser.parse_args()

    chains = _load_selected_chains(args.chains_dir, args.selection, n=args.pilot_n)
    print(f"[v4_ref] loaded {len(chains)} chains")

    if args.scan:
        print("[v4_ref] scanning candidate defaults...")
        scan_results = scan_candidate_defaults(chains, source="pokemon")
        print("\n=== Candidate default scan (sorted by coverage) ===")
        for r in scan_results:
            flag = "✓" if r["passes_90pct"] else "✗"
            print(f"  {flag} {r['default_phase']:35s}  "
                  f"coverage={r['non_max_backoff_fraction']:.4f}  "
                  f"levels={r['level_counts']}")
        # Save scan results alongside coverage output
        scan_out = args.coverage_out.parent / "pilot_default_scan.json"
        scan_out.parent.mkdir(parents=True, exist_ok=True)
        with open(scan_out, "w") as f:
            json.dump(scan_results, f, indent=2)
        print(f"\n[v4_ref] scan results written to {scan_out}")
    else:
        print(f"[v4_ref] building reference distribution with default='{args.default_phase}'...")
        dist = build_with_default(chains, source="pokemon", default_phase=args.default_phase)
        cov = dist.check_coverage(chains)
        print(f"[v4_ref] coverage: {cov}")

        if cov.get("non_max_backoff_fraction", 0) < 0.90:
            print(f"[v4_ref] WARN: coverage {cov['non_max_backoff_fraction']:.4f} "
                  f"below 0.90 target — check default_phase selection")

        args.out.parent.mkdir(parents=True, exist_ok=True)
        dist.save(args.out)
        print(f"[v4_ref] reference distribution saved to {args.out}")

        args.coverage_out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.coverage_out, "w") as f:
            json.dump(cov, f, indent=2)
        print(f"[v4_ref] coverage stats saved to {args.coverage_out}")
