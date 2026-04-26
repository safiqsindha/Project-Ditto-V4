"""
Generate the deterministic 1,200-chain selection from the v1 chain mirror.

Selection rule (pre-registered in SPEC.md):
  - Sort all chain files in data/v1_chains_mirror/ lexicographically by filename
  - Select 1,200 using random.Random(42)
  - Record seed and ordered list of chain_ids in v4_chain_selection.json

Run once before any evaluation. Output is committed as part of the
pre-registration commit.
"""

from __future__ import annotations

import json
import pathlib
import random
import sys

MIRROR_DIR = pathlib.Path(__file__).parent.parent / "data" / "v1_chains_mirror"
OUTPUT_PATH = pathlib.Path(__file__).parent.parent / "v4_chain_selection.json"
SEED = 42
N = 1200


def main() -> None:
    files = sorted(MIRROR_DIR.glob("*.jsonl"))
    if len(files) < N:
        print(f"ERROR: only {len(files)} chains in mirror, need {N}", file=sys.stderr)
        sys.exit(1)

    rng = random.Random(SEED)
    selected = rng.sample(files, N)
    # Preserve the sample order (not re-sorted) — this is the evaluation order.
    chain_ids = [f.stem for f in selected]

    out = {
        "seed": SEED,
        "n": N,
        "total_available": len(files),
        "chain_ids": chain_ids,
    }
    OUTPUT_PATH.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Written {OUTPUT_PATH}: {N} chains selected from {len(files)} available")
    print(f"First 3: {chain_ids[:3]}")
    print(f"Last 3:  {chain_ids[-3:]}")


if __name__ == "__main__":
    main()
