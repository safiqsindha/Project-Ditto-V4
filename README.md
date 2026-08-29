<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" alt="Project Ditto v4" width="100%">
  </picture>
</p>

# Project Ditto v4

**When v3 came back reversed, was the methodology broken — or was v3's data?**

v4 is a single-cell methodology characterization study. It takes v3's pre-registered methodology **unchanged** and runs it against v1's Pokémon Showdown chains, which are known to carry real-vs-shuffled signal under v1's own scoring. If the methodology were the problem, it should fail here too. If it produces strong signal on clean chains, the fault lies with v3's chain construction instead.

- **A control experiment, not a new hypothesis** — one model, one source, one variable changed
- **v3 is vendored, not edited** — pinned as a git submodule at commit `ac144c2`; v4 wraps it, never modifies it
- **Cheap and decisive** — 14,400 calls, $5–10 against a $50 hard ceiling
- **Replicated across three configs** before being called a result

![Python](https://img.shields.io/badge/python-3.10%2B-0891b2?style=flat-square)
![Outcome](https://img.shields.io/badge/outcome-strong__positive-22c55e?style=flat-square)
![Status](https://img.shields.io/badge/status-complete-22c55e?style=flat-square)
![Pre-registered](https://img.shields.io/badge/pre--registered-v1.0-7C3AED?style=flat-square)

**[Pre-registration](SPEC.md)** · **[Amendments](SPEC_v1.1.md)** · **[Results](RESULTS.md)** · **[Build plan](BUILD_PLAN.md)** · **[Session log](SESSION_LOG.md)**

## Result

| | |
|---|---|
| **Outcome** | **strong_positive** |
| Layer 1 gap (real − shuffled) | **+0.1311** |
| McNemar χ² | 167.3, *p* ≈ 0 |
| n_pairs_actionable | 3,600 (100% retention) |
| Model | Claude Haiku 4.5 |
| Pre-registration | `SPEC.md` v1.0, signed off 2026-04-26 |
| Both-author sign-off | Safiq Sindha · Myriam Khalil |

The gap clears the pre-registered strong-positive threshold (gap ≥ 0.08, Bonferroni *p* < 0.01) by a wide margin, and replicates across both variance configurations — T=0.5/seed=1337 gives +0.143, T=0.5/seed=7919 gives +0.134.

**Interpretation.** v3's pre-registered methodology is *not* the proximate cause of v3's reversed result. The same methodology produces strong signal on v1's organically-distributed Pokémon chains, which supports the conclusion that v3's reversal reflects v3-specific chain-construction properties rather than a flaw in the scoring or evaluation design.

### Pre-registered thresholds

| Tier | Criterion |
|---|---|
| Strong-positive | Layer 1 gap ≥ 0.08 **and** Bonferroni *p* < 0.01 |
| Moderate-positive | Layer 1 gap ≥ 0.05 **and** Bonferroni *p* < 0.05 |
| Null | Gap not clearing 0.05, or *p* not clearing 0.05 |
| Reversed | Gap negative **and** Bonferroni *p* < 0.05 in the negative direction |

The v4 hypothesis is supported iff the primary config clears at least moderate-positive. It cleared strong.

## Evaluation parameters

| Parameter | Value |
|---|---|
| Model | Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) |
| Source | `pokemon` — v1 Showdown chains |
| Chains | 1,200 real + 3,600 shuffled |
| Conditions | 1 real + 3 shuffled per real chain |
| Configs | T=0.0/seed=42 (primary) · T=0.5/seed=1337 · T=0.5/seed=7919 |
| Total calls | 14,400 |
| Bonferroni divisor | 1 — single cell, no correction |
| Cost | $5–10 actual, $50 hard ceiling |

## Two domain adaptations, both pre-committed

v3's methodology carries chess-specific defaults that do not transfer to Pokémon chains. Both changes below were committed in `SPEC.md`/`SPEC_v1.1.md` before evaluation, not chosen afterward.

**1. `current_phase` default.** v3 defaults to `"phase_opening"`, which is chess vocabulary. v1's `to_phase` values are `vs_unit_a`, `vs_unit_b`, … `forced_switch_required`. `v4_reference_builder.py --scan` tests candidates empirically on a 50-chain pilot; the winner is recorded in `v4_pilot_decisions.json`.

**2. `ACTIONABLE_TYPES` widened to all six types** (SPEC_v1.1 Amendment 1). `InformationState` is included because Pokémon battles carry genuine hidden information — the opponent's team is concealed until revealed. `ResourceBudget` was added because HP and PP directly constrain move selection and survival, which is categorically more actionable than a chess material count. The pilot made this necessary rather than optional: 46% of chains have `ResourceBudget` at the cutoff, and both-actionable retention was **30.7%** without it — below the 50% Gate 2 threshold.

> `CoordinationDependency` and `OptimizationCriterion` have zero occurrences in v1 chains. They stay in the set for consistency with the six-type definition, but have no practical effect here.

## Submodule pin — an engineering decision

`BUILD_PLAN.md` named `T-code-game-v1.0-frozen` as the pinning target, but that tag ships `PROMPT_VERSION = "v3.0-game"` (verb-noun format) while `SPEC.md` requires `v3.1-game` (entity-only). The two are inconsistent.

The submodule is therefore pinned to **`ac144c2`**, which carries the v3.1-game prompt (Amendment 1), on-the-fly `focal_action` recomputation (Amendment 2), the `primary_cells`/`variance_study` output structure (Amendment 3), and the Bug 4 fix populating reference counts at all four backoff levels. Without that last fix, shuffled chain pairs with no level-0 reference match were silently dropped and coverage could not exceed 90%.

This is an engineering implementation decision, not a methodology change: the SPEC committed to v3.1-game, and the pin is what actually satisfies it.

## Repository layout

```
vendor/v3/                  v3 as a git submodule, pinned to ac144c2 — never modified
src/
  v4_reference_builder.py   wraps the v3 reference builder; configurable phase default
  v4_runner.py              wraps the v3 batch runner; pokemon source, Haiku
  v4_scorer_config.py       wraps the v3 scorer; 6-type ACTIONABLE_TYPES, divisor 1
scripts/
  generate_selection.py     one-shot seed-42 chain selection (run once, committed)
  setup_v4_chains.py        builds the symlink trees the scorer reads
  check_rendered_format.py  sanity-checks v1 rendered-field compatibility
data/
  v1_chains_mirror/         4,806 v1 chain JSONLs (gitignored; MANIFEST.sha256 committed)
  v4_pokemon_chains/        symlink trees for the scorer (gitignored)
results/
  v4_scored.json            primary scored output (committed)
  phase1_summary.json       batch run summary (committed)
```

## Cross-session invariants

- `SPEC.md` and `SPEC.pdf` are **never** modified after the pre-registration commit
- `v4_chain_selection.json` is **never** modified after the pre-registration commit
- The v3 submodule is **never** modified
- The scorer runs in a **separate session** from the evaluation runner
- **No effect-size monitoring** during evaluation
- One `SESSION_LOG.md` entry per session

## The Ditto program

| Version | Domain | Headline |
|---|---|---|
| [v1](https://github.com/safiqsindha/Project-Ditto) | Pokémon Showdown telemetry | Sonnet +0.206 · Haiku +0.066 |
| [v2](https://github.com/safiqsindha/Project-Ditto-v2) | Programming agent trajectories | Partial reproduction |
| [v3](https://github.com/safiqsindha/Project-Ditto-V3) | Chess · Chess960 · checkers · draughts | Phase 1 complete, paused at Gate 8 |
| **v4** ⟵ *you are here* | **Pokémon, as a methodology control** | **+0.131, strong-positive** |
| [v4.5](https://github.com/safiqsindha/Ditto-V4.5--DeepSeek-Flash-test) | DeepSeek V4 Flash cross-model probe | Scoping stub |
| [v5](https://github.com/safiqsindha/Ditto-V5) | PUBG · NBA · CS:GO · Rocket League · poker | 4-tier hierarchy, closed |
| [v5.1](https://github.com/safiqsindha/Ditto-5.1) | 22-model cross-provider panel | Near-chance across the panel |
| [v5.2](https://github.com/safiqsindha/Ditto-5.2-diagostic) | Diagnostic kit for the v5.1 null | Pre-registered, in progress |
| [v5.4](https://github.com/safiqsindha/DITTO-V5.4-OLAT) | 24 inference levers, two DeepSeek models | 6 meaningful conditions |

## Authors

**Safiq Sindha** — lead author · **Myriam Khalil** — co-author

## License

No license file is present in this repository. Research artifacts; contact the repository owner for use beyond academic citation.
