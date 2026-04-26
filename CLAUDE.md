# Project Ditto v4 — Architecture and Session Protocol

**Read at the start of every session**, after reading `SPEC.md` and the
latest `SESSION_LOG.md` entry.

---

## What v4 is

A single-cell methodology characterization study. It applies v3's
pre-registered methodology (unchanged) to v1's Pokémon Showdown chains
(known to carry real-vs-shuffled signal under v1's own methodology).
The question: does v3's methodology reproduce that signal on clean chains?

One model (Haiku 4.5), one source (pokemon), three eval configs, 14,400
calls total. Pre-registered thresholds and interpretation framework are
in `SPEC.md` (frozen after pre-registration commit).

---

## Repository layout

```
vendor/v3/          v3 git submodule — pinned to commit ac144c2
                    (T-code-game-v1.0-frozen + SPEC_v1.1 amendments + Bug 4 fix)
                    DO NOT MODIFY v3 source. Import via sys.path manipulation.

data/
  v1_chains_mirror/     4,806 v1 chain JSONLs (gitignored)
    MANIFEST.sha256     SHA-256 per-file manifest (committed)
  v4_pokemon_chains/    symlink directories for scorer (gitignored, run setup script)
    real/pokemon/       → symlinks to v1_chains_mirror (1,200 selected)
    shuffled/pokemon/   → symlinks to v1 shuffled chains (3,600)
  reference_v4_pokemon_pilot.pkl    (gitignored — generated Session 2)
  reference_v4_pokemon_full.pkl     (gitignored — generated Session 3)
  reference_v4_pokemon_full.coverage.json   (committed Session 3)

src/
  v4_reference_builder.py  wraps v3 reference builder; configurable phase default
  v4_runner.py             wraps v3 batch runner; pokemon source, Haiku model
  v4_scorer_config.py      wraps v3 scorer; 6-type ACTIONABLE_TYPES (SPEC_v1.1), divisor=1

scripts/
  generate_selection.py    one-shot seed-42 chain selection (run once, committed)
  setup_v4_chains.py       creates symlink directories for scorer
  check_rendered_format.py sanity check v1 rendered field compatibility

results/
  raw/phase1/{config}/pokemon/   (gitignored)
  raw/pilot/pokemon/             (gitignored)
  blinded/phase1/                (gitignored)
  pilot_scored.json              (gitignored)
  v4_scored.json                 (committed — Session 4 output)
  phase1_summary.json            (committed — Session 3 output)

SPEC.md         frozen at pre-registration commit
SPEC.pdf        immutable anchor — generated from SPEC.md, not edited after commit
BUILD_PLAN.md   execution roadmap — can be revised between sessions
RESULTS.md      Session 5 output
SESSION_LOG.md  one entry per session
```

---

## Submodule note (engineering decision, Session 1)

`BUILD_PLAN.md` named `T-code-game-v1.0-frozen` as the pinning target.
That tag has `PROMPT_VERSION = "v3.0-game"` (verb-noun format). `SPEC.md`
requires `v3.1-game` (entity-only format, per SPEC §Models and Evaluation
Parameters). These are inconsistent.

**Resolution:** submodule pinned to `ac144c2` ("Bug 4 fix: populate
reference counts at all 4 backoff levels"). This commit has:
- v3.1-game prompt (SPEC_v1.1 Amendment 1)
- focal_action recomputed on-the-fly (Amendment 2)
- `primary_cells`/`variance_study` output structure (Amendment 3)
- Bug 4 fix (reference counts at all 4 backoff levels — required for
  coverage to exceed 90%; without this fix, shuffled chain pairs with
  no level-0 reference match were silently dropped)

This is an engineering implementation decision, not a methodology change.
The SPEC committed to v3.1-game; the submodule pin satisfies that
requirement. Documented here and in SESSION_LOG.md Session 1.

---

## v1-domain adaptations (pre-committed in SPEC.md)

1. **`current_phase` default** — selected empirically from pilot 50 chains
   (Session 2). v3 defaults to `"phase_opening"` (chess vocabulary); v1's
   `to_phase` values are `vs_unit_a`, `vs_unit_b`, ..., `forced_switch_required`.
   `v4_reference_builder.py` exposes `--scan` to test candidates; the best
   default is recorded in `v4_pilot_decisions.json`.

2. **`ACTIONABLE_TYPES`** — 6-type set per **`SPEC_v1.1.md` Amendment 1**
   (Session 2, 2026-04-26):
   `ToolAvailability`, `SubGoalTransition`, `InformationState`,
   `CoordinationDependency`, `OptimizationCriterion`, `ResourceBudget`.

   `InformationState` included: Pokémon battles have meaningful hidden
   information (opponent Pokémon hidden until revealed).
   `ResourceBudget` added via SPEC_v1.1 Amendment 1: HP/PP in the Pokémon
   domain directly constrains move selection and survival decisions —
   categorically more actionable than chess material counts. Pilot Gate 2
   revealed 46% of chains have ResourceBudget at cutoff_k; both-actionable
   retention was 30.7% without it (below 50% Gate 2 threshold).

   Note: `CoordinationDependency` and `OptimizationCriterion` appear to be
   absent from v1 chains (zero occurrences in pilot). Their presence in
   ACTIONABLE_TYPES has no practical effect but is retained for consistency
   with the 6-type set definition.

---

## Session protocol

### At session start

1. Read `SPEC.md` (frozen — do not modify)
2. Read `CLAUDE.md` (this file)
3. Read `BUILD_PLAN.md` — find the current session's tasks and gate criteria
4. Read the previous `SESSION_LOG.md` entry
5. Confirm `git status` is clean before starting work

### During the session

- Mark tasks complete as you go, not in batches
- Gate failure → document in SESSION_LOG.md and stop for author review
- Do NOT read effect-size outputs during evaluation runs (Sessions 3)
- Engineering changes (defensive patches, path fixes) are permitted;
  record in SESSION_LOG.md
- Methodology changes require `SPEC_v1.1.md` supplement + both-author sign-off
- When unsure whether a change is methodology vs engineering: **stop and ask**

### At session end

- Append SESSION_LOG.md entry with:
  - Tasks completed
  - Gate status
  - Files created or modified
  - Blockers or open questions
  - Next session planned tasks
- Commit with atomic, descriptive commit messages
- Push to GitHub if session output is non-trivial

---

## Quick reference: v4 evaluation parameters

| Parameter | Value |
|---|---|
| Model | Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) |
| Source | `pokemon` (v1 Pokémon Showdown chains) |
| Chain count | 1,200 real + 3,600 shuffled |
| Conditions | 1 real + 3 shuffled per real chain |
| Configs | T=0.0/seed=42 (primary); T=0.5/seed=1337; T=0.5/seed=7919 |
| Total calls | 14,400 (1,200 × 4 conditions × 3 configs) |
| Bonferroni divisor | 1 (single cell — no correction) |
| API | Anthropic Messages Batches (50% cost reduction) |
| Est. cost | $5–10 |
| Hard budget ceiling | $50 |

## Quick reference: pre-registered thresholds

| Tier | Criterion |
|---|---|
| Strong-positive | Layer 1 gap ≥ 0.08 AND Bonferroni p < 0.01 |
| Moderate-positive | Layer 1 gap ≥ 0.05 AND Bonferroni p < 0.05 |
| Null | Gap not clearing 0.05, or p not clearing 0.05 |
| Reversed | Gap negative AND Bonferroni p < 0.05 (negative direction) |

v4 hypothesis supported iff primary clears **at least moderate-positive**.

---

## Cross-session invariants

- `SPEC.md` and `SPEC.pdf` are **never modified** after pre-registration commit
- `v4_chain_selection.json` is **never modified** after pre-registration commit
- v3 submodule is **never modified** (pinned to `ac144c2`)
- Scorer runs in a **separate session** from the evaluation runner
- **No effect-size monitoring** during evaluation (Session 3)
- One `SESSION_LOG.md` entry per session, in the format above

---

*CLAUDE.md v1.0 — 2026-04-26. Companion to SPEC.md v1.0 and BUILD_PLAN.md v1.0.*
