"""
v4 scorer configuration wrapper.

Wraps v3's scorer with the two v1-domain adaptations pre-committed in SPEC.md:

  1. SOURCES = ["pokemon"]  (single cell, single source)
  2. ACTIONABLE_TYPES = {ToolAvailability, SubGoalTransition, InformationState,
                         CoordinationDependency, OptimizationCriterion}
     (5-type set; InformationState re-included for v1's hidden-info domain)
  3. Bonferroni divisor = 1  (single cell; no correction applied)

v3 code is NOT modified. Module-level constants are patched before calling
v3's score_all function.

Output schema: matches v3's SPEC_v1.1 Amendment 3 structure
  primary_cells:  {"haiku::pokemon": {...}}
  variance_study: {"haiku::pokemon::T0.5_seed1337": {...},
                   "haiku::pokemon::T0.5_seed7919": {...}}

Requires a pokemon chain directory structure under --chains-dir:
  {chains-dir}/real/pokemon/{chain_id}.jsonl    (real chains)
  {chains-dir}/shuffled/pokemon/{chain_id}.jsonl (shuffled chains)

Run scripts/setup_v4_chains.py first to create these directories.

Usage
-----
  # Pilot scoring:
  python -m src.v4_scorer_config \
    --results results/raw/pilot \
    --reference data/reference_v4_pokemon_pilot.pkl \
    --chains-dir data/v4_pokemon_chains \
    --out results/pilot_scored.json

  # Full evaluation scoring (Session 4 — fresh session):
  python -m src.v4_scorer_config \
    --results results/raw/phase1 \
    --reference data/reference_v4_pokemon_full.pkl \
    --chains-dir data/v4_pokemon_chains \
    --out results/v4_scored.json
"""

from __future__ import annotations

import json
import pathlib
import sys
from pathlib import Path

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


# scorer imports from src.normalize and src.reference — load those first
_load_v3("normalize")
_load_v3("reference")
_v3_scorer = _load_v3("scorer")

# ---------------------------------------------------------------------------
# v4 configuration patches
# ---------------------------------------------------------------------------

V4_SOURCES: list[str] = ["pokemon"]

# v1-domain actionable types (SPEC.md §Reference Distribution Build)
# InformationState included — Pokémon battles have meaningful hidden information.
# ResourceBudget excluded — non-actionable material counter, same as v2/v3.
V4_ACTIONABLE_TYPES: set[str] = {
    "ToolAvailability",
    "SubGoalTransition",
    "InformationState",
    "CoordinationDependency",
    "OptimizationCriterion",
}

# Bonferroni divisor = 1 (single analysis, single cell — no correction applied)
V4_BONFERRONI_DIVISOR: int = 1


def score_v4(
    results_dir: Path,
    reference_path: Path,
    chains_dir: Path,
    out_path: Path,
) -> dict:
    """
    Score v4 results with the v1-domain configuration.

    Patches v3's module-level SOURCES and ACTIONABLE_TYPES, calls score_all,
    then restores originals.
    """
    # Patch module constants
    orig_sources = _v3_scorer.SOURCES
    orig_actionable = _v3_scorer.ACTIONABLE_TYPES

    _v3_scorer.SOURCES = V4_SOURCES
    _v3_scorer.ACTIONABLE_TYPES = V4_ACTIONABLE_TYPES

    try:
        dist_paths = {"pokemon": reference_path}
        chains_real_dir = chains_dir / "real"
        chains_shuffled_dir = chains_dir / "shuffled"

        scored = _v3_scorer.score_all(
            results_dir,
            dist_paths,
            chains_real_dir,
            chains_shuffled_dir,
            bonferroni_divisor=V4_BONFERRONI_DIVISOR,
        )
    finally:
        _v3_scorer.SOURCES = orig_sources
        _v3_scorer.ACTIONABLE_TYPES = orig_actionable

    return scored


def validate_output(scored: dict, pilot: bool = False) -> list[str]:
    """
    Validate scored output against Gate 4 pass criteria.

    Returns list of failure messages (empty = all pass).
    pilot=True skips the variance_study check (pilot only runs primary config).
    """
    failures = []

    primary = scored.get("primary_cells", {})
    if list(primary.keys()) != ["haiku::pokemon"]:
        failures.append(f"primary_cells keys: expected ['haiku::pokemon'], got {list(primary.keys())}")

    variance = scored.get("variance_study", {})
    if not pilot:
        expected_var = {"haiku::pokemon::T0.5_seed1337", "haiku::pokemon::T0.5_seed7919"}
        if set(variance.keys()) != expected_var:
            failures.append(f"variance_study keys: expected {expected_var}, got {set(variance.keys())}")

    for label, cell in {**primary, **variance}.items():
        for field in ("gap", "mcnemar_chi2", "raw_p", "bonferroni_p",
                      "n_pairs", "both_actionable_retention", "outcome_tier"):
            # Check top-level or within layer1_actionable (v3's nested format)
            l1a = cell.get("layer1_actionable_bonferroni") or cell.get("layer1_actionable") or {}
            if field == "outcome_tier" and "outcome_tier" not in cell:
                failures.append(f"{label}: missing 'outcome_tier'")
            if field == "gap" and "gap" not in l1a:
                failures.append(f"{label}: missing 'gap' in layer1_actionable")

        tier = cell.get("outcome_tier")
        valid_tiers = {"strong_positive", "moderate_positive", "weak_mixed", "null", "reversed"}
        if tier and tier not in valid_tiers:
            failures.append(f"{label}: invalid outcome_tier {tier!r}")

    return failures


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="src.v4_scorer_config")
    parser.add_argument("--results", type=Path, required=True,
                        help="Directory containing raw result JSON files")
    parser.add_argument("--reference", type=Path, required=True,
                        help="Path to reference_v4_pokemon_*.pkl")
    parser.add_argument("--chains-dir", type=Path,
                        default=Path("data/v4_pokemon_chains"),
                        help="Base dir with real/ and shuffled/ subdirectories")
    parser.add_argument("--out", type=Path, required=True,
                        help="Output path for scored JSON")
    parser.add_argument("--pilot", action="store_true",
                        help="Pilot mode: skip variance_study Gate 4 check (primary config only)")
    args = parser.parse_args()

    print(f"[v4_scorer] SOURCES={V4_SOURCES}")
    print(f"[v4_scorer] ACTIONABLE_TYPES={sorted(V4_ACTIONABLE_TYPES)}")
    print(f"[v4_scorer] Bonferroni divisor={V4_BONFERRONI_DIVISOR}")

    scored = score_v4(args.results, args.reference, args.chains_dir, args.out.parent / "tmp")

    # Validate output structure
    failures = validate_output(scored, pilot=args.pilot)
    if failures:
        print("\n[v4_scorer] GATE 4 FAILURES:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(scored, f, indent=2)

    print(f"\n[v4_scorer] Gate 4 PASS — results written to {args.out}")

    # Print summary
    primary = scored.get("primary_cells", {})
    print("\n=== PRIMARY (haiku::pokemon) ===")
    for label, cell in primary.items():
        l1a = cell.get("layer1_actionable_bonferroni", cell.get("layer1_actionable", {}))
        gap = l1a.get("gap", "N/A")
        p_bon = l1a.get("p_value_bonferroni", l1a.get("p_value", "N/A"))
        tier = cell.get("outcome_tier", "?")
        n_act = cell.get("diagnostics", {}).get("n_pairs_actionable", "N/A")
        print(f"  {label}: gap={gap}  p={p_bon}  n_act={n_act}  tier={tier}")

    variance = scored.get("variance_study", {})
    if variance:
        print("\n=== VARIANCE STUDY ===")
        for label, cell in sorted(variance.items()):
            l1a = cell.get("layer1_actionable", {})
            gap = l1a.get("gap", "N/A")
            print(f"  {label}: gap={gap}")
