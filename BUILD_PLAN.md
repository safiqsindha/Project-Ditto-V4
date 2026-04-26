# Project Ditto v4 — Build Plan

**Companion to:** `SPEC.md` v1.0 (signed off 2026-04-26 by Safiq Sindha
and Myriam) and `SPEC.pdf` (immutable anchor).

**Read this:** at the start of every session, after reading `SPEC.md`
and the latest `SESSION_LOG.md` entry.

This document is the session-by-session execution roadmap for v4. It
specifies which work happens in which session, what counts as a gate
pass/fail, and what stops execution for author review. The SPEC defines
*what* v4 commits to; this document defines *how* it gets executed.

This document is **not** part of the pre-registration anchor. It can be
revised between sessions as long as no SPEC commitment is changed.
Methodology changes require `SPEC_v1.1.md` (a dated supplement); only
execution sequencing and engineering decisions belong here.

---

## Session map

| Session | Purpose | Gate(s) | Commits |
|---|---|---|---|
| Session 1 | Repo init, pre-registration commit | Gate 1 | Pre-registration commit |
| Session 2 | Pilot (50 chains, end-to-end) | Gate 2 | Pilot results + pilot session log |
| Session 3 | Full evaluation Phase 1 | Gate 3 | Raw + blinded results |
| Session 4 | Scoring (separate session, blinded) | Gate 4 | `results/v4_scored.json` |
| Session 5 | RESULTS.md write-up | Gate 5 | RESULTS.md draft |
| (Session 6) | RESULTS.md commit | — | RESULTS.md final |

The total session count is small because v4 is a focused single-cell
study. Each session should run 2–6 hours of focused work; do not stretch
sessions or combine them. Session boundaries exist so SESSION_LOG entries
are grain-sized correctly for audit.

---

## Session protocol (every session)

**At session start:**

1. Read `SPEC.md` (frozen — do not modify; reference only)
2. Read `BUILD_PLAN.md` (this document) — find the relevant session's
   tasks and gate criteria
3. Read the previous `SESSION_LOG.md` entry for prior context
4. Confirm git working tree is clean before starting work

**During the session:**

- Mark tasks complete as you go, not in batches
- If a gate criterion fails, document in SESSION_LOG.md and stop for
  author review — do not auto-recover
- Do not compute gap statistics across cells during evaluation runs.
  v4 has only one cell, but the discipline still applies: do not run
  Layer 1 / Layer 2 calculations on partial Phase 3 data
- Engineering changes (defensive code patches, glob fixes, etc.) are
  permitted and recorded in SESSION_LOG.md. Methodology changes are
  not permitted; they require SPEC_v1.1.md
- If something looks like it might be a methodology change but you're
  not sure, **stop and ask** before proceeding

**At session end:**

- Append a new entry to `SESSION_LOG.md` per the format in v3's
  CLAUDE.md (Tasks completed / Gate status / Files created or
  modified / Blockers or open questions / Next session planned tasks)
- Commit with atomic, well-described commit messages
- Push to GitHub if the session output is non-trivial (skip for purely
  exploratory work)

**Stopping rules:**

- Pilot failure (Gate 2): pause for lead author review
- Full evaluation pre-flight failure (Gate 3 pre-flight checks fail):
  pause; do not auto-recover
- Any unanticipated divergence from the SPEC: pause and ask

---

## Gates

### Gate 1 — Pre-registration commit (Session 1)

**Pass criteria (all must hold):**

- v3 added as git submodule pinned to `T-code-game-v1.0-frozen`; `git
  submodule status` shows the correct commit hash
- v1 chain JSONLs mirrored into `data/v1_chains_mirror/` from the
  local source; SHA-256 of mirror manifest recorded in
  `data/v1_chains_mirror/MANIFEST.sha256`
- `v4_chain_selection.json` generated with the deterministic seed-42
  selection of 1,200 chain IDs from the mirror; committed before any
  evaluation
- `SPEC.md` committed with both-author sign-off (already recorded in
  the SPEC's Authors and Review section as of 2026-04-26)
- `SPEC.pdf` generated from `SPEC.md` and committed; `SPEC.pdf` is
  treated as immutable from this commit forward
- `BUILD_PLAN.md` (this document) committed
- `CLAUDE.md` (architecture / session protocol document) committed
- Pre-registration commit message: `"Pre-registration commit —
  thresholds and methodology frozen"`
- Repository pushed to `safiqsindha/Project-Ditto-V4`

**Fail response:** Stop. The pre-registration is the foundational
commitment; do not proceed to evaluation without all of the above in
place.

### Gate 2 — Pilot validation (Session 2)

**Pass criteria (all must hold):**

- 50 v1 chains from the chain selection load successfully under v3's
  chain-handling code (no schema mismatches, no parse errors)
- Reference distribution build on the pilot 50 achieves ≥ 90%
  non-max-backoff coverage at the chosen `current_phase` default value
  (the default value is selected by the pilot — see §"Session 2"
  below)
- 50 chains × (1 real + 3 shuffled) × 1 config (T=0.0 seed=42) = 200
  pilot calls succeed via the Anthropic Batches API at expected cost
  (~$0.30)
- Responses parse into single tokens; non-zero match rate against the
  reference distribution (sanity check; not an effect-size test)
- Both-actionable retention rate is ≥ 50% — flag if outside ~60–85%
  expected range; halt if below 50%
- Pilot scoring runs without error and produces well-formed
  `results/pilot_scored.json`

**Fail response:** Pause. Document the failure mode in SESSION_LOG.md.
Most likely failure modes and their responses are listed in §"Session
2 — Pilot" below. **Author review is required before any retry.**

### Gate 3 — Full evaluation pre-flight (Session 3)

**Pass criteria (all must hold; checked before any batch is submitted):**

- Pilot results (Gate 2) have been reviewed and approved by the lead
  author
- `v4_chain_selection.json` matches the pre-registration commit's
  selection (no drift)
- The 1,200 chains in the selection all load successfully (full check,
  not just the pilot 50)
- Reference distribution rebuilt on the full 1,200 chains (not just
  pilot) achieves ≥ 90% non-max-backoff coverage at the same
  `current_phase` default value selected at pilot
- Cost estimate from sample-call dry run is within $5–15 ceiling
- Per-batch chunking respects the runner's `_MAX_BATCH_SIZE` (10,000
  per batch); for 14,400 calls this means 2 batches per condition or
  similar — verify the chunking is correct before submission

**Fail response:** Stop. Pre-flight is the last checkpoint before
spending API budget; do not bypass.

### Gate 4 — Scoring complete (Session 4)

**Pass criteria:**

- `results/v4_scored.json` produced by the scorer with no errors
- Scorer was run with `SOURCES = ["pokemon"]`, the v1-domain
  `ACTIONABLE_TYPES` set, Bonferroni divisor = 1
- Output schema matches v3's SPEC_v1.1 Amendment 3 structure
  (`primary_cells` with one entry; `variance_study` with two entries)
- Scorer was run in a separate session from the evaluation runner
  (blinded protocol)
- Per-cell threshold classification produced an outcome tier in
  `{strong_positive, moderate_positive, weak_mixed, null, reversed}`

**Fail response:** Pause. Scoring failures are most often technical
(file-path or schema issues); diagnose and re-run within the same
session if the fix is purely engineering. If the issue is interpretive
(e.g., unclear how to handle missing pairs), pause for author review.

### Gate 5 — RESULTS.md draft (Session 5)

**Pass criteria:**

- RESULTS.md draft exists and matches the structure described in
  SPEC.md §"Phase 4 — Write-up"
- The four-outcome classification is reported per the pre-registered
  thresholds (no post-hoc reclassification)
- All supplementary analyses listed in SPEC.md §"Pre-registered
  Supplementary Analyses" are present (per-config variance,
  constraint-type carrier, comparison to v1 published numbers,
  pair-level disagreement, backoff-level distribution)
- RESULTS.md explicitly states v4's interpretation limits per SPEC.md
  §"Pre-registered Interpretation Framework"
- Technical risks observed during execution (e.g., prompt-vocabulary
  fixation, phase-name default coverage) are disclosed

**Fail response:** Iterate within the session. RESULTS draft can be
revised based on co-author feedback; this gate is for completeness
of structure, not for the substantive findings.

---

## Session 1 — Repo initialization and pre-registration commit

**Goal:** All pre-registration artifacts in place; evaluation can begin
in Session 2.

### Tasks

1. **Repo scaffold.** In the empty `safiqsindha/Project-Ditto-V4`
   repository:
   - Add `.gitignore` covering `__pycache__/`, `*.pyc`, `.env`,
     `results/raw/`, `results/blinded/`, `results/pilot_scored.json`,
     `results/v4_scored.json`, `data/v1_chains_mirror/*.jsonl` (the
     mirror itself; manifest is committed)
   - Add `pyproject.toml` and `requirements.txt` (Python ≥ 3.11;
     dependencies: `anthropic`, `scipy`, `numpy`, plus whatever v3's
     submodule needs at the pinned tag)
   - Add `.env.example` documenting required env vars
     (`ANTHROPIC_API_KEY`)

2. **Add v3 as submodule.** Pin to `T-code-game-v1.0-frozen`:
   ```bash
   git submodule add https://github.com/safiqsindha/Project-Ditto-V3 vendor/v3
   cd vendor/v3
   git checkout T-code-game-v1.0-frozen
   cd ../..
   git add vendor/v3
   ```
   Verify `git submodule status` shows the right commit hash.

3. **Mirror v1 chains.** Copy v1 chain JSONLs from local source into
   `data/v1_chains_mirror/`. Generate `MANIFEST.sha256` recording
   per-file SHA-256 hashes. Mirror is gitignored; manifest is
   committed.

4. **Generate chain selection.** Run a small selection script that:
   - Loads all chains from `data/v1_chains_mirror/`
   - Sorts by `chain_id` lexicographically (deterministic ordering)
   - Selects 1,200 chains using `random.Random(42)` from the sorted
     list
   - Writes `v4_chain_selection.json` with the seed (42) and the
     ordered list of 1,200 selected `chain_id`s
   - Commits the selection JSON before any evaluation

5. **Add v4-specific scripts that aren't in the v3 submodule.**
   v4 needs thin wrappers that:
   - Configure the v3 scorer with `SOURCES = ["pokemon"]` and the
     5-type `ACTIONABLE_TYPES` set
   - Configure the v3 reference builder with the candidate
     `current_phase` defaults to scan
   - These wrappers live in `src/v4_runner.py`, `src/v4_scorer_config.py`,
     `src/v4_reference_builder.py`. They MUST NOT modify v3 code; they
     import from `vendor/v3/src/...` and pass adapted configuration.

6. **Generate SPEC.pdf.** Convert `SPEC.md` to PDF via pandoc or
   similar. The PDF is the immutable pre-registration anchor; once
   committed, it is not edited.

7. **Initial CLAUDE.md and SESSION_LOG.md.**
   - `CLAUDE.md`: architecture and session protocol document, modeled
     on v3's CLAUDE.md but adapted for v4's smaller scope
   - `SESSION_LOG.md`: Session 1 entry in v3's format

8. **Pre-registration commit:**
   ```
   git add SPEC.md SPEC.pdf BUILD_PLAN.md CLAUDE.md SESSION_LOG.md \
     pyproject.toml requirements.txt .env.example .gitignore \
     .gitmodules vendor/v3 \
     v4_chain_selection.json data/v1_chains_mirror/MANIFEST.sha256 \
     src/v4_runner.py src/v4_scorer_config.py src/v4_reference_builder.py
   git commit -m "Pre-registration commit — thresholds and methodology frozen"
   git push origin main
   ```

### Files created or modified

| File | Status |
|---|---|
| `.gitignore` | new |
| `.gitmodules` | new (auto from submodule add) |
| `pyproject.toml` | new |
| `requirements.txt` | new |
| `.env.example` | new |
| `vendor/v3/` | submodule pinned to `T-code-game-v1.0-frozen` |
| `data/v1_chains_mirror/MANIFEST.sha256` | new (gitignored chain files) |
| `v4_chain_selection.json` | new |
| `src/v4_runner.py` | new |
| `src/v4_scorer_config.py` | new |
| `src/v4_reference_builder.py` | new |
| `SPEC.md` | new (signed-off draft) |
| `SPEC.pdf` | new (generated from SPEC.md; **immutable**) |
| `BUILD_PLAN.md` | new (this document) |
| `CLAUDE.md` | new |
| `SESSION_LOG.md` | new (Session 1 entry) |

### Gate 1 check

Run through all Gate 1 pass criteria above. If any fail: stop, fix,
retry. Do not proceed to Session 2 until Gate 1 is fully green.

### Estimated time

3–4 hours.

---

## Session 2 — Pilot validation

**Goal:** Validate that v3's methodology runs end-to-end on v1 chains
before committing to the full evaluation budget.

### Tasks

1. **Build candidate reference distributions.** v3's
   `extract_state_signature` defaults `current_phase` to
   `"phase_opening"`. v1's `to_phase` taxonomy may differ. Per SPEC
   §"Empirical items pending pilot validation":
   - Identify the candidate default values: at minimum
     `"phase_opening"` (v3 default), plus whatever v1 actually emits
     for early-game `SubGoalTransition.to_phase` (inspected from a
     sample of 20 v1 chains)
   - Build pilot reference distributions for each candidate using
     v3's `ReferenceDistribution.build_from_chains` on the pilot 50
     chains
   - Run `check_coverage` for each candidate; record level-0/1
     coverage
   - Select the candidate with highest non-max-backoff coverage. If
     the top two tie within 0.5 percentage points, lead author selects
     manually

2. **Record the selected default.** Add the chosen default value to
   `v4_chain_selection.json` (or a separate `v4_pilot_decisions.json`
   if cleaner). The choice is now part of the pre-registered v4
   methodology.

3. **Pilot evaluation run.** 50 chains × (1 real + 3 shuffled) × 1
   config (T=0.0 seed=42) = 200 calls. Submit via Anthropic Batches
   API:
   - Use `src/v4_runner.py` with `--n 50 --seeds 42 --temperature 0.0
     --dry-run` first to verify the pipeline; then run the actual
     pilot
   - Cost expected: ~$0.30 (200 calls × $0.0015/call rough)
   - Wall time: ~30 seconds for batch submission, ~5–25 minutes for
     batch completion (Anthropic batch infrastructure variance)

4. **Pilot scoring.** Run the v3 scorer (via
   `src/v4_scorer_config.py`) on the pilot results. Output goes to
   `results/pilot_scored.json`. Pilot scoring uses the same
   methodology as the full evaluation, so any scorer issues surface
   here.

5. **Inspect pilot output.** Verify:
   - Reference distribution coverage at the selected default ≥ 90%
   - Both-actionable retention rate ≥ 50% (flag if outside 60–85%)
   - Layer 1 match rate is non-zero on real chains
   - Layer 1 match rate is non-zero on shuffled chains (if zero on
     either, something is wrong with the scoring pipeline, not with
     the experimental signal)
   - No file-path errors, no JSON schema mismatches

6. **Document any prompt-vocabulary anomalies.** If responses cluster
   on `phase_endgame` / `formation_C` / `piece_A` even when v1
   chains contain `unit_A` / `action_3` etc., this is the
   prompt-vocabulary fixation risk (SPEC §Risk 1) materializing.
   Record the response distribution in SESSION_LOG.md. This does NOT
   halt the pilot — it's an interpretation note for the final
   RESULTS.md.

7. **Gate 2 check.** Run through Gate 2 pass criteria. If all pass,
   notify lead author with a pilot summary. **Stop and wait for
   author approval before Session 3.**

### Pilot fail modes and responses

| Symptom | Likely cause | Response |
|---|---|---|
| Coverage < 90% at all candidate defaults | v1 chains' `to_phase` taxonomy is structurally incompatible with v3's signature | Pause for author review. May require a SPEC_v1.1 supplement extending the empirical default rule, or a structural adaptation. |
| Both-actionable retention < 50% | v1 chains have unexpectedly low actionable density at cutoff | Pause for author review. May indicate that v4's 5-type set is not the right adaptation for v1's domain. |
| Match rate near zero on real | Prompt-vocabulary fixation OR scorer normalization issue OR reference-build issue | Inspect response distribution + reference-distribution top entries. If purely vocabulary fixation, record and proceed to Session 3 with the limit documented. If scorer/reference issue, fix the engineering bug and re-pilot. |
| API calls fail at scale | Rate limiting or env config | Engineering issue — diagnose and retry. Not a methodology issue. |
| Chain load errors | v1 chain schema mismatch with v3's `extract_state_signature` expectations | Pause. Likely needs `src/v4_reference_builder.py` to adapt the chain dict before passing to v3 code. May be a SPEC supplement if the adaptation is non-trivial. |

### Files created or modified

| File | Status |
|---|---|
| `data/reference_v4_pokemon_pilot.pkl` | new (pilot reference distribution) |
| `v4_pilot_decisions.json` (or addition to `v4_chain_selection.json`) | new (records selected `current_phase` default) |
| `results/raw/pilot/*.json` | new (gitignored) |
| `results/blinded/pilot/*.json` | new (gitignored) |
| `results/pilot_scored.json` | new (gitignored) |
| `SESSION_LOG.md` | append Session 2 entry |

### Gate 2 check

Run through Gate 2 pass criteria. **Halt for author review** before
Session 3 regardless of pass/fail — the lead author needs to inspect
pilot output before $5–10 of full-eval spend.

### Estimated time

3–5 hours including the wait for batch completion.

---

## Session 3 — Full evaluation Phase 1

**Goal:** Run the full v4 evaluation: 1,200 chains × 4 conditions × 3
configs = 14,400 calls.

### Tasks

1. **Pre-flight.** Verify Gate 3 pre-flight checks. Specifically:
   - Lead author has approved the pilot output (per Session 2 stop
     point)
   - `v4_chain_selection.json` is unchanged from pre-registration
     commit
   - All 1,200 chains load successfully (not just pilot 50)
   - Reference distribution rebuilt on full 1,200 chains achieves ≥
     90% coverage at the pilot-selected default
   - Cost estimate from a 10-call sample matches expectations

2. **Build full reference distribution.** Run
   `src/v4_reference_builder.py` on the full 1,200-chain selection
   with the pilot-selected `current_phase` default. Save to
   `data/reference_v4_pokemon_full.pkl`.

3. **Per-config evaluation.** Submit 3 batch jobs (one per config),
   each covering all 1,200 chains × 4 conditions:
   - Config 1: T=0.0, seed=42 (primary)
   - Config 2: T=0.5, seed=1337 (variance study)
   - Config 3: T=0.5, seed=7919 (variance study)
   - Each config has 4,800 calls; chunked per `_MAX_BATCH_SIZE`
     limits

4. **Monitor.** Technical monitoring only (API errors, malformed
   responses, missing pairs). **No effect-size monitoring.** Do not
   look at match rates between batches.

5. **Save raw results.** All responses to `results/raw/phase1/{config}/`.
   Generate blinded mirrors in `results/blinded/phase1/` (model
   identity, condition, seed stripped per v3's blinded-scorer
   protocol).

6. **Gate 3 check.** Verify:
   - Total calls submitted = 14,400
   - Total calls succeeded ≥ 14,260 (≥ 99% success rate per v3 Phase
     1 baseline)
   - Per-config call count = 4,800 (no missing batches)
   - Raw and blinded result files present in expected paths
   - Cost stayed within $5–15

### Files created or modified

| File | Status |
|---|---|
| `data/reference_v4_pokemon_full.pkl` | new (gitignored — large) |
| `data/reference_v4_pokemon_full.coverage.json` | new (committed; coverage stats) |
| `results/raw/phase1/{config}/*.json` | new (gitignored — 14,400 files) |
| `results/blinded/phase1/*.json` | new (gitignored) |
| `results/phase1_summary.json` | new (committed; per-batch stats) |
| `results/phase1_log.txt` | new (committed; full stdout) |
| `SESSION_LOG.md` | append Session 3 entry |

### Estimated time

1–2 hours active work plus ~30 minutes for batch completion (per v3
Session 10's 26-minute wall time on 4× v4's call volume).

### Stop point

After Session 3 completes successfully, **stop and notify lead
author**. Do not auto-proceed to scoring. v3's protocol is to score
in a separate session from a fresh environment; v4 follows the same
discipline.

---

## Session 4 — Scoring (separate session, blinded)

**Goal:** Produce `results/v4_scored.json` from blinded inputs.

### Tasks

1. **Verify blinded protocol.** Open a fresh session/environment.
   The scorer reads from `results/blinded/phase1/` only. Model
   identity, condition (real vs shuffled), and eval_seed have been
   stripped. The scorer reconstructs pairing from `chain_id` patterns
   (`{base_id}` vs `{base_id}_shuffled_{shuffle_seed}`).

2. **Run scoring.** Use `src/v4_scorer_config.py` to invoke v3's
   scorer with the v4-specific configuration:
   ```bash
   python -m src.v4_scorer_config \
     --results results/blinded/phase1/ \
     --reference data/reference_v4_pokemon_full.pkl \
     --bonferroni-divisor 1 \
     --out results/v4_scored.json
   ```

3. **Verify scorer output structure.** Confirm:
   - `primary_cells` has exactly one entry: `haiku::pokemon`
   - `variance_study` has exactly two entries:
     `haiku::pokemon::T0.5_seed1337`,
     `haiku::pokemon::T0.5_seed7919`
   - Per-cell stats include: `gap`, `mcnemar_chi2`, `raw_p`,
     `bonferroni_p`, `n_pairs`, `both_actionable_retention`,
     `outcome_tier`
   - `bonferroni_p` equals `raw_p` (since divisor = 1)

4. **Record outcome tier.** Per SPEC §"Pre-registered Success
   Criteria" thresholds. The classification logic is already in v3's
   scorer; verify it produced one of `{strong_positive,
   moderate_positive, weak_mixed, null, reversed}`.

5. **Gate 4 check.** Verify all Gate 4 pass criteria.

6. **Stop point.** Do NOT begin RESULTS.md write-up in this session.
   v3's discipline is to keep scoring isolated from interpretation;
   the lead author reviews the scored output before write-up begins.

### Files created or modified

| File | Status |
|---|---|
| `results/v4_scored.json` | new (committed) |
| `SESSION_LOG.md` | append Session 4 entry |

### Estimated time

1–2 hours.

---

## Session 5 — RESULTS.md write-up

**Goal:** Draft `RESULTS.md` matching v3's RESULTS structure.

### Tasks

1. **Structure.** RESULTS.md sections:
   - Status (with pre-registration link, scoring link, authors, date)
   - Abstract
   - Hypothesis (quoted from SPEC.md)
   - Pre-registered Success Criteria (quoted from SPEC.md)
   - Methods (data, methodology, the two v1-domain adaptations,
     scoring)
   - Results (per-cell threshold check; primary outcome tier; variance
     study)
   - Pre-registered Supplementary Analyses (one subsection per item
     in SPEC §"Pre-registered Supplementary Analyses")
   - Discussion (what the result establishes; what it does NOT
     establish; comparison to v1, v2, v3)
   - Limits (interpretation framework reminder; technical risks
     observed during execution)
   - Authors and Acknowledgements

2. **Outcome reporting.** Report the outcome per the pre-registered
   thresholds. **Do not** post-hoc reclassify. If the outcome is
   ambiguous (e.g., gap = 0.049 just below 0.05), report it as the
   tier the threshold rule produces, not the tier closest in spirit.

3. **Comparison to v1 published numbers.** Per SPEC §Supplementary 3.
   Use v1's CORRECTED_SCORING figures (Haiku 0.066, Sonnet 0.206) as
   the v1 reference points. Note the focal_action computation
   difference (v3's on-the-fly vs v1's stored — see SPEC §Risk 4) so
   the comparison is calibrated correctly.

4. **Comparison to v3 Phase 1 numbers.** Per SPEC §Supplementary 3.
   Sourced from v3's `results/phase1_v31_scored_full.json`. The four
   v3 cell gaps (chess_standard −0.187, chess960 −0.231,
   checkers_american −0.115/+0.039, draughts_intl −0.155) are the
   reference points.

5. **Constraint-type carrier analysis.** Per SPEC §Supplementary 2.
   Compare which constraint types carry the actionable signal in v4
   to v2's TB-vs-SWE asymmetry (TB → ToolAvailability; SWE →
   InformationState). v4's 5-type set includes InformationState,
   which is a primary candidate carrier given v1's hidden-info
   structure.

6. **Disclose technical observations.** If pilot or full eval
   surfaced any technical risks (prompt-vocabulary fixation,
   coverage difficulty at chosen default, etc.), disclose explicitly
   in §Limits.

7. **Co-author review.** Send draft to Myriam. Iterate based on
   feedback. Gate 5 is the structural completeness check; substantive
   revisions can continue after Gate 5 passes.

8. **Final commit (Session 6, separate).** After co-author sign-off,
   commit the final RESULTS.md. Tag the v4 results commit with
   `v4-results-final-{date}`.

### Files created or modified

| File | Status |
|---|---|
| `RESULTS.md` | new (draft, then iterate) |
| `SESSION_LOG.md` | append Session 5 entry (draft); Session 6 entry (final) |

### Gate 5 check

Run through Gate 5 pass criteria. Iterate within session until
structural completeness is satisfied. Substantive revisions
post-co-author can extend across multiple sessions; that's fine.

### Estimated time

3–5 days calendar (1–2 days drafting; 1–3 days co-author review and
iteration).

---

## Out-of-band issues

### What stops execution

- Gate failure with no obvious engineering fix
- Anticipated SPEC deviation (anything that smells like a methodology
  change)
- Cost overrun beyond the $5–15 ceiling
- Co-author has not approved a step that requires approval (after
  pilot; before final commit)

### What does NOT stop execution

- Defensive code patches (typo fixes, glob pattern fragility, NaN
  handling)
- API rate limit retries (use exponential backoff per v3's runner)
- Re-running a batch that failed for transient reasons
- Adding logging or diagnostics

The distinction: methodology vs engineering. If unsure, stop and ask.

### Cost overrun protocol

If actual costs exceed $15 during evaluation:

1. Stop the current batch
2. Diagnose (typically: token-count miscalibration or unintended Sonnet
   calls)
3. Notify lead author
4. Do not auto-resume; require explicit approval to continue

Budget hard ceiling: $50 total. Above this, halt and reassess.

### Methodology change protocol

Any methodology change post-pre-registration commit:

1. Stop work
2. Document the proposed change in SESSION_LOG.md
3. Draft a `SPEC_v1.1.md` supplement following v3's SPEC_v1.1 model
4. Both authors sign off on the supplement
5. Implement the change against the supplement

Never modify `SPEC.md` or `SPEC.pdf` post-commit.

---

## Cross-session invariants

These hold across all sessions:

- `SPEC.md` and `SPEC.pdf` are not modified post-commit
- v3 submodule is not modified; if v3 itself changes, the submodule
  stays pinned to `T-code-game-v1.0-frozen`
- `v4_chain_selection.json` is not modified post-commit
- The scorer is run in a session separate from the evaluation runner
- No effect-size monitoring during evaluation
- SESSION_LOG.md has one entry per session, in v3's format
- Engineering changes are documented in SESSION_LOG.md, not buried in
  commits

---

## v4 Cell 1 relationship

Per SPEC §"Relationship to v4 Cell 1": v4 Cell 1 is parallel work on
v3's repo (non-merged branch `claude/v4-cell-1-statistical-robustness`).
This BUILD_PLAN does **not** include any task related to Cell 1's
disposition. Cell 1's eventual co-author review and merge decision is
out of scope for v4 Cell 2 execution.

If during Session 5 RESULTS.md write-up the lead author wants to
reference Cell 1's findings as program context, that's fine and
already accommodated in SPEC §Supplementary 3. v4 Cell 2's
classification does not depend on Cell 1's disposition.

---

## Quick reference: gate decisions

| Gate | Pass action | Fail action |
|---|---|---|
| Gate 1 | Proceed to Session 2 | Stop; fix scaffold issues |
| Gate 2 | Notify author; wait for approval | Stop; document in SESSION_LOG; author review |
| Gate 3 (pre-flight) | Submit batches | Stop; do not bypass pre-flight |
| Gate 3 (post-eval) | Notify author; proceed to Session 4 in fresh session | Stop; investigate failures |
| Gate 4 | Notify author; await approval before Session 5 | Diagnose engineering issue; if methodology issue, stop |
| Gate 5 | Iterate with co-author until commit | Iterate within session |

---

*BUILD_PLAN.md v1.0 — 2026-04-26. Companion to SPEC.md v1.0 (signed
off by both authors 2026-04-26).*
