# Project Ditto v4 — SPEC Amendment v1.1

**Supplements:** `SPEC.md` v1.0 (2026-04-26)
**Date:** 2026-04-26
**Authors:** Safiq Sindha (lead), Myriam (co-author)
**Status:** Lead author approved; co-author sign-off pending

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
| Myriam | Co-author | — | pending |

---

*SPEC_v1.1.md — 2026-04-26. Supplements SPEC.md v1.0; does not modify SPEC.md.*
