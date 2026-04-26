# Project Ditto v4

**Single-cell methodology characterization study.**

Applies v3's pre-registered methodology to v1's Pokémon Showdown chains (known
signal carriers) to test whether v3's reversed result on chess/draughts chains
reflects a flaw in the methodology or a property of v3's chain construction.

| | |
|---|---|
| **Outcome** | **strong_positive** |
| Layer 1 gap (real − shuffled) | **+0.1311** |
| McNemar χ² | 167.3, p ≈ 0 |
| n_pairs_actionable | 3,600 (100% retention) |
| Model | Claude Haiku 4.5 |
| Pre-registration | `SPEC.md` v1.0, signed off 2026-04-26 |
| Both-author sign-off | Safiq Sindha + Myriam Khalil |

The gap of +0.1311 clears the pre-registered strong-positive threshold
(gap ≥ 0.08, Bonferroni p < 0.01) by a wide margin and replicates across
both variance configs (T=0.5/seed=1337: +0.143; T=0.5/seed=7919: +0.134).

**Interpretation:** v3's pre-registered methodology is not the proximate cause
of v3's reversed result on chess/draughts chains. The methodology produces
strong signal when applied to v1's organically-distributed Pokémon chains,
supporting the conclusion that v3's reversal reflects v3-specific
chain-construction properties.

---

## Key documents

| File | Description |
|---|---|
| [`SPEC.md`](SPEC.md) | Pre-registration (frozen) |
| [`SPEC_v1.1.md`](SPEC_v1.1.md) | Post-commit methodology amendments (both-author sign-off) |
| [`RESULTS.md`](RESULTS.md) | Full write-up: methods, results, supplementary analyses, discussion |
| [`results/v4_scored.json`](results/v4_scored.json) | Scored output (primary + variance study) |
| [`BUILD_PLAN.md`](BUILD_PLAN.md) | Session execution roadmap |
| [`SESSION_LOG.md`](SESSION_LOG.md) | Per-session engineering log |

---

## Repository structure

```
vendor/v3/              v3 scoring pipeline (git submodule, pinned to ac144c2)
src/
  v4_runner.py          batch evaluation runner (Haiku, pokemon source)
  v4_scorer_config.py   scorer wrapper with v1-domain patches
  v4_reference_builder.py  reference distribution builder
data/
  v1_chains_mirror/     v1 Pokémon Showdown chains (gitignored; MANIFEST.sha256 committed)
  v4_pokemon_chains/    symlink directories for scorer (gitignored)
  reference_v4_pokemon_full.pkl   reference distribution (gitignored)
  reference_v4_pokemon_full.coverage.json  coverage stats (committed)
results/
  v4_scored.json        primary scored output (committed)
  phase1_summary.json   batch run summary (committed)
scripts/
  generate_selection.py   seed-42 chain selection (run once)
  setup_v4_chains.py      creates symlink directories
```

---

## Prior program

- [Project Ditto v1](https://github.com/safiqsindha/Project-Ditto) — Pokémon Showdown, moderate/strong positive
- [Project Ditto v2](https://github.com/safiqsindha/Project-Ditto-v2) — programming tasks, partial replication
- [Project Ditto V3](https://github.com/safiqsindha/Project-Ditto-V3) — formal-rule games, reversed on three of four cells; checkers_american under review
