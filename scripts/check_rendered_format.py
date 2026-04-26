"""
Sanity check: verify v1 chain 'rendered' fields are compatible with v3's
cutoff_rendered() function.

v3's cutoff_rendered() splits on "Step N" boundaries using re.split(r"(Step \d+)", ...).
v1's rendered format must use the same "Step N" header convention for the
prompt builder to work correctly.

Run once during Session 1 repo initialization.

Usage
-----
  python scripts/check_rendered_format.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
MIRROR_DIR = PROJECT_ROOT / "data" / "v1_chains_mirror"
SELECTION_PATH = PROJECT_ROOT / "v4_chain_selection.json"

_VENDOR_V3 = PROJECT_ROOT / "vendor" / "v3"
if str(_VENDOR_V3) not in sys.path:
    sys.path.insert(0, str(_VENDOR_V3))

from src.prompt_builder import cutoff_rendered, build_prompt  # noqa: E402


def check(n_samples: int = 10) -> bool:
    with open(SELECTION_PATH) as f:
        chain_ids = json.load(f)["chain_ids"]

    passed = 0
    failed = 0

    for cid in chain_ids[:n_samples]:
        path = MIRROR_DIR / f"{cid}.jsonl"
        with open(path) as f:
            chain = json.loads(f.readline().strip())

        rendered = chain.get("rendered", "")
        cutoff_k = chain.get("cutoff_k", 0)

        if not rendered:
            print(f"FAIL [{cid}]: empty rendered field")
            failed += 1
            continue

        # Count steps in rendered
        step_matches = re.findall(r"Step \d+", rendered)
        if not step_matches:
            print(f"FAIL [{cid}]: no 'Step N' headers found in rendered")
            print(f"  rendered[:200]: {rendered[:200]!r}")
            failed += 1
            continue

        # Try truncating
        truncated = cutoff_rendered(rendered, cutoff_k)
        if not truncated:
            print(f"FAIL [{cid}]: cutoff_rendered returned empty for cutoff_k={cutoff_k}")
            failed += 1
            continue

        # Build full prompt
        prompt = build_prompt(truncated, cutoff_k)
        if not prompt:
            print(f"FAIL [{cid}]: build_prompt returned empty")
            failed += 1
            continue

        truncated_steps = re.findall(r"Step \d+", truncated)
        print(f"OK   [{cid}]: {len(step_matches)} total steps, "
              f"{len(truncated_steps)} shown (cutoff_k={cutoff_k})")
        print(f"     prompt ends: ...{prompt[-80:].strip()!r}")
        passed += 1

    print(f"\nResult: {passed}/{n_samples} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    ok = check(n_samples=10)
    sys.exit(0 if ok else 1)
