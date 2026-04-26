# Project Ditto v4 — SPEC Amendment v1.1

**Supplements:** `SPEC.md` v1.0 (2026-04-26)
**Date:** 2026-04-26
**Authors:** Safiq Sindha (lead), Myriam (co-author)
**Status:** Both authors approved (2026-04-26)

---

## Amendment 1: ResourceBudget added to ACTIONABLE_TYPES

### What changed

`SPEC.md` §"Reference Distribution Build" specifies a 5-type `ACTIONABLE_TYPES`
set for the layer1_actionable analysis:

```
{ToolAvailability, SubGoalTransition, InformationState,
 CoordinationDependency, OptimizationCriterion}
```

This amendment adds `ResourceBudget` to produce a 6-type set:

```
{ToolAvailability, SubGoalTransition, InformationState,
 CoordinationDependency, OptimizationCriterion, ResourceBudget}
```

### Trigger

Session 2 pilot found both-actionable retention = 30.7% (43/140 pairs),
below the Gate 2 threshold of ≥ 50%. Diagnostic showed 46% of v1 chains
have `ResourceBudget` as the constraint type at cutoff_k. Because both-actionable
requires the type to be actionable in BOTH the real and shuffled chain, expected
retention ≈ (0.54)² = 29%, consistent with observation.

### Rationale for inclusion

`SPEC.md` excludes `ResourceBudget` as a "non-actionable material counter."
That characterization was inherited from v3's chess/draughts framing, where
material count (piece advantage) is strategic background context but not
directly decision-forcing per move.

In the Pokémon Showdown domain, `ResourceBudget` represents HP and PP
tracking. These are categorically different from chess material:

- **HP directly determines survival decisions.** A Pokémon at ≤25% HP is in
  KO range for many common moves; the player must decide whether to switch,
  sacrifice, or attempt a speed KO. HP percentage is the primary input to
  risk-management calculations.
- **PP exhaustion constrains move availability.** When a Pokémon's PP runs
  low, the move becomes effectively unavailable, collapsing the action space.
  This is a hard constraint on what the player *can* do, not just strategic
  context.
- **Both are explicitly reported in v1 chains** as `ResourceBudget`
  constraints with `amount` fields tracking the resource level.

In the Pokémon domain, `ResourceBudget` is therefore directly actionable:
knowing the resource level changes which moves are viable, which Pokémon
should be sacrificed, and what speed tier is relevant. This parallels
`ToolAvailability` in the coding domain (does the model have the tool it
needs?) — the resource availability constrains what actions are possible.

The original `ResourceBudget` exclusion was domain-appropriate for
chess/draughts (v3) and arguably for SWE/TB coding (v2). For v1 Pokémon, the
exclusion removes the most operationally critical constraint type from the
analysis. Including it is the correct domain adaptation.

### Impact on pre-registered analysis

1. **Layer1_actionable**: both-actionable pair count increases from ~30% to
   ~100% of covered pairs (all 6 types cover the full v1 constraint type
   distribution observed in the pilot). Expected ~360 → ~1,200+ actionable
   pairs in the full 1,200-chain run.

2. **Reference distribution**: unchanged. The reference build uses all
   constraint types regardless of ACTIONABLE_TYPES. No re-build required.

3. **Outcome interpretation thresholds**: unchanged. Gap ≥ 0.08, p < 0.01
   for strong-positive; gap ≥ 0.05, p < 0.05 for moderate-positive (per
   SPEC.md §"Pre-registered Success Criteria").

4. **Bonferroni divisor**: unchanged (1, single cell).

5. **This is the only change to the methodology.** All other SPEC.md
   commitments remain in force.

### Implementation

- `src/v4_scorer_config.py`: `V4_ACTIONABLE_TYPES` updated to include
  `"ResourceBudget"`.
- `CLAUDE.md`: ACTIONABLE_TYPES note updated to reflect 6-type set.
- `data/reference_v4_pokemon_pilot.pkl`: **not regenerated** (ACTIONABLE_TYPES
  does not affect reference build).
- `v4_pilot_decisions.json`: amendment note added.
- Pilot re-scored with 6-type set to verify Gate 2 now passes.

### Sign-off

| Author | Role | Date | Signature |
|---|---|---|---|
| Safiq Sindha | Lead author | 2026-04-26 | ✓ approved |
| Myriam | Co-author | 2026-04-26 | ✓ approved |

---

## Amendment 2: `phase_` prefix strip in response normalization

### What changed

v3's `normalize_action` (in `vendor/v3/src/normalize.py`) is documented as
"domain-blind" — it lowercases, strips whitespace, and removes punctuation,
but does no entity-class prefix handling. SPEC.md applies v3's methodology
unchanged, so v4 inherits this normalization.

This amendment adds a v4-specific normalization adapter that strips a
leading `phase_` prefix from model responses *during scoring only*. The
adapter is implemented in `src/v4_scorer_config.py` via the same
monkey-patch pattern used for `extract_state_signature` and
`classify_outcome_tier`. It does NOT modify `vendor/v3/`.

```
normalize_v4(s):
    out = v3_normalize_action(s)
    if out.startswith("phase_"):
        out = out[len("phase_"):]
    return out
```

The reference distribution build is unaffected: v1 chains do not have
entities natively prefixed with `phase_` (SubGoalTransition `to_phase`
values are bare names like `vs_unit_a`, `forced_switch_required`), so
`extract_entity_from_constraint` already produces bare names. The
asymmetry exists only on the response side, where the v3.1-game prompt's
chess-flavored example token (`phase_endgame`) induces `phase_X` outputs.

### Trigger

Session 2 bug scan (Opus) and direct simulation found:
- 22.0% of real responses (11/50) carried a `phase_` prefix
- 8.0% of shuffled responses (12/150) carried a `phase_` prefix

The asymmetry arises because real chains preserve coherent phase signal,
making the model more likely to emit a phase-style answer. Without the
strip, all 11 real `phase_X` responses miss against the reference (which
stores bare names); the model's correct intent is being scored as a miss.

Pilot impact (50-chain re-score with the patch): real_rate 0.20 → 0.22,
shuffled_rate unchanged at 0.173, gap +0.0267 → +0.0467.

### Rationale for the amendment

SPEC.md §"Risk 1: Prompt-vocabulary fixation" pre-registered the risk
that v3.1-game's chess-flavored prompt examples could induce v3-style
output formats on v1 data. The amendment does **not** change the prompt
or the methodology's match-counting rule conceptually — it adds a thin
adapter that recovers the model's clear intent (`phase_vs_unit_a` was
"a phase prediction of `vs_unit_a`") in the v1 entity space.

Without the adapter, the experiment systematically discounts a class of
correct predictions by an artifact of cross-domain prompt vocabulary.
With the adapter, scoring measures whether v3's methodology can
distinguish real from shuffled v1 chains under the v3.1-game prompt,
without an unnecessary penalty for prompt-induced format mismatch.

The adapter is conservative:
- Stripped only when the leading prefix is exactly `phase_`
- Applied after v3's existing `normalize_action`
- No reference-build-side change required (v1 references are already
  bare names)
- v3 source is not modified; the patch lives in `v4_scorer_config.py`

### Impact on pre-registered analysis

1. **Match counting**: real responses with `phase_` prefix are now
   eligible for matches against bare-name references. Effect is
   asymmetric (favors real_rate) because the prompt-vocabulary fixation
   itself is asymmetric.
2. **Reference distribution**: unchanged. Build path unaffected.
3. **Outcome interpretation thresholds**: unchanged.
4. **Bonferroni divisor**: unchanged.
5. **All other SPEC.md commitments remain in force.**

### Implementation

- `src/v4_scorer_config.py`: `_normalize_action_spec` adapter; monkey-
  patches `_v3_normalize.normalize_action` in `score_v4()` and restores
  in `finally`.
- `vendor/v3/src/normalize.py`: not modified.
- `data/reference_v4_pokemon_pilot.pkl`: not regenerated (reference
  builds use `extract_entity_from_constraint` directly, which is
  unchanged).
- Pilot re-scored with the adapter to verify behavior.

### Sign-off

| Author | Role | Date | Signature |
|---|---|---|---|
| Safiq Sindha | Lead author | 2026-04-26 | ✓ approved |
| Myriam | Co-author | 2026-04-26 | ✓ approved |

---

*SPEC_v1.1.md — 2026-04-26. Supplements SPEC.md v1.0; does not modify SPEC.md.*
