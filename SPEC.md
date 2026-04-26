# Project Ditto v4 — Pre-Registration Specification

**Specification v1.0** · Pre-registration draft
Full PDF: `SPEC.pdf` (immutable — to be generated and committed after author review)

> **This document will be frozen before any chain construction begins.**
> Thresholds, methodology, and analysis plan are committed here before
> implementation. Any methodology change after pre-registration commit
> invalidates the pre-registration and requires a new dated spec. Pre-
> registration discipline is matched to v3's level (`SPEC.md` + immutable
> `SPEC.pdf` + dated supplements for any post-commit amendments).

---

## Hypothesis (precisely scoped)

When v3's pre-registered methodology — the prompt template `v3.1-game`,
the state-signature design from `src/reference.py`, the both-actionable
filter logic, and the paired-McNemar / paired-t / Bonferroni statistical
analysis — is applied to the constraint chains constructed by v1
(Project-Ditto Pokémon Showdown telemetry), with a single v1-domain
adaptation to the actionable-types set (see §"Reference Distribution
Build"), the evaluation will reproduce v1's published moderate-positive
Haiku result.

The directional prediction is:

> **Layer 1 actionable gap on Haiku 4.5 will clear the moderate-positive
> threshold (gap ≥ 0.05, Bonferroni-corrected p < 0.05) on v1's chain
> data evaluated under v3's methodology.**

This is a single-cell methodology characterization study. It is not a
replication of v1, a re-analysis of v3, a transfer experiment, or a test
of the original training-exposure hypothesis. The question it isolates is
narrow and specific:

> *Does v3's pre-registered methodology produce signal on chains
> generated under v1's organically-distributed construction process?*

If yes (Haiku Layer 1 actionable gap clears moderate-positive on v1
chains under v3 methodology): v3's pre-registered methodology is sound;
v3's reversed result on three of its four formal-game cells is most
likely attributable to v3-specific chain-construction properties rather
than to the methodology itself.

If no (the gap fails to clear, or reverses): v3's pre-registered
methodology has issues that affect even chains v1 originally showed
strong signal on. The methodology requires more substantive review than
the audit-pattern fixes already applied via `SPEC_v1.1.md`.

This is the only question v4 answers. v4 does not test post-hoc
corrections to v3's methodology, does not characterize the four-outcome
joint behavior of pre-registered and corrected methodologies, and does
not produce statistical evidence supporting any specific corrected-
methodology design. Those questions remain open after v4 and require
separate experiments to address.

---

## What this experiment is NOT

This list is exhaustive on what v4 can and cannot conclude. The list
is load-bearing for interpretation; deviations from it after pre-
registration commit are spec amendments.

- **NOT a replication of v1.** v1's published numbers stand independently
  on v1's pre-registered methodology. v4 does not validate v1's
  publication; v1 is treated as a fixed reference point with a known
  outcome (Haiku gap 0.066 corrected, Sonnet gap 0.206 corrected,
  per `CORRECTED_SCORING.md` in the v1 repo).

- **NOT a re-analysis of v3.** v3's pre-registered classification
  (`reversed` on chess_standard, chess960, draughts_intl; outcome on
  checkers_american is methodology-sensitive — see §"v3 status as of
  v4 pre-registration" below) is unchanged regardless of v4's outcome.
  v4 does not have the standing to retroactively reclassify v3.

- **NOT a transfer test.** No claim is made about whether v3's models
  trained on v3's data, whether v1's models trained on v1's data, or
  about cross-domain generalization of any abstraction.

- **NOT a test of the training-exposure hypothesis.** v3's hypothesis
  was that training-data exposure compresses the real-vs-shuffled
  detectability gap (with chess_standard / chess960 and
  checkers_american / draughts_intl as within-family contrasts). v4
  does not test this hypothesis. v1's domain has no within-family
  exposure contrast.

- **NOT a validation of any post-hoc methodology corrections.** v4 runs
  v3's pre-registered methodology only. No comparison to corrected
  variants is performed. Any claim about whether post-hoc corrections
  to v3's methodology recover signal is out of scope; it requires a
  separate experiment with a corrected methodology specified in advance.

- **NOT additive to v1's findings.** v4 produces no new claim about
  Pokémon, about v1's models, or about v1's prompt format. v4's
  contribution is purely diagnostic: characterizing v3's methodology
  on chains of known structure.

- **NOT a multi-cell experiment.** A single source (v1 Pokémon chains)
  is evaluated. There is no within-family contrast and no Bonferroni
  family across cells.

---

## Why we are running this experiment now

This section describes the program context honestly so that a future
reader can understand v4's place in the program.

**v1** (Project-Ditto, Pokémon Showdown telemetry; published 2026-04-21,
methodology correction 2026-04-25): pre-registered methodology produced
strong-positive on Sonnet (gap 0.206 corrected) and moderate-positive on
Haiku (gap 0.066 corrected). Both findings cleared the corrected paired-
test methodology with extreme statistical margins.

**v2** (Project-Ditto-v2, programming-task agent trajectories; published
2026-04-25): pre-registered methodology partially replicated v1's effect.
Layer 2 cleared on all four model × source cells; Layer 1 actionable on
Haiku-TB cleared the moderate-positive threshold (gap 0.0801, Bonferroni-
corrected p = 0.0116). The other three cells did not clear. Direction
positive in 7 of 8 cells.

**v3** (Project-Ditto-V3, formal-rule games; pre-registered 2026-04-25,
Phase 1 evaluated 2026-04-25, scored shortly after): under v3's pre-
registered methodology with the SPEC_v1.1 amendments applied (entity-
only prompt v3.1-game, focal_action cutoff fix, scorer output structure
separation), Phase 1 Haiku produced negative Layer 1 actionable gaps on
three of four cells (chess_standard −0.187, chess960 −0.231,
draughts_intl −0.155). The fourth cell, checkers_american, returned a
positive unfiltered gap (+0.039) that flipped to negative under the
both-actionable filter (−0.115); see v3 SESSION_LOG.md "v4 Cell 1 —
Statistical methodology robustness" for the full per-methodology table.

A v4 Cell 1 analysis on a non-merged branch in v3's repository
characterized the robustness of v3's outcome to four statistical
methodology choices; that work is referenced in §"Relationship to v4
Cell 1" below. Diagnostic mechanisms identified during v3 post-hoc
analysis (resource_side dominance and backoff differential are recorded
in v3's SESSION_LOG; further mechanism analysis if any is not yet
documented in materials available at v4 pre-registration time) trace to
v3-specific design choices in the formal-game T-code.

The question v4 isolates is whether v3's *methodology* — independent of
v3's *chains* — produces the predicted detectability gap on chains
already known to carry the relevant structure under a different
pre-registered methodology. If methodology-on-clean-chains succeeds, the
program's inferential picture stabilizes around chain-construction as
the source of v3's reversal. If methodology-on-clean-chains fails, the
methodology requires more substantive review.

---

## v3 status as of v4 pre-registration

This subsection records v3's status at the time of v4 pre-registration
to anchor v4's interpretation framework. Numbers are sourced from v3's
SESSION_LOG.md "v4 Cell 1 — Statistical methodology robustness" entry
(2026-04-26).

| v3 cell | Pre-registered methodology gap | v3 classification |
|---|---:|---|
| chess_standard | −0.187 | reversed (robust across 4 methodologies) |
| chess960 | −0.231 | reversed (robust across 4 methodologies) |
| checkers_american | −0.115 (filtered) / +0.039 (unfiltered) | methodology-dependent; under review |
| draughts_intl | −0.155 | reversed (filter+Bonferroni-dependent significance) |

v3's pre-registered classification per its SPEC.md is reversed on three
of four cells under the pre-registered methodology, with checkers_american
flagged for co-author review. v4's analysis does not depend on the
disposition of checkers_american; v4 references v3 only as the
methodology source under test.

---

## Pre-registered Success Criteria

### Per-cell thresholds (single cell: Haiku × v1 Pokémon chains)

| Criterion | Threshold | Tier |
|-----------|-----------|------|
| Layer 1 actionable gap (real − shuffled, both-actionable filter) | ≥ 0.05 | Moderate-positive |
| Layer 1 actionable significance | Bonferroni-corrected p < 0.05 | Moderate-positive |
| Layer 2 gap (legality × optimality composite) | ≥ 0.04 | Layer 2 confirmation |
| Layer 2 significance | Bonferroni-corrected p < 0.05 | Layer 2 confirmation |
| Strong-positive | Layer 1 actionable gap ≥ 0.08 ∧ Bonferroni p < 0.01 | Strong-positive |

These thresholds match v3's SPEC.md exactly. The Bonferroni divisor for
v4 is **1** — a single analysis (v3's pre-registered methodology) on a
single cell (Haiku × v1 Pokémon chains). Bonferroni correction with
divisor 1 is equivalent to no correction; the column is retained in the
results output for cross-experiment comparability with v1/v2/v3 reporting
conventions but applies no actual correction. The "Bonferroni-corrected
p" reported in §"Pre-registered Success Criteria" is therefore identical
to the raw McNemar p in v4's output.

Outcome tiers (consistent with v1, v2, v3):
`strong_positive`, `moderate_positive`, `weak_mixed`, `null`, `reversed`.

### Threshold for "v3 methodology works on clean chains"

The v4 hypothesis is supported iff the **primary** analysis (v3's pre-
registered methodology) clears at least the moderate-positive threshold.
Strong-positive on the primary is a stronger form of support but is not
required for v4 to be informative.

A null result on the primary (gap not clearing 0.05 or p not clearing
Bonferroni 0.05) refutes the v4 hypothesis. A reversed result on the
primary (gap negative + Bonferroni-significant) is the strongest form of
refutation and would imply that v3's methodology produces inversion even
on chains v1 originally showed strong signal on.

---

## Pre-registered Interpretation Framework

The four outcomes below are committed before any data collection. They
correspond to the four possible classifications of the primary analysis
result. v4 runs a single primary analysis (v3's pre-registered
methodology) on a single cell (Haiku × v1 Pokémon chains). There is no
secondary analysis and no joint interpretation across analyses.

### Four-outcome interpretation

**Primary: strong-positive** (Layer 1 actionable gap ≥ 0.08, p < 0.01).
v3's pre-registered methodology — applied to v1's chains under the
two pre-registered v1-domain adaptations — produces a stronger
detectability gap than v1's own pre-registered methodology produced on
Haiku (v1 published Haiku gap 0.066 corrected). Strongest possible
support for the v4 hypothesis: the methodology is not the source of
v3's reversed result. v3's reversal is most parsimoniously explained
by v3-specific chain-construction properties.

**Primary: moderate-positive** (Layer 1 actionable gap ≥ 0.05, p < 0.05).
v3's pre-registered methodology produces a detectability gap on v1
chains in the same tier as v1's own published Haiku result. Supports
the v4 hypothesis. v3's reversal is plausibly attributable to chain
construction rather than methodology.

**Primary: null** (gap not clearing 0.05, or p not clearing 0.05; gap
direction not specifically negative). v3's pre-registered methodology
fails to detect signal on chains v1 originally classified as
moderate-positive. Refutes the v4 hypothesis. The methodology has
issues affecting chains beyond v3's domain. Possible explanations: (a)
the SPEC_v1.1 amendments to v3 (entity-only prompt, focal_action fix,
scorer output structure) are insufficient to rehabilitate the
methodology; (b) v1's signal is specific to v1's prompt/scorer
combination and does not survive the v3.1-game prompt reformulation
even with chain content held constant. v4 alone cannot distinguish
(a) from (b); a follow-up experiment with v3 methodology + v1 prompt,
or v1 methodology + v3.1 prompt, would be required to disambiguate.

**Primary: reversed** (gap negative, Bonferroni-corrected p < 0.05 in
the negative direction). Strongest possible refutation of the v4
hypothesis. v3's pre-registered methodology produces *inverted* signal
on chains v1 classified as moderate-positive. The methodology has
structural issues that affect even chains of known good structure. A
substantial review of v3's scoring pipeline is required before any
follow-on experiment.

### What v4 does NOT change

**v3's pre-registered classification stands.** Regardless of v4's
outcome, v3's pre-registered classification per its own SPEC.md is
unchanged. v4 has standing to comment on v3's *methodology*, not on
v3's *classification* — those are different objects.

**v1's published numbers stand.** v4 uses v1 chains as input but does
not re-evaluate v1's published gaps. v1's results are a fixed reference
point; v4's outcome carries no implication for v1's standing.

---

## Models and Evaluation Parameters

| Parameter | Value |
|-----------|-------|
| Models | Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) — only model |
| Primary config | Temperature 0.0, seed 42 |
| Variance study | T=0.5, seed 1337; T=0.5, seed 7919 |
| Max tokens | 50 |
| Cutoff K | `len(constraints) // 2` (matches v1 and v3 — `max(1, …)` floor applied per `reference.py` defensive logic) |
| Prompt version | v3.1-game (verbatim from v3 `src/prompt_builder.py`; system + user prompts unchanged) |
| API | Anthropic Messages Batches (50% cost reduction) |
| Action normalization | Full normalization (case, punctuation, whitespace, word order) — same as v1/v2/v3 |

### Model selection rationale (Haiku-only)

v4 is a single-cell methodology characterization study answering a
binary question. v3's Phase 1 ran Haiku to gate the more expensive
Sonnet phase. v4 mirrors v3's Phase 1 structure. Sonnet is not run
because:

- The binary "does v3's methodology produce signal on clean chains?"
  question is fully answerable with Haiku.
- Adding Sonnet doubles cost and runtime without changing what v4
  can conclude.
- v1 published Haiku gap 0.066 (moderate-positive). v4 tests whether v3
  methodology reproduces *that* number's tier, not the larger Sonnet
  effect. The Haiku comparison is the directly relevant one.

If v4 primary returns null or reversed, a follow-up Sonnet evaluation
may be warranted — but that is a separate experiment, not part of v4's
pre-registration.

### Prompt portability check (verbatim use)

v3.1-game prompt body:

```
Given the state above, what is the most likely entity (resource, tool,
phase, or coordination tag) at step {cutoff_k + 1}?
Output only a single token like piece_A, chain_B, formation_C,
phase_endgame, or progress_remaining.
No verbs, no explanation.
```

System prompt: v3's `SYSTEM_PROMPT` from `src/prompt_builder.py`
(framing: "sequential decision process", domain-blind throughout).

The prompt examples reference `piece_A`, `chain_B`, `formation_C`,
`phase_endgame`, `progress_remaining` — these are v3-domain entity
labels. They are retained **unchanged** in v4. Rationale: v4's
hypothesis is that v3's *methodology unchanged* produces signal on
clean chains. Modifying the prompt examples for Pokémon would change
the methodology under test. The model receives v3-flavored entity
example labels paired with a chain prefix containing v1-flavored entity
labels (`unit_A`, `action_3`, etc.); whether the model's output
distribution adjusts to the prefix's vocabulary is part of what v4 is
implicitly testing. If pilot inspection (§"Phase structure") shows
near-zero match rate driven by example-vocabulary fixation rather than
a real methodology issue, this is a pre-pilot risk to flag, not a
post-pilot spec amendment.

The `sequential decision process` framing in the system prompt is
fully domain-blind and applies without modification.

---

## Data Sources (committed — will not change after freeze)

### Primary source: v1 Pokémon chains

| Property | Value |
|---|---|
| Source | `chains/real/` directory of v1 repo (Project-Ditto, Pokémon Showdown telemetry) |
| Chain construction | v1 pipeline frozen at git tag `T-v1.1-frozen` (per v1 CLAUDE.md) |
| Chain schema | v1 JSONL: per-file chain dict with `constraints` (list of constraint dicts), `cutoff_k`, `chain_id`, etc. (per v1 CLAUDE.md and confirmed against v1 reference.py interface) |
| Per-cell sample target | 1,200 real chains |
| Shuffled variants | 3 per real chain at seeds 42, 1337, 7919 (v1 default; matches v3's shuffler) |

### Sample size: 1,200 v1 Pokémon chains

Matches v3's per-cell sample target. Power calculations from v3 SPEC.md
§"Sample Size & Power" carry over and are **stronger** at v4's smaller
Bonferroni divisor: at α = 0.05 (v4 divisor = 1) with n = 1,000 paired
evaluations and v2-calibrated discordant rates, per-cell power for
moderate-positive (gap ≥ 0.05) exceeds the ~94% v3 calculated at α =
0.0125 (v3 Phase 1 divisor = 4). Power for strong-positive remains
≥ 99%. v4 is generously powered for the binary hypothesis.

The 1,200-chain target assumes v1's chains achieve approximately the
same both-actionable-retention rate v3 calibrated against (~83% retention
= ~1,000 paired evaluations after filter). v1's chain set is large
enough that 1,200 chains can be sampled without re-running v1's
acquisition pipeline (v1 reports having generated 4,806 real chains
across p1+p2 perspectives per `CORRECTED_SCORING.md` data structure).

Sampling is deterministic at seed 42 from v1's available chains, with
the seed and the ordered list of selected `chain_id`s recorded in
`v4_chain_selection.json` and committed before any evaluation runs.

### What is NOT used

- v1's reference distribution (`reference_dist.pkl`) is **not used**.
  v4 builds a fresh reference distribution from v1's chains using v3's
  `src/reference.py` (with the v1-domain adaptations described in
  §"Reference Distribution Build"). Using v1's own reference would mean
  evaluating v1 chains under a hybrid methodology, defeating v4's
  test-v3-methodology framing.
- v1's prompt template, scorer, runner, T-code are not used. v4 uses
  v3's versions throughout.
- v2's modules and chains are not used.

---

## Reference Distribution Build

This section implements the original prompt's flagged "biggest risk"
explicitly. The ground truth is that v1's StateSignature
(`(active_pair, hp_brackets, status_effects, field_conditions,
turn_bucket)`) and v3's StateSignature
(`(current_phase, last_move_type, resource_bracket, entity_label)` at
level 0) have different shapes. v4 must choose between using v1's or
v3's signature design. The pre-committed choice is:

> **v4 uses v3's StateSignature design with the two v1-domain adaptations
> documented below (phase-name default; actionable types include
> InformationState), building a fresh reference distribution from v1
> chains.** The signature *structure* (4-level backoff,
> `(current_phase, last_move_type, resource_bracket, entity_label)`,
> `extract_entity_from_constraint` logic) is unchanged from v3.

### v3's `src/reference.py` is largely domain-blind

Inspection of v3's `src/reference.py` confirms that its components are
mostly domain-blind by design:

| Component | Source | v1 chain compatibility |
|---|---|---|
| `current_phase` | last `SubGoalTransition.to_phase` in prefix; defaults to `"phase_opening"` | v1 chains have `SubGoalTransition` constraints. Default may need adaptation — see below. |
| `last_move_type` | `constraint_type` of `constraints[cutoff_k - 1]` (last shown) | Domain-blind: any constraint type name. v1's chains use the same six types. |
| `resource_bracket` | bracket of last `ResourceBudget.amount` (0–4 buckets) | Domain-blind: `_resource_bracket` operates on a normalized float. v1 chains have `ResourceBudget` constraints with `amount` fields. |
| `entity_label` | `extract_entity_from_constraint(constraints[cutoff_k])` | Domain-blind: returns whatever lowercased abstract label the constraint dict carries (e.g. v3's `piece_g`, v1's `unit_a`). |

`extract_entity_from_constraint` itself is fully domain-blind; it reads
known fields off six constraint types and lowercases the result. v1's
constraints carry the same fields (`tool`, `to_phase`, `resource`,
`dependency`, `objective`, `observable_added`).

### Required adaptation: phase-name default

v3's `current_phase` defaults to the string `"phase_opening"` when no
`SubGoalTransition` appears in the prefix window. This default is
v3-specific (chess/checkers phase taxonomy: opening / middlegame /
endgame). v1's `to_phase` taxonomy is different (Pokémon battle phases
emitted by v1's T-code).

**Adaptation:** v4 retains v3's `extract_state_signature` function
unchanged in structure, but the **default phase string** is selected
empirically from the pilot 50-chain set. Pre-registration commits to:
*the default value maximizing level-0/1 reference coverage on the
pilot set, recorded in `v4_chain_selection.json` before the full
evaluation runs.* If multiple candidate defaults tie within 0.5
percentage points of coverage, the lead author selects (and records
the selection in the pilot session log). The default value is a
*parameter*, not a methodology change — v3's `reference.py` itself
documents this default as `# Defensive default`.

### Required adaptation: actionable types include InformationState

v3's both-actionable filter excludes `InformationState` because formal
games are perfect-information. v1's domain (Pokémon battles) has
meaningful `InformationState` — opponent Pokémon are hidden until
revealed; opponent HP is bucketed; opponent moves are hidden until
used. Excluding `InformationState` from v4's actionable set would
remove a substantial fraction of v1's actionable chain content and
materially distort the test.

**Pre-committed adaptation:** v4's `ACTIONABLE_TYPES` set is:

```python
{
  "ToolAvailability",
  "SubGoalTransition",
  "InformationState",   # added (v1-domain — meaningful hidden info)
  "CoordinationDependency",
  "OptimizationCriterion",
}
```

This is **five** actionable types. v3 uses four (excludes both
`InformationState` and `ResourceBudget`). v1's published methodology
did not apply an actionable-types filter at all (per v1
`CORRECTED_SCORING.md`: "v1's filter rule (reference-miss exclusion)
is preserved... v2's actionable-constraint-type filter is **not**
imported; v1 had no such filter"). v4's five-type set is the v3
filter logic with `InformationState` re-included for v1's domain.
`ResourceBudget` remains excluded as non-actionable, matching v2's
and v3's design choice for material-counting / budget constraints
that the model cannot meaningfully predict in advance.

This is a v1-domain adaptation, **not** a methodology change in v3's
sense. The pre-registered scorer logic operates on whatever set is
configured for `ACTIONABLE_TYPES`; v4 merely configures the set
appropriate to v1's domain. The adaptation is documented here to be
explicit; the SPEC commits to it.

### Coverage target

v3 SPEC.md §"Pipeline Reuse from v1/v2" specifies ≥ 90% non-max-backoff
coverage. v4 retains this target. Pilot validation (§"Phase structure")
verifies coverage before the full evaluation runs.

---

## Pre-registered Statistical Methodology

### Primary (and only) analysis: v3's pre-registered methodology with v1-domain adaptations

Layer 1 (primary): paired McNemar's test with continuity correction,
both-actionable filter (with `ACTIONABLE_TYPES` set per §"Reference
Distribution Build" above). Bonferroni divisor = 1 (single analysis;
no correction applied). The threshold is therefore raw McNemar p < 0.05
for moderate-positive and raw McNemar p < 0.01 for strong-positive.

Layer 2: paired t-test (`scipy.stats.ttest_rel`) on legality × optimality
composite scores. Same Bonferroni treatment (divisor = 1).

Pair alignment by `(base_chain_id, eval_seed)` — model dimension is
fixed (Haiku only). Three shuffled variants per real chain (seeds 42,
1337, 7919) produce three pairs per real evaluation, matching v3's
`(base_chain_id, model, eval_seed) × (shuffled_chain = base_chain_id +
"_shuffled_" + shuffle_seed)` pair structure.

Pairs missing either real or shuffled result are reported and excluded.
Gap is computed as `real_match_rate − shuffled_match_rate` over all
included pairs (matching v2/v3 estimand convention).

The scorer is v3's `src/scorer.py` (per `SPEC_v1.1.md` Amendment 3,
producing the `primary_cells` / `variance_study` separation), with two
configuration changes:

1. `SOURCES = ["pokemon"]` (single cell)
2. `ACTIONABLE_TYPES` includes `InformationState` (5-type set per
   §"Reference Distribution Build")

The scorer's statistical logic is unchanged. The per-cell threshold
classification logic is unchanged. The output schema's `primary_cells`
key contains a single entry (`haiku::pokemon`); the `variance_study`
key contains two entries (`haiku::pokemon::T0.5_seed1337`,
`haiku::pokemon::T0.5_seed7919`).

### No secondary analysis

v4 does not include a comparison to a post-hoc-corrected methodology.
This is a deliberate scope decision recorded at pre-registration:

- The corrected methodology referenced in v4's planning prompt
  ("downweighted reference + matched-backoff stratification + leave-
  one-out, as developed in v3's Phase A and Path 1 analyses") is not
  implementable from documents available at v4 pre-registration time.
- Including a secondary analysis whose specification is incomplete
  would not be a legitimate pre-registration.
- Even if the secondary methodology were specifiable, v4 could not
  *validate* it (the corrections were designed against v3 data; v1
  data observing them work would be consistent with the diagnosis but
  would not independently establish the corrections' validity).

A separate experiment with a fully-specified corrected methodology,
pre-registered against data that was not used in the methodology's
design, would be required to produce evidence about post-hoc
corrections. v4 does not attempt that.

---

## Phase Structure

v4 has no formal gates between phases (the experiment is small and the
question is binary). The phase structure below is a sequencing aid, not
a gating mechanism.

### Phase 0 — Pre-registration commit

- Author review of this SPEC.md (lead + co-author)
- Verification of v1 chain mirror in `data/v1_chains_mirror/` and
  commit of the deterministic 1,200-chain selection at seed 42
  (recorded in `v4_chain_selection.json`)
- Verification of v3 git submodule pinned to `T-code-game-v1.0-frozen`
- Generation and commit of `SPEC.pdf` from finalized `SPEC.md`
- Pre-registration commit message: "Pre-registration commit —
  thresholds and methodology frozen"
- Both-author sign-off recorded in commit history (matching v3's
  protocol)

### Phase 1 — Pilot validation (50 chains)

50 v1 chains evaluated end-to-end under the v3 methodology. Pilot
verifies:

- v1 chain JSONLs load correctly under v3's chain-handling code
  (compatibility check)
- Reference distribution build on v1 chains achieves ≥ 90% non-max-
  backoff coverage (matching v3's target); flag if below
- v3.1-game prompt produces parseable single-token responses on v1
  chains at non-zero match rate (sanity check; not an effect-size
  measurement)
- Both-actionable filter retention rate is in the expected range
  (~60–85%); flag if outside

Pilot pass criteria: load OK; coverage ≥ 90%; non-zero match rate; both-
actionable retention ≥ 50%.

Pilot fail response: pause for author review. Likely failure modes:
phase-name default mismatch (adjust per §"Reference Distribution Build"),
prompt-vocabulary fixation (flagged as a limit on v4's interpretation,
not a spec amendment), chain-format incompatibility (technical fix).

### Phase 2 — Full evaluation

1,200 v1 chains × (1 real + 3 shuffled variants) × 3 evaluation configs
(T=0.0 seed=42; T=0.5 seed=1337; T=0.5 seed=7919) = **14,400 calls**.
This matches v3's per-cell call volume (v3 ran 57,600 calls across 4
cells = 14,400 per cell).

Anthropic Messages Batches API. Cost estimate: $5–10 (Haiku batch rate
of $0.40/M input + $2.00/M output; per v3 Session 10's actual cost of
~$17 on 57,600 calls scaled to v4's 14,400). The original planning
prompt's $20–30 estimate was conservative; v4 should come in well
under it.

### Phase 3 — Scoring

Scorer is v3's `src/scorer.py` (per SPEC_v1.1 Amendment 3 output
structure) with `SOURCES = ["pokemon"]` and the v1-domain
`ACTIONABLE_TYPES` set. Scoring runs in a separate session from
evaluation, on blinded inputs (model identity, condition, seed stripped
before scoring), matching v3's blinded-scorer protocol.

Output: `results/v4_scored.json` containing per-config per-condition
gap, McNemar χ², raw p, Bonferroni-corrected p, both-actionable
retention rate, n_pairs, and outcome tier classification per the
pre-registered thresholds.

### Phase 4 — Write-up

Single results document `RESULTS.md` matching v3's RESULTS structure:
abstract; pre-registration link; threshold check table; primary +
secondary outcome cells with interpretation per the four-outcome
framework; supplementary analyses (per-config variance; carrier
analysis); discussion of limits; explicit statement that v4 does not
change v3's pre-registered classification.

Co-author review before commit (matches v3 Gate 8 protocol).

---

## Pre-registered Supplementary Analyses

1. **Per-config variance study** — three temperature/seed configs as
   above, reported as supplementary stability characterization. Not in
   the primary Bonferroni family, matching v3 SPEC.md §"Pre-registered
   Supplementary Analyses" item 1.

2. **Constraint-type carrier analysis** — which actionable constraint
   types carry the signal (or its inversion) on v1 chains under v3
   methodology. Compares against v2's TB / SWE carrier asymmetry
   finding (`ToolAvailability` for TB, `InformationState` for SWE) and
   v1's per-type breakdown (which is in v1's results but was not the
   primary metric).

3. **Comparison to v1 published numbers** — v4 Haiku gap on v1 chains
   under v3 methodology, vs v1's published Haiku gap (0.066 corrected),
   vs v3's Phase 1 Haiku per-cell gaps (sourced from v3's
   `results/phase1_v31_scored_full.json` — same data v4 Cell 1's
   robustness analysis operated on, but used here only as descriptive
   reference points). Descriptive only; not a hypothesis test.

4. **Pair-level disagreement analysis** — for the small expected
   number of cases where v4 primary and v1's published methodology
   disagree at the chain level (real-correct under one and not the
   other), characterize the disagreement to support
   §"Constraint-type carrier analysis".

5. **Backoff-level distribution** — match rate per backoff level
   (0–3) for v1 chains under v4. Comparison to v3's per-cell backoff
   distributions (per v3's reference coverage report) is descriptive.
   This analysis is *deliberately not* a hypothesis test of the
   "backoff differential" mechanism; testing that mechanism on v4
   data would require a Phase A-style diagnostic, which is out of
   scope for v4.

---

## Relationship to v4 Cell 1 (statistical robustness analysis)

v3's SESSION_LOG.md contains an entry "v4 Cell 1 — Statistical
methodology robustness — 2026-04-26" describing a study on a non-
merged branch (`claude/v4-cell-1-statistical-robustness`) that applied
four statistical methodologies to v3's existing primary-config response
data. This SPEC describes the experiment that has been called
**v4 Cell 2** in informal discussion: the v1-Pokémon-chains methodology
characterization.

The two studies are independent:

- v4 Cell 1 holds v3's chains constant and varies the statistical
  methodology. It characterizes how robust v3's `reversed` outcome is
  to test-choice within v3's data.
- v4 Cell 2 (this SPEC) holds the methodology constant (v3's pre-
  registered methodology) and varies the chain construction (v3's
  formal-game chains → v1's Pokémon chains). It characterizes whether
  v3's methodology produces signal on chains generated under different,
  organically-distributed construction.

Both v4 cells inform the chain-vs-methodology question from different
sides. Neither alone is sufficient; together they triangulate.

This SPEC does not commit to merging the v4 Cell 1 branch. That
decision is independent of v4 Cell 2 and depends on co-author review
of Cell 1's output (per v3 SESSION_LOG.md's standing recommendation).

---

## What v4 would establish

### If primary clears moderate-positive

> "v3's pre-registered methodology — applied to chains constructed
> under v1's organically-distributed pipeline, with the two
> pre-registered v1-domain adaptations (phase-name default;
> actionable types include `InformationState`) — produces a
> real-vs-shuffled detectability gap consistent with v1's own
> published Haiku result. This is consistent with the
> interpretation that v3's reversed result on three of four formal-
> game cells reflects v3-specific chain-construction properties
> (resource_side dominance and backoff differential per v3's
> SESSION_LOG; further mechanisms if any) rather than a structural
> problem with the v3 statistical methodology."

This does not validate v3's methodology in absolute terms; it only
establishes that the methodology is not the proximate cause of v3's
reversal.

### If primary returns null or reversed

> "v3's pre-registered methodology fails to produce signal — or
> produces inverted signal — on chains v1's pre-registered
> methodology classified as moderate-positive. This implies the
> methodology has issues affecting chains beyond v3's domain, and the
> SPEC_v1.1 amendments (prompt vocabulary alignment, focal_action
> off-by-one, scorer output structure) are insufficient to fully
> rehabilitate it. v5 (or a v3 SPEC v1.2) requires a more substantial
> methodology review than the audit-pattern fixes already applied."

This does not invalidate v1's published result; v1 used a different
methodology. v4's null/reversed result implies a methodology issue
under v3's pre-registered design; it does not specify what would fix
that issue. A follow-on experiment with v3 methodology + v1 prompt,
or v1 methodology + v3.1 prompt, would help disambiguate whether the
issue is in v3's prompt reformulation, in the focal_action /
state-signature design, or elsewhere. v4 alone cannot make that
determination.

---

## Pre-registration discipline

Matching v3's discipline (per v3 CLAUDE.md):

- This `SPEC.md` is frozen at pre-registration commit.
- `SPEC.pdf` is the immutable anchor — not edited after the commit.
- Any post-commit amendment is recorded as a dated supplement
  (`SPEC_v1.1.md`, etc.) with both-author sign-off; `SPEC.md` is not
  overwritten.
- Pilot failure pauses execution for author review; auto-recovery is
  not permitted.
- Effect-size monitoring during evaluation runs is not permitted.
  Technical monitoring (API errors, malformed chains, missing pairs)
  is permitted.

---

## Authors and Review

- Lead: Safiq Sindha (Microsoft Azure Hardware PM, independent
  research)
- Co-author: Myriam (Columbia University, systems engineering;
  Boeing FT) — reviews all major decisions; on all v4 publications

### Pre-registration sign-off

- [x] **Safiq Sindha** (lead author) — date: 2026-04-26
- [x] **Myriam** (co-author, Columbia University) — date: 2026-04-26

Both authors have signed off on this SPEC v1.0. Pre-registration commit
proceeds with this document and the generated SPEC.pdf as the immutable
anchors. Any post-commit methodology change requires a dated supplement
(`SPEC_v1.1.md`, `SPEC_v1.2.md`, etc.) with both-author sign-off; the
SPEC.md and SPEC.pdf themselves are not modified after commit.

---

## Pre-commit decisions (recorded; resolved by lead author 2026-04-26)

The following items were resolved before pre-registration commit:

1. **Secondary analysis: dropped** (Option 2.C). v4 runs primary
   analysis only. Bonferroni divisor = 1. v4 makes no claim about
   post-hoc-corrected methodologies.

2. **v1 chain availability: local mirror.** v1's chain JSONLs are
   available locally and will be mirrored into
   `data/v1_chains_mirror/` at pre-registration commit time. The
   deterministic 1,200-chain sample selected at seed 42 is recorded
   in `v4_chain_selection.json` and frozen at commit.

3. **Repository structure: git submodule.** v3 is referenced by git
   submodule pinned to its `T-code-game-v1.0-frozen` tag. v4 imports
   v3's modules from the submodule path; v3 source is not copied into
   v4. The submodule reference is part of the pre-registration commit.

4. **v4 Cell 1 relationship: parallel work, not input.** v4 Cell 2's
   RESULTS document references v4 Cell 1 as program context (existence,
   methodology-sensitivity finding) but does not condition v4 Cell 2's
   interpretation on Cell 1's disposition. Cell 2's outcome stands on
   its own pre-registration. Cell 1's eventual co-author review has no
   bearing on Cell 2's classification.

## Empirical items pending pilot validation

The following item is empirical — pre-registration commits to the
resolution rule, and the pilot data fills in the value.

1. **`current_phase` default value** (§"Reference Distribution Build").
   v3's `extract_state_signature` defaults `current_phase` to
   `"phase_opening"` when no `SubGoalTransition` appears in the prefix
   window. v1's chains may use a different `to_phase` taxonomy.
   Pre-registration commits to: *"the default value maximizing
   level-0/1 reference coverage on the pilot 50-chain set, recorded in
   `v4_chain_selection.json` before the full evaluation runs."* The
   pilot's reference-build step measures coverage at each candidate
   default; the highest-coverage value is selected. If multiple values
   tie within 0.5 percentage points, the lead author selects (and
   records the selection in the pilot session log).

---

## Technical risks identified during drafting

The two HIGH-risk items at draft time (v1 chain accessibility, secondary
analysis specification) were resolved by lead-author decisions recorded
in §"Pre-commit decisions". The remaining risks are:

1. **Prompt-vocabulary fixation.** v3.1-game's prompt examples
   (`piece_A`, `chain_B`, `formation_C`, `phase_endgame`,
   `progress_remaining`) are formal-game-flavored. When evaluated on
   v1 Pokémon chains, the model may anchor on these example labels
   rather than picking up the prefix's vocabulary (`unit_A`, `action_3`,
   etc.), producing artifactually low match rates. Pilot validation
   surfaces this. If this materializes, v4 has a known interpretation
   limit: the "v3 methodology with two v1-domain adaptations" frame
   becomes "v3 methodology with two v1-domain adaptations *plus*
   v3-flavored prompt examples that may anchor the model away from
   v1-flavored prefix vocabulary." The SPEC's framing already
   accommodates this; an explicit note in RESULTS.md is warranted if
   the pattern is observed. **MEDIUM RISK; pilot will detect.**

2. **Phase-name default value.** v3's `current_phase` defaults to
   `"phase_opening"`. v1's chains may use different `to_phase` strings
   from `SubGoalTransition` constraints. If v1's `to_phase` taxonomy
   does not include any string that maps to a sensible v3-style
   default, the level-0/1 backoff hits drop dramatically and v4's
   reference coverage falls below the 90% target. Pilot detects.
   **MEDIUM RISK; mitigation in SPEC.**

3. **Both-actionable filter retention.** v4 adds `InformationState`
   to actionable types (v1-domain adaptation). This is a deliberate
   choice but it changes the filter's behavior relative to v3. If
   v1's `InformationState` constraints are themselves non-predictive
   (the model cannot meaningfully predict which Pokémon will be
   revealed next), including them in actionable could pull the gap
   toward zero. Pilot's actionable-retention measurement is one input;
   the carrier analysis (§Supplementary) is another. **LOW-MEDIUM
   RISK; documented as an interpretation note rather than a spec
   risk.**

4. **Stored-vs-recomputed focal_action.** v1 chains were generated
   under v1's chain-construction code, which may have stored
   `focal_action` per the original `cutoff_k - 1` interpretation
   (later fixed in v3 by SPEC_v1.1 Amendment 2 to be
   `constraints[cutoff_k]`). v3's `reference.py` now recomputes
   focal_action on-the-fly and ignores the stored field. v4's reference
   build uses v3's `reference.py` with the v1-domain adaptations
   (phase-name default, 5-type actionable set), so v4 inherits the
   on-the-fly focal_action computation. v1's stored `focal_action` is
   not read. This is correct but worth noting: if v1 chains' stored
   `focal_action` was used elsewhere in v1's published numbers, v4's
   gap will be computed against a slightly different focal-action
   target than v1's published gap. This is a feature, not a bug —
   v4 tests v3's methodology, which uses the corrected focal_action —
   but it means v4's gap is not directly comparable to v1's published
   gap on a numerical basis. The §"Comparison to v1 published numbers"
   supplementary analysis must call this out. **LOW RISK; documented.**

---

## Estimated timeline

Per the §"Pre-commit decisions" resolutions, the only remaining
gating item is pilot validation:

| Phase | Calendar time | Notes |
|---|---|---|
| Pre-registration finalization | **DONE 2026-04-26** | Both authors signed off on SPEC v1.0 |
| Pre-registration commit | < 1 day | Generate SPEC.pdf, initialize v4 repo (v3 submodule + v1 chain mirror + chain selection JSON), commit |
| Pilot (50 chains, end-to-end) | 1–2 days | Includes reference build + scoring |
| Pilot review pause | 1–3 days | Author review |
| Full evaluation (14,400 calls × 1 model) | < 1 day wall time | Anthropic Batches API; v3's 57,600-call run took 26 minutes, so v4's 14,400 calls should run in ~10–15 minutes |
| Scoring | < 1 day | Separate session, blinded |
| Write-up | 3–5 days | RESULTS.md draft + co-author review |
| **Total focused work** | **1.5–2 weeks** | Matches the planning prompt's estimate |

Budget: ~$5–10 in Haiku Batches API calls, well under the planning
prompt's $20–30 estimate and well under prior phases.

---

*Pre-registration v1.0 — drafted and signed off 2026-04-26 by Safiq
Sindha (lead) and Myriam (co-author, Columbia University). Prior work:
[Project Ditto v1](https://github.com/safiqsindha/Project-Ditto)
(Pokémon, moderate/strong positive),
[Project Ditto v2](https://github.com/safiqsindha/Project-Ditto-v2)
(programming, partial replication),
[Project Ditto V3](https://github.com/safiqsindha/Project-Ditto-V3)
(formal-rule games, reversed on three of four cells; checkers_american
under review).*
