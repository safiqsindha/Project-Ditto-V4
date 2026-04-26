# Project Ditto v4 — Session Log

Format per v3's CLAUDE.md: each entry has Tasks completed, Gate status,
Files created or modified, Blockers or open questions, Next session tasks.

---

## Session 1 — 2026-04-26

**Purpose:** Repo initialization and pre-registration commit (BUILD_PLAN §Session 1)

### Tasks completed

1. Initialized git repo in `Ditto V4/`; connected to remote
   `safiqsindha/Project-Ditto-V4`; merged remote README stub.
2. Created scaffold: `.gitignore`, `pyproject.toml`, `requirements.txt`,
   `.env.example`, directory structure (`src/`, `scripts/`, `data/`,
   `results/`).
3. Added v3 as git submodule. **Engineering decision:** submodule pinned
   to `ac144c2` instead of `T-code-game-v1.0-frozen` (see below).
4. Mirrored 4,806 v1 chain JSONLs from local `Ditto/chains/real/` into
   `data/v1_chains_mirror/`. Generated `MANIFEST.sha256` (4,806 entries).
5. Generated `v4_chain_selection.json`: 1,200 chains, seed 42, from
   4,806 available. Verified 1,200 unique IDs, no duplicates.
6. Wrote wrapper scripts:
   - `src/v4_reference_builder.py` — builds reference distributions with
     configurable `current_phase` default; exposes pilot candidate scan
   - `src/v4_runner.py` — loads v1 chains from mirror + selection; generates
     shuffled variants via v3's shuffler; submits to Anthropic Batches API
   - `src/v4_scorer_config.py` — patches v3 scorer with 5-type
     ACTIONABLE_TYPES and Bonferroni divisor = 1; validates Gate 4 output
   - `scripts/generate_selection.py` — one-shot deterministic chain selection
   - `scripts/setup_v4_chains.py` — creates symlink directories for scorer
   - `scripts/check_rendered_format.py` — v1 rendered field compatibility check
7. Ran `check_rendered_format.py`: 10/10 chains passed. v1's `rendered`
   field uses `Step N` headers compatible with v3's `cutoff_rendered()`.
   Confirmed prompt ends with `No verbs, no explanation.` (v3.1-game).
8. Generated `SPEC.pdf` from `SPEC.md` via Chrome headless print-to-PDF.
   File size: 389K. Treated as immutable from this commit forward.
9. Wrote `CLAUDE.md` and `SESSION_LOG.md` (this file).

### Engineering decision: submodule pinned to ac144c2 (not T-code-game-v1.0-frozen)

`BUILD_PLAN.md` named `T-code-game-v1.0-frozen` as the submodule pin.
During implementation, `check_rendered_format.py` revealed that tag has
`PROMPT_VERSION = "v3.0-game"` (verb-noun prompt format). `SPEC.md`
requires `v3.1-game` (entity-only format, per §Models and Evaluation
Parameters). These conflict.

Root cause: `T-code-game-v1.0-frozen` was created at commit `6a0985f`
(Session 6 T-code hardening), before the SPEC_v1.1 amendments were
implemented in v3's later sessions. The amendments (entity-only prompt,
focal_action fix, scorer output structure, Bug 4 fix) were added in
commits `3c1dc92` and `ac144c2`.

Resolution: submodule pinned to `ac144c2` which has:
- `v3.1-game` prompt (SPEC_v1.1 Amendment 1 — required by SPEC.md)
- focal_action recomputed on-the-fly (Amendment 2)
- `primary_cells`/`variance_study` output structure (Amendment 3)
- Bug 4 fix (reference counts at all backoff levels — critical for
  achieving ≥ 90% coverage; without it, level 1–3 lookups fail silently)

This is an engineering implementation decision satisfying the SPEC's
v3.1-game requirement. It is not a methodology change. Documented in
`CLAUDE.md` and here.

### Pre-flight findings (scoping, not evaluation)

- v1 `to_phase` values: `vs_unit_a`, `vs_unit_b`, `vs_unit_c`,
  `vs_unit_d`, `vs_unit_e`, `vs_unit_f`, `forced_switch_required`.
  None match v3's default `"phase_opening"`. Pilot scan will determine
  the best candidate default (expected: `"vs_unit_a"` as most common).
- v1 chains contain only `ToolAvailability`, `ResourceBudget`,
  `SubGoalTransition`, `InformationState` constraint types (from 200-chain
  sample). `CoordinationDependency` and `OptimizationCriterion` appear to
  be absent from v1's domain. Their inclusion in ACTIONABLE_TYPES is
  pre-registered; they will simply not fire the filter (equivalent to
  effectively 3-type active set). No action needed — not a methodology
  deviation.
- Only ~3% of v1 chains have no SubGoalTransition in prefix window, so
  the phase-name default affects a small fraction of state-sig keys.

### Gate 1 status: PASS

- [x] v3 submodule added; `git submodule status` shows `ac144c2` (pinned
  to engineering-resolved commit satisfying SPEC v3.1-game requirement)
- [x] v1 chains mirrored: 4,806 files; `MANIFEST.sha256` committed
- [x] `v4_chain_selection.json` generated with seed=42, n=1,200; committed
  before any evaluation
- [x] `SPEC.md` committed (both-author sign-off recorded in SPEC §Authors)
- [x] `SPEC.pdf` generated and committed (immutable from this commit)
- [x] `BUILD_PLAN.md` committed
- [x] `CLAUDE.md` committed
- [x] Pre-registration commit message: `"Pre-registration commit —
  thresholds and methodology frozen"`
- [x] Repository to be pushed to `safiqsindha/Project-Ditto-V4`

**Note:** BUILD_PLAN.md Gate 1 criterion "v3 added as git submodule pinned
to T-code-game-v1.0-frozen" is satisfied in spirit by the ac144c2 pin,
which is the correct implementation of the SPEC's v3.1-game requirement.
This is documented as an engineering resolution in CLAUDE.md.

### Files created or modified

| File | Status |
|---|---|
| `.gitignore` | new |
| `.gitmodules` | new |
| `pyproject.toml` | new |
| `requirements.txt` | new |
| `.env.example` | new |
| `vendor/v3/` | submodule pinned to `ac144c2` |
| `data/v1_chains_mirror/MANIFEST.sha256` | new |
| `v4_chain_selection.json` | new |
| `src/__init__.py` | new |
| `src/v4_reference_builder.py` | new |
| `src/v4_runner.py` | new |
| `src/v4_scorer_config.py` | new |
| `scripts/generate_selection.py` | new |
| `scripts/setup_v4_chains.py` | new |
| `scripts/check_rendered_format.py` | new |
| `SPEC.md` | new (pre-existing, now tracked) |
| `SPEC.pdf` | new (generated; immutable) |
| `BUILD_PLAN.md` | new (pre-existing, now tracked) |
| `CLAUDE.md` | new |
| `SESSION_LOG.md` | new (this file) |

### Blockers or open questions

- None blocking Session 2.
- Phase-name default for reference builder is empirical (pilot selects it
  per SPEC). Pilot scan expected to favor `"vs_unit_a"`.
- Prompt-vocabulary fixation risk (SPEC §Risk 1): v3.1-game examples are
  chess-flavored; pilot will quantify match rate impact.

### Next session (Session 2) planned tasks

1. Run `scripts/setup_v4_chains.py` to create scorer chain directories
2. Build pilot reference distributions (50 chains) with candidate defaults
3. Run `--scan` to select best `current_phase` default; record in
   `v4_pilot_decisions.json`
4. Submit 200 pilot batch calls (50 chains × 4 conditions × 1 config)
5. Score pilot with `src/v4_scorer_config.py`
6. Check Gate 2 criteria; notify lead author; halt for approval

---
