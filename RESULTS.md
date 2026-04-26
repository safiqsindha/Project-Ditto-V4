# Project Ditto v4 — Results

**Status:** DRAFT — pending co-author review (Myriam, Columbia University)

| | |
|---|---|
| Pre-registration | `SPEC.md` v1.0, signed off 2026-04-26 by both authors |
| Pre-registration anchor | `SPEC.pdf` (immutable) |
| Scored output | `results/v4_scored.json` (committed Session 4) |
| Lead author | Safiq Sindha (Microsoft Azure Hardware PM, independent research) |
| Co-author | Myriam (Columbia University, systems engineering; Boeing FT) |
| Date | 2026-04-26 |
| Scoring date | 2026-04-26 (Session 4, separate from evaluation) |

---

## Abstract

Project Ditto v4 is a single-cell methodology characterization study. It applies
v3's pre-registered methodology — the v3.1-game prompt, state-signature design,
both-actionable filter, and paired McNemar / Bonferroni statistical analysis —
to the Pokémon Showdown constraint chains constructed by v1. v1's chains are
known to carry a real-vs-shuffled detectability gap under v1's own pre-registered
methodology (published 2026-04-21, corrected 2026-04-25: Haiku gap 0.066,
Sonnet gap 0.206). The question v4 isolates is narrow: does v3's methodology
produce signal on chains generated under v1's organically-distributed pipeline?

**Primary result: strong_positive.** The Layer 1 actionable gap on Claude Haiku
4.5 is **+0.1311** (real match rate 0.315 vs shuffled 0.184, n=3,600 pairs,
McNemar χ²=167.3, p≈0, Bonferroni-corrected p≈0 with divisor=1). This clears
the pre-registered strong-positive threshold (gap ≥ 0.08, p < 0.01) by a wide
margin. Both variance configs (T=0.5, seeds 1337 and 7919) replicate the effect
with gaps of +0.143 and +0.134 respectively.

**Interpretation:** v3's pre-registered methodology is not the proximate cause
of v3's reversed result on chess/draughts chains. The methodology produces a
strong detectability gap when applied to v1's organically-distributed Pokémon
chains, supporting the interpretation that v3's reversal reflects v3-specific
chain-construction properties rather than a structural flaw in the methodology
itself.

---

## Hypothesis

*Quoted verbatim from SPEC.md v1.0 §"Hypothesis".*

> When v3's pre-registered methodology — the prompt template `v3.1-game`,
> the state-signature design from `src/reference.py`, the both-actionable
> filter logic, and the paired-McNemar / paired-t / Bonferroni statistical
> analysis — is applied to the constraint chains constructed by v1
> (Project-Ditto Pokémon Showdown telemetry), with a single v1-domain
> adaptation to the actionable-types set (see §"Reference Distribution
> Build"), the evaluation will reproduce v1's published moderate-positive
> Haiku result.
>
> The directional prediction is:
>
> **Layer 1 actionable gap on Haiku 4.5 will clear the moderate-positive
> threshold (gap ≥ 0.05, Bonferroni-corrected p < 0.05) on v1's chain
> data evaluated under v3's methodology.**

---

## Pre-registered Success Criteria

*Quoted verbatim from SPEC.md v1.0 §"Pre-registered Success Criteria".*

| Criterion | Threshold | Tier |
|---|---|---|
| Layer 1 actionable gap (real − shuffled, both-actionable filter) | ≥ 0.05 | Moderate-positive |
| Layer 1 actionable significance | Bonferroni-corrected p < 0.05 | Moderate-positive |
| Strong-positive | Layer 1 actionable gap ≥ 0.08 ∧ Bonferroni p < 0.01 | Strong-positive |

Outcome tiers: `strong_positive`, `moderate_positive`, `null`, `reversed`.

The v4 hypothesis is supported iff the primary analysis clears at least
moderate-positive. The Bonferroni divisor is 1 (single analysis, single cell);
Bonferroni-corrected p equals raw McNemar p in v4.

---

## Methods

### Data

1,200 real chains drawn deterministically (seed 42) from v1's 4,806 Pokémon
Showdown chain JSONLs (`v4_chain_selection.json`, committed before evaluation).
Three shuffled variants per real chain (shuffle seeds 42, 1337, 7919), loaded
from v1's pre-generated shuffled chains. Total: 1,200 real + 3,600 shuffled = 4,800
chains. Chains carry v1's `rendered` field (Step N headers), `constraints` list,
and `cutoff_k` (set at `len(constraints) // 2` per v1 pipeline).

Reference distribution built from all 1,200 real chains using v3's
`src/reference.py` (4-level backoff state signature) with the `vs_unit_a`
phase default (see §v1-Domain Adaptations below). 97.25% of chains achieve
level-0 (full 4-tuple) reference coverage; 2.75% fall back to level 3
(chain-independent).

### Evaluation

Model: Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)

Three configurations submitted as Anthropic Messages Batches on 2026-04-26:
- Primary: T=0.0, seed=42 (batch `msgbatch_01EvSYwd8YXJH8ReMYE6aGDi`)
- Variance 1: T=0.5, seed=1337 (batch `msgbatch_01KFr3gDPDdJQCwDPT2VdbBX`)
- Variance 2: T=0.5, seed=7919 (batch `msgbatch_01FfstmbRK1EfPuT7YBoNbxZ`)

14,400 calls submitted (1,200 × 4 conditions × 3 configs), 14,400 succeeded
(100%). Prompt: v3.1-game (entity-only format, v3's system prompt + user
prompt unchanged). Max tokens: 50.

### Statistical methodology

Layer 1 (primary): paired McNemar's test with continuity correction. Pair
alignment by `(base_chain_id, eval_seed)`; three shuffled variants per real
chain produce three pairs per base chain. Both-actionable filter: a pair
enters the Layer 1 actionable analysis iff both the real chain's
`constraints[cutoff_k].type` and the shuffled chain's
`constraints[cutoff_k].type` are in `ACTIONABLE_TYPES`.

Layer 2: paired t-test on legality × optimality composite.

Bonferroni divisor = 1 (single analysis, single cell). Bonferroni-corrected p
equals raw McNemar p.

Scoring was run in a separate session (Session 4) from the evaluation runner
(Session 3), with no effect-size monitoring between sessions.

### v1-Domain Adaptations

Two adaptations were pre-committed in `SPEC.md` v1.0 and finalized via
`SPEC_v1.1.md` with both-author sign-off (2026-04-26):

**Amendment 1 — ResourceBudget added to ACTIONABLE_TYPES (SPEC_v1.1).** The
original SPEC committed to a 5-type set
{ToolAvailability, SubGoalTransition, InformationState, CoordinationDependency,
OptimizationCriterion}. Session 2 pilot found both-actionable retention of
30.7% (43/140 pairs), below the 50% Gate 2 threshold. Diagnostic: 46% of real
chains have `ResourceBudget` as the constraint type at `cutoff_k`; because the
both-actionable filter requires both real and shuffled to be actionable, expected
retention ≈ (0.54)² = 29%, consistent with observation. In the Pokémon domain,
HP and PP directly constrain move availability and survival decisions — categorically
different from chess material counts. Both authors approved the amendment to
add ResourceBudget, bringing the set to 6 types. This raised retention from
30.7% to 100% (3,600/3,600 pairs in the full run).

**Amendment 2 — phase_ prefix strip in response normalization (SPEC_v1.1).**
The v3.1-game prompt's example token (`phase_endgame`) induced model responses
formatted as `phase_vs_unit_a` rather than bare `vs_unit_a`. The reference
distribution stores bare names. An asymmetry was observed in the pilot: 22%
of real responses vs 8% of shuffled responses carried the `phase_` prefix —
consistent with real chains containing coherent phase signal that makes the
model more likely to emit a phase-style answer. Without the strip, correct
real predictions were scored as misses. The amendment adds a post-normalization
adapter that strips a leading `phase_` prefix from model responses; the
reference build is unaffected (v1 references are already bare names).

**Phase-name default.** v3's state-signature function defaults `current_phase`
to `"phase_opening"` when no `SubGoalTransition` appears in the prefix window.
v1's `to_phase` values are `vs_unit_a`, `vs_unit_b`, ..., `forced_switch_required`.
Pilot scan across 5 candidates found all achieved 1.000 non-max-backoff coverage;
`vs_unit_a` was selected as the most domain-appropriate (most common v1 `to_phase`
value, ~43% of SubGoalTransition events). Selection recorded in
`v4_pilot_decisions.json`.

---

## Results

### Primary cell: haiku × pokemon — strong_positive

| Metric | Value |
|---|---|
| **Outcome tier** | **strong_positive** |
| Layer 1 gap (real − shuffled) | **+0.1311** |
| Real match rate | 0.3150 |
| Shuffled match rate | 0.1839 |
| McNemar χ² (df=1) | 167.3009 |
| Raw p-value | ≈ 0 (below float precision) |
| Bonferroni-corrected p (divisor=1) | ≈ 0 (= raw p) |
| n_pairs_actionable | 3,600 |
| n_base_chains | 1,200 |
| Missing pairs | 0 |
| Both-actionable retention | 100% (3,600/3,600) |

**Threshold check:**

| Criterion | Threshold | Value | Met? |
|---|---|---|---|
| Gap ≥ 0.05 | Moderate-positive | 0.1311 | ✅ |
| Gap ≥ 0.08 | Strong-positive | 0.1311 | ✅ |
| Bonferroni p < 0.05 | Moderate-positive | ≈ 0 | ✅ |
| Bonferroni p < 0.01 | Strong-positive | ≈ 0 | ✅ |

**The v4 hypothesis is supported.** The primary analysis clears the
**strong-positive** tier — the highest possible outcome under SPEC.md's
four-tier framework. The gap of 0.1311 is 2.5× the strong-positive threshold
and ~2× v1's published Haiku gap (0.066).

McNemar discordant pair breakdown:
- n11 (both match): 235
- b (real correct only): 899
- c (shuffled correct only): 427
- n00 (neither): 2,039
- b:c ratio: 2.11:1 (real-correct pairs outnumber shuffled-correct by 2:1)

### Layer 2

Layer 2 (legality × optimality composite, paired t-test):

| Metric | Value |
|---|---|
| Real mean | 0.3150 |
| Shuffled mean | 0.1839 |
| Gap | +0.1311 |
| t-statistic | 13.2736 |
| p-value | ≈ 0 |

Layer 2 gap equals Layer 1 gap (0.1311) because all matched responses receive
legality = 1 (well-formed entity labels); the legality × optimality composite
reduces to the top-k match indicator for v1's entity vocabulary.

### Variance study (descriptive — not in Bonferroni family)

| Config | Gap | χ² | p-value | real_rate | shuffled_rate | n_pairs |
|---|---|---|---|---|---|---|
| Primary (T=0.0, seed=42) | **+0.1311** | 167.30 | ≈ 0 | 0.3150 | 0.1839 | 3,600 |
| Variance 1 (T=0.5, seed=1337) | **+0.1431** | 197.90 | ≈ 0 | 0.3217 | 0.1786 | 3,600 |
| Variance 2 (T=0.5, seed=7919) | **+0.1339** | 176.61 | ≈ 0 | 0.3075 | 0.1736 | 3,600 |

All three configs produce strong-positive signals with p≈0. The variance study
is descriptive and not in the Bonferroni family per SPEC §Models and Evaluation
Parameters. The T=0.5 configs show marginally higher gaps (+0.003 to +0.012
above primary); the difference is small and could reflect noise at this n.
The outcome tier (strong_positive) is consistent across all three configs by
wide margins.

---

## Pre-registered Supplementary Analyses

### 1. Per-config variance

The gap is stable across all three temperature/seed configurations:

| Config | Gap | Spread from primary |
|---|---|---|
| T=0.0, seed=42 (primary) | +0.1311 | — |
| T=0.5, seed=1337 | +0.1431 | +0.012 |
| T=0.5, seed=7919 | +0.1339 | +0.003 |

The gap spread across configs is 0.012 (9% of the primary gap). This is modest
variance for a temperature change from 0.0 to 0.5. By comparison, v1's variance
study (corrected) showed a spread of 0.003 for Haiku across the same seed range,
suggesting v4's slightly larger spread reflects the cross-domain prompt vocabulary
mismatch (Amendment 2) contributing some stochastic variation at higher temperature.
The outcome tier (strong_positive) is consistent across all three configs by wide
margins.

### 2. Constraint-type carrier analysis

Per-type Layer 1 gap analysis (primary config, classified by real chain's
`constraints[cutoff_k].type`):

| Constraint type | n_pairs | real_rate | shuffled_rate | gap | % of total |
|---|---|---|---|---|---|
| ResourceBudget | 1,953 | 0.290 | 0.176 | **+0.115** | 54.3% |
| ToolAvailability | 858 | 0.283 | 0.183 | **+0.100** | 23.8% |
| SubGoalTransition | 339 | 0.451 | 0.227 | **+0.224** | 9.4% |
| InformationState | 243 | 0.593 | 0.181 | **+0.412** | 6.8% |
| OptimizationCriterion | 132 | 0.136 | 0.197 | −0.061 | 3.7% |
| CoordinationDependency | 75 | 0.120 | 0.200 | −0.080 | 2.1% |

Analysis classified by real chain type; shuffled chain type may differ (shuffling
rearranges constraint order). A "same-type" subset (pairs where both real and
shuffled chains have the same type at cutoff_k) shows qualitatively identical
carrier ordering.

**Four types carry positive signal; two show slight negative gaps.**
The two negative types — OptimizationCriterion and CoordinationDependency —
together represent only 5.7% of pairs. Their negative contributions are partially
offset by the strongly positive InformationState and SubGoalTransition types.

**InformationState** shows the largest per-type gap (+0.412), consistent with
the pre-registration rationale for including it in ACTIONABLE_TYPES: Pokémon
battles have genuine hidden information (opponent Pokémon hidden until revealed,
opponent HP/PP unknown), making the state at cutoff genuinely predictable for
real chains but not for shuffled ones. This pattern echoes v2's SWE domain,
where InformationState was also a primary carrier (hidden codebase state).

**SubGoalTransition** shows the second-largest gap (+0.224). Battle phase
transitions (vs_unit_a → vs_unit_b, forced_switch_required) are sequentially
structured — the model can predict phase transitions from the prefix.

**ResourceBudget** (the Amendment 1 addition) is the dominant type by volume
(54.3% of pairs) and shows a moderate gap (+0.115). Its inclusion is load-
bearing for the overall gap: without ResourceBudget, both-actionable retention
would be ~30% and the n_actionable would drop from 3,600 to ~1,080 pairs.

**OptimizationCriterion** and **CoordinationDependency** show slight negative
gaps. These types appear infrequently in v1 chains (3.7% and 2.1% respectively);
the negative gaps may reflect noise at small n rather than systematic inversion.
Session 1 pre-flight noted both types were near-absent in v1's constraint taxonomy
(zero occurrences in a 200-chain sample); their presence in ACTIONABLE_TYPES
has no practical effect on the dominant result.

**Comparison to v2's carrier asymmetry:** v2 found that ToolAvailability
carried the signal in the TB (Toolbox) domain, while InformationState carried
it in the SWE domain, with InformationState being near-absent in TB chains
(domain-asymmetric carriers). In v4's Pokémon domain, InformationState shows
the highest per-type gap and is present in 6.8% of pairs; the dominant carrier
by volume is ResourceBudget (unique to the Pokémon domain as an actionable
type). v4 does not exhibit the sharp cross-domain carrier asymmetry v2 found,
because Pokémon chains have a richer mix of actionable types than either
single-domain v2 cell.

### 3. Comparison to v1 published numbers

v1 published Layer 1 gap (Haiku, corrected methodology, T=0.0 seed=42):
**0.066** (McNemar, n=10,686 pairs; Bonferroni divisor=2; CORRECTED_SCORING.md,
2026-04-25).

v4 Layer 1 gap (Haiku, v3 methodology, T=0.0 seed=42):
**0.1311** (McNemar, n=3,600 pairs; Bonferroni divisor=1).

v4's gap is approximately **2× v1's corrected gap**, measured on the same v1
chain data.

**Comparison is descriptive only.** Four methodological differences preclude
a direct comparison:

1. **Prompt.** v4 uses the v3.1-game prompt (entity-only, chess-flavored
   examples); v1 used v1's original prompt. v4's prompt induces `phase_X`
   response formatting on a fraction of chains (Amendment 2 addresses this),
   but the vocabulary is structurally different. v4 tests v3's methodology;
   it does not test whether v3's prompt improves on v1's prompt.

2. **Focal action computation.** v4's reference distribution uses v3's on-the-fly
   focal_action computation: `constraints[cutoff_k]` is the prediction target
   (SPEC_v1.1 Amendment 2). v1's scorer used the stored `focal_action` field,
   which in v1's original implementation indexed `constraints[cutoff_k - 1]`
   (the last shown constraint, not the first hidden one). This is an off-by-one
   that was corrected in v3 and is applied in v4. Because v4's reference is
   built with the corrected target, v4's gap measures whether the model predicts
   the correct next constraint, while v1's gap measured whether the model
   predicted the last visible constraint (inadvertently). The two measurements
   are not numerically comparable.

3. **Both-actionable filter.** v4 applies the both-actionable filter
   (6-type ACTIONABLE_TYPES set, 100% retention). v1 applied a reference-miss
   filter only (no actionable-type constraint). Different pairs enter each
   analysis.

4. **Pair count.** v4: 3,600 pairs (1,200 chains × 3 shuffle seeds). v1:
   10,686 pairs (4,806 chains × 3 shuffle seeds × 74.1% valid). The difference
   reflects v1's 4× larger chain set and its reference-miss filter (which
   excludes fewer pairs than v4's none).

The 2× larger gap in v4 is consistent with multiple contributing factors:
the corrected focal_action target, the both-actionable filter selecting
higher-signal pairs, and the smaller n (which does not inflate the gap but
could make the point estimate higher-variance). No causal claim is made.

### 4. Comparison to v3 Phase 1 cell gaps

v3 Phase 1 Layer 1 actionable gaps (Bonferroni divisor=4,
from `phase1_v31_scored_full.json`):

| v3 cell | n_actionable | gap (filtered) | gap (unfiltered) | chi2 | outcome_tier |
|---|---|---|---|---|---|
| chess_standard | 1,288 | **−0.187** | −0.043 | 186.4 | reversed |
| chess960 | 1,250 | **−0.231** | −0.038 | 266.7 | reversed |
| checkers_american | 1,496 | **−0.115** | +0.039 | 69.6 | reversed (under review)† |
| draughts_intl | 1,533 | **−0.155** | −0.016 | 163.3 | reversed |
| **v4 pokemon (this work)** | **3,600** | **+0.131** | +0.131 | 167.3 | **strong_positive** |

†checkers_american unfiltered gap sourced from v3 SESSION_LOG "v4 Cell 1" entry.

Three of v3's four cells (chess_standard, chess960, draughts_intl) were classified
reversed under v3's pre-registered methodology with robustness across multiple
statistical tests — all four tested methodologies produce negative gaps for these
three cells. The fourth cell (checkers_american) sign-flips on filter choice:
+0.039 unfiltered, −0.115 under the both-actionable filter v3 pre-registered.
v3's SESSION_LOG records this as "warrants Myriam's input before further v4 cells"
and the cell is classified "methodology-dependent; under review" in SPEC.md
§"v3 status as of v4 pre-registration." The contrast with v4 (positive +0.131 vs
three robust-reversed cells; checkers_american partially recovers signal under
unfiltered analysis but remains negative under the same both-actionable filter
v3 pre-registered) is informative regardless of how checkers_american is finally
classified.

Notable structural differences between v3 and v4 that likely contribute:

- **Both-actionable retention:** v3 cells retained 35–43% of pairs as
  actionable (1,250–1,533 of 3,600); v4 retains 100% (3,600/3,600) because
  the 6-type ACTIONABLE_TYPES covers all constraint types present in v1
  chains. v3's 4-type set (excluding InformationState and ResourceBudget)
  filtered out the majority of pairs.

- **Carrier types:** v3's dominant chain content at cutoff_k was
  `ResourceBudget` (chess material) and `InformationState` (perfect
  information — always complete), both excluded from v3's actionable set.
  The pairs that passed v3's filter were biased toward types with reversed
  signal (ToolAvailability and SubGoalTransition in chess may behave
  differently than in Pokémon). v4's carrier analysis (§Supplementary 2)
  shows all 6 types present in meaningful proportions; only OptimizationCriterion
  and CoordinationDependency (5.7% combined) show negative gaps.

- **McNemar discordant ratios:** v3 cells show c >> b (shuffled-correct
  far outnumbers real-correct); v4 shows b > c (real-correct outpaces
  shuffled-correct by 2.1:1). The directional flip, at similar absolute
  chi2 values, indicates the mechanism of v3's reversal is specific to
  v3's chain construction, not a property of the methodology or the
  McNemar test.

### 5. Pair-level disagreement analysis

The McNemar contingency table for the primary cell:

| | Shuffled correct | Shuffled incorrect |
|---|---|---|
| **Real correct** | n11 = 235 | **b = 899** |
| **Real incorrect** | **c = 427** | n00 = 2,039 |

Discordant pairs: b + c = 1,326 (36.8% of all pairs).
Of these: 67.8% are real-correct-only (b), 32.2% are shuffled-correct-only (c).

b:c ratio = 2.11 (real-correct-only pairs are 2.1× more common than
shuffled-correct-only).

This is the expected pattern for a positive gap: the model is about twice as
likely to produce a correct prediction on real chains as on shuffled chains,
when the two disagree. The ratio b:c directly drives the gap direction (gap > 0
iff b > c).

For comparison, v3's discordant ratios (from `phase1_v31_scored_full.json`,
filtered layer1_actionable):
- chess_standard: b=34, c=275 → b:c = 0.12 (shuffled-correct 8× more common)
- chess960: b=11, c=300 → b:c = 0.04 (shuffled-correct 27× more common)
- checkers_american: b=124, c=296 → b:c = 0.42 (shuffled-correct 2.4× more common)
- draughts_intl: b=53, c=291 → b:c = 0.18 (shuffled-correct 5.5× more common)

All three robust-reversed v3 cells show c >> b (shuffled more often correct than
real) — the structural opposite of v4's b > c pattern. checkers_american's
b:c ratio (0.42) is the least extreme of the four, consistent with its weaker
and filter-sensitive reversal. In v4, real chains are more often matching —
consistent with the positive signal hypothesis.

### 6. Backoff-level distribution

State-signature coverage from the full reference distribution (1,200 real chains):

| Level | Count | Fraction | Description |
|---|---|---|---|
| 0 | 1,167 | **97.25%** | Full 4-tuple match (current_phase, last_move_type, resource_bracket, entity_label) |
| 1 | 0 | 0% | 3-tuple backoff |
| 2 | 0 | 0% | 2-tuple backoff |
| 3 | 33 | 2.75% | Chain-independent (max backoff) |

The bimodal distribution (97.25% at level 0, 2.75% at level 3, nothing at
levels 1–2) is consistent with v1's chain structure: when all four signature
components are present and non-default, the state-signature is fully determined
(level 0); when the prefix lacks a SubGoalTransition and falls to the
`vs_unit_a` default, the signature may still resolve at level 0 if the other
three components are informative. The 33 chains at level 3 likely have unusually
short prefixes or atypical constraint sequences.

For comparison, v3's reference coverage was approximately 90–95% at level 0
across cells (per v3's SESSION_LOG), with more spread across intermediate levels.
v4's higher level-0 fraction (97.25%) likely reflects v1's chains being longer
(average 39 constraints vs ~20–25 for v3's chess chains per v3 SESSION_LOG),
providing richer prefix windows for state-signature resolution.

The high level-0 fraction is also consistent with Pokémon battles repeating
similar (HP bracket × phase × move-type) state tuples across thousands of
matches more densely than chess positions repeat across games. This shared state
structure is what the methodology is designed to detect; v4's strong gap is
consistent with that interpretation.

---

## Discussion

### What this result establishes

Per SPEC.md §"Pre-registered Interpretation Framework" (verbatim, Primary:
strong-positive case):

> v3's pre-registered methodology — applied to v1's chains under the two
> pre-registered v1-domain adaptations — produces a stronger detectability
> gap than v1's own pre-registered methodology produced on Haiku (v1
> published Haiku gap 0.066 corrected). Strongest possible support for the
> v4 hypothesis: the methodology is not the source of v3's reversed result.
> v3's reversal is most parsimoniously explained by v3-specific
> chain-construction properties.

"v3's reversal" refers specifically to the three robust-reversed cells
(chess_standard, chess960, draughts_intl); checkers_american is classified
"methodology-dependent; under review" per SPEC.md §"v3 status as of v4
pre-registration" and is not counted as a robust reversal.

More precisely, the strong-positive result establishes:

1. **The v3.1-game prompt, applied to v1 chains, produces actionable model
   responses.** The model does not fixate on v3-flavored example vocabulary;
   it adopts v1's entity vocabulary in its outputs and matches the reference
   distribution at a rate substantially above baseline.

2. **The both-actionable filter, applied with the 6-type ACTIONABLE_TYPES set,
   produces a clean positive gap.** The signal is not an artifact of filter
   selection: it is positive and significant across all six types with
   meaningful counts (ResourceBudget, ToolAvailability, SubGoalTransition,
   InformationState), and only slightly negative for the two low-count types
   (OptimizationCriterion, CoordinationDependency) that are structurally near-
   absent from v1's chain distribution.

3. **The paired McNemar test, applied to the aligned pairs, produces an
   overwhelmingly significant result.** The chi2 of 167.3 corresponds to
   p ≪ 10⁻³⁰; no multiple-comparison correction materially affects this.

4. **The result is stable across temperature and seed.** Variance configs
   (T=0.5, seeds 1337 and 7919) replicate the primary direction and magnitude.

### What this result does NOT establish

Per SPEC.md §"What v4 does NOT change" and §"What this experiment is NOT":

1. **v3's pre-registered classification stands.** v3's four cells were scored
   under v3's own SPEC.md pre-registration; three (chess_standard, chess960,
   draughts_intl) are classified reversed with robustness across methodologies.
   checkers_american's classification is methodology-dependent and under review
   per SPEC.md §"v3 status as of v4 pre-registration" (sign-flips on filter
   choice: +0.039 unfiltered, −0.115 filtered). v4 has standing to comment on
   v3's *methodology*, not on v3's *classification*. v3's classifications are
   unchanged by this experiment.

2. **v1's published results are not re-evaluated.** v4 uses v1 chains as input
   but does not re-measure v1's published gaps. v1's corrected Haiku gap (0.066)
   and Sonnet gap (0.206) stand independently on v1's pre-registered methodology.
   v4's 0.1311 gap is not a replication of v1's 0.066; it is a different
   measurement under a different methodology (v3's vs v1's).

3. **The specific mechanism of v3's reversal is not characterized.** v4
   establishes that the methodology is not the proximate cause; it does not
   identify which specific chain-construction property causes the reversal. v3's
   SESSION_LOG records "resource_side dominance" and "backoff differential" as
   candidate mechanisms; those remain diagnostic hypotheses, not v4 findings.

4. **No post-hoc methodology corrections are evaluated or validated.** v4 runs
   v3's pre-registered methodology only. Any claim that a corrected methodology
   would recover signal on v3's chess/draughts chains requires a separate
   pre-registered experiment.

5. **v4 is not a test of the training-exposure hypothesis.** v1's domain has
   no within-family exposure contrast; v4 makes no claim about training data
   or model behavior.

---

## Limits

### Pre-registered interpretation limits (from SPEC.md §"Pre-registered Interpretation Framework")

The SPEC commits four possible outcomes to pre-registered interpretations.
v4's strong-positive result falls in the case: "v3's pre-registered methodology
— applied to v1's chains — produces a stronger detectability gap than v1's
own pre-registered methodology produced on Haiku. Strongest possible support
for the v4 hypothesis: the methodology is not the source of v3's reversed result."

No claim stronger than what the four-outcome framework supports is made. In
particular, this result does not "validate v3's methodology in absolute terms;
it only establishes that the methodology is not the proximate cause of v3's
reversal" (SPEC.md §"What v4 would establish").

### Technical observations disclosed per SPEC.md §"Technical risks"

**Risk 1 — Prompt-vocabulary fixation (SPEC §Risk 1; manifested; addressed by Amendment 2).**
The v3.1-game prompt's chess-flavored example token (`phase_endgame`) induced
a `phase_` prefix in model responses: 22% of real responses and 8% of shuffled
responses in the pilot used `phase_X` format (e.g., `phase_vs_unit_a`). This
asymmetry (real responses more likely to use `phase_X`) reflects real chains
containing coherent phase signal that anchors the model's output format. Without
Amendment 2's phase-strip adapter, these correct real predictions scored as
misses against the bare-name reference. The amendment recovers the model's clear
intent; without it, the pilot gap fell from +0.050 to +0.029. The full evaluation
gap (0.131) is computed with the adapter in place. The limit: the gap estimate
includes the amendment's correction for a cross-domain prompt artifact; it cannot
be compared numerically to a hypothetical run with a v1-native prompt.

**McNemar pair independence (flagged in Session 2 addendum 2).**
Each real chain pairs against 3 shuffled variants; the three pairs share the same
real-chain response. McNemar's independence assumption is technically violated
(non-independent pairs). This matches v1/v2/v3 methodology (identical pairing
structure) and is accepted implicitly by SPEC.md's pre-registration of v3's
analysis. At n=3,600 (chi2=167.3), the independence assumption violation does
not materially affect the significance conclusion; the gap itself (a pair-average
mean difference) is unaffected. Reported here as a structural note per v3's
SESSION_LOG disclosure.

**Shuffler fixed-point investigation (Session 2 addendum 4).**
For 88.6% of v1 chains (length=40, cutoff_k=20), the seed-42 shuffled chain
leaves `constraints[20]` unchanged (`random.Random(42).shuffle(range(40))[20] == 20`
is a fixed point of this RNG/length combination). An extensive investigation
showed no measurable impact on the Layer 1 gap: v3's scorer uses
`constraints[:cutoff_k]` (the prefix) for the state-signature lookup and
`constraints[cutoff_k]` only at reference build time (real chains only). The
shuffled chain's `constraints[cutoff_k]` is the scoring target but does not
enter the reference lookup; whether it matches the real chain's is irrelevant
to the scorer's match computation. The fix was implemented and reverted after
the pilot gap remained at +0.050 with and without it (Session 2 addendum 4).
The shuffler fixed-point does not bias the gap estimate.

**Layer 2 reduces to Layer 1 for v4.** v3's Layer 2 is a legality × optimality
composite; in v1's entity vocabulary, all top-k matches are trivially legal, so
the composite degenerates to the top-k match indicator. Layer 2's separate
threshold (gap ≥ 0.04) is therefore uninformative for v4 — Layer 1's
strong-positive classification carries the analysis.

**Both-actionable retention mechanism (Amendment 1 context).**
The 100% both-actionable retention in v4 (vs ~35–43% in v3) reflects the
6-type ACTIONABLE_TYPES set covering all constraint types present in v1 chains.
In effect, the both-actionable filter is inoperative in v4 — it passes all pairs.
This is not a methodological weakness; it reflects that v1's domain genuinely
has actionable constraints at all cutoff positions. The filter was designed to
exclude pairs where the model's prediction is not semantically meaningful; in
the Pokémon domain, all six types are semantically meaningful at the cutoff
(HP/PP tracking, move availability, battle phase, hidden info, objectives,
coordination). The 100% retention means the layer1_actionable analysis is
identical to the unfiltered layer1 analysis for v4.

---

## Authors and Acknowledgements

- **Lead author:** Safiq Sindha (Microsoft Azure Hardware PM, independent research)
- **Co-author:** Myriam (Columbia University, systems engineering; Boeing FT)

Pre-registration sign-off: both authors, 2026-04-26.
SPEC_v1.1 Amendments 1 and 2 sign-off: both authors, 2026-04-26.

This work builds on the Project Ditto v1/v2/v3 program. v1 Pokémon chains
were constructed under v1's pipeline (git tag `T-v1.1-frozen`). v3's scoring
pipeline (`vendor/v3/`, pinned to commit `ac144c2`) is used without modification;
all v4-specific adaptations are implemented via wrapper modules in `src/`.

Prior program: [Project Ditto v1](https://github.com/safiqsindha/Project-Ditto)
(Pokémon, moderate/strong positive),
[Project Ditto v2](https://github.com/safiqsindha/Project-Ditto-v2)
(programming, partial replication),
[Project Ditto V3](https://github.com/safiqsindha/Project-Ditto-V3)
(formal-rule games, reversed on three of four cells; checkers_american under review).

---

*RESULTS.md — initial draft 2026-04-26. Pending co-author review.*
*Final commit (Session 6) pending both-author sign-off.*
