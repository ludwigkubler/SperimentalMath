# 04 - Dead Code & Orphan Files Audit

Sub-agent 4/6 of code-integrity audit. Read-only analysis on `ludo@sec`.
Generated: 2026-05-13. Source: `/tmp/audit_1778671816/python.txt`

## 1. Executive Summary

- Python files analyzed: **6,348**
- Candidate modules examined for orphan status: **1,322** (after excluding __init__/__main__/setup/conftest, test_*, scripts/bin, __main__-guarded)
- Orphan files detected (basename never imported anywhere): **409**
- Public function defs analyzed (non-framework, non-builtin-name): **19,595**
- Dead public functions (zero external call sites): **3,128**

## 2. Orphan Files (top 50 by LOC)

Definition: module basename never appears as an imported leaf anywhere in the 6,348-file corpus.
Files marked with `WARN` are >200 LOC (high-value possibly-dead code).

| # | Path | LOC | System | Last Modified |
|---|------|-----|--------|---------------|
| 1 | `/home/ludo/Scrivania/future/research/research_proof_complexity_20260404_204925/research_proof_complexity_20260404_204925/complexity_research.py` | 554 WARN | Scrivania/future | 2026-04-04 |
| 2 | `/home/ludo/Scrivania/future/create/cli_tool_20260413_055245/algorithm_kata_20260413_065514/billing_cycle.py` | 342 WARN | Scrivania/future | 2026-04-13 |
| 3 | `/home/ludo/Scrivania/future/practice/algorithm_kata_20260413_065514/algorithm_kata_20260413_065514/billing_cycle.py` | 342 WARN | Scrivania/future | 2026-04-13 |
| 4 | `/home/ludo/Scrivania/future/research/research_proof_complexity_20260407_200531/research_proof_complexity_20260407_200531/dictionary_processor.py` | 333 WARN | Scrivania/future | 2026-04-07 |
| 5 | `/home/ludo/tools/Wav2Lip/evaluation/real_videos_inference.py` | 305 WARN | tools | 2026-04-14 |
| 6 | `/home/ludo/tools/Wav2Lip/inference.py` | 280 WARN | tools | 2026-04-14 |
| 7 | `/home/ludo/tools/Wav2Lip/evaluation/gen_videos_from_filelist.py` | 238 WARN | tools | 2026-04-14 |
| 8 | `/home/ludo/SEC/src/monetization/sec_revenue.py` | 216 WARN | SEC | 2026-04-07 |
| 9 | `/home/ludo/Scrivania/SEC/src/monetization/sec_revenue.py` | 216 WARN | Scrivania/SEC | 2026-04-07 |
| 10 | `/home/ludo/Scrivania/future/practice/math_proof_20260411_155708/math_proof_20260411_155708/eigen_analysis.py` | 209 WARN | Scrivania/future | 2026-04-11 |
| 11 | `/home/ludo/Scrivania/future/explore/new_language_feature_20260408_153811/new_language_feature_20260408_153811/src/data_analysis/lessons.py` | 189 | Scrivania/future | 2026-04-08 |
| 12 | `/home/ludo/Scrivania/future/research/chess_research_20260405_134753/chess_research_20260405_134753/natural_proofs.py` | 129 | Scrivania/future | 2026-04-05 |
| 13 | `/home/ludo/Scrivania/future/practice/refactor_challenge_20260410_063038/gas_expansion.py` | 127 | Scrivania/future | 2026-04-10 |
| 14 | `/home/ludo/Scrivania/future/reflect/security_audit_20260405_012151/security_audit_20260405_012151/notification_system.py` | 125 | Scrivania/future | 2026-04-05 |
| 15 | `/home/ludo/Scrivania/future/research/research_proof_complexity_20260408_185626/ideal_gas_expansion.py` | 116 | Scrivania/future | 2026-04-08 |
| 16 | `/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/audit/triage_inconclusive.py` | 114 | Scrivania/SEC | 2026-05-08 |
| 17 | `/home/ludo/Scrivania/future/explore/architecture_study_20260414_150035/architecture_study_20260414_150035/data_processing/pigeonhole_principle.py` | 111 | Scrivania/future | 2026-04-15 |
| 18 | `/home/ludo/Scrivania/future/experiment/research_formalization_20260404_210238/two_body_simulation.py` | 110 | Scrivania/future | 2026-04-04 |
| 19 | `/home/ludo/Scrivania/future/explore/architecture_study_20260414_150035/architecture_study_20260414_150035/natural_proofs_analysis.py` | 109 | Scrivania/future | 2026-04-15 |
| 20 | `/home/ludo/Scrivania/future/practice/refactor_challenge_20260410_000854/refactor_challenge_20260410_000854/web_data_collector.py` | 106 | Scrivania/future | 2026-04-10 |
| 21 | `/home/ludo/Scrivania/future/create/physics_simulation_20260405_200808/ideal_gas_expansion.py` | 105 | Scrivania/future | 2026-04-05 |
| 22 | `/home/ludo/Scrivania/future/experiment/creative_solution_20260408_215734/src/sat_analysis.py` | 101 | Scrivania/future | 2026-04-08 |
| 23 | `/home/ludo/Scrivania/future/explore/new_language_feature_20260408_153811/new_language_feature_20260408_153811/src/data_analysis/analyze.py` | 101 | Scrivania/future | 2026-04-08 |
| 24 | `/home/ludo/Scrivania/future/reflect/analyze_errors_20260408_233248/analyze_errors_20260408_233248/error_prevention_strategies_python.py` | 101 | Scrivania/future | 2026-04-09 |
| 25 | `/home/ludo/Scrivania/future/research/research_literature_review_20260412_182703/barrier_summary.py` | 100 | Scrivania/future | 2026-04-12 |
| 26 | `/home/ludo/Scrivania/future/create/physics_simulation_20260412_003753/physics_simulation_20260412_003753/orbit_visualization.py` | 98 | Scrivania/future | 2026-04-12 |
| 27 | `/home/ludo/Scrivania/future/practice/physics_derivation_20260409_202050/n_body_simulation.py` | 98 | Scrivania/future | 2026-04-09 |
| 28 | `/home/ludo/Scrivania/future/create/micro_project_20260405_114659/src/blackbody_radiation.py` | 96 | Scrivania/future | 2026-04-05 |
| 29 | `/home/ludo/Scrivania/future/research/research_literature_review_20260412_182703/verify_barriers.py` | 95 | Scrivania/future | 2026-04-12 |
| 30 | `/home/ludo/Scrivania/future/research/research_proof_complexity_20260410_002419/verify_dirac_equation.py` | 93 | Scrivania/future | 2026-04-10 |
| 31 | `/home/ludo/kissat/pvnp_lab/lab_c001/experiments/make_plots.py` | 92 | kissat | 2026-01-16 |
| 32 | `/home/ludo/Scrivania/future/explore/learn_library_20260405_161642/learn_library_20260405_161642/library_analysis.py` | 92 | Scrivania/future | 2026-04-05 |
| 33 | `/home/ludo/Scrivania/future/practice/algorithm_kata_20260405_160538/src/planetaryOrbits.py` | 92 | Scrivania/future | 2026-04-05 |
| 34 | `/home/ludo/Scrivania/future/experiment/research_formalization_20260429_022053/research_formalization_20260429_022053/webhook_handler.py` | 91 | Scrivania/future | 2026-04-29 |
| 35 | `/home/ludo/Scrivania/future/practice/test_writing_20260429_023704/research_formalization_20260429_022053/webhook_handler.py` | 91 | Scrivania/future | 2026-04-29 |
| 36 | `/home/ludo/Scrivania/future/explore/chess_study_20260410_114853/chess_study_20260410_114853/src/chess_db_scraper.py` | 88 | Scrivania/future | 2026-04-10 |
| 37 | `/home/ludo/Scrivania/future/explore/architecture_study_20260412_040948/architecture_study_20260412_040948/db_migration_tool.py` | 87 | Scrivania/future | 2026-04-12 |
| 38 | `/home/ludo/Scrivania/future/explore/architecture_study_20260412_042203/architecture_study_20260412_040948/db_migration_tool.py` | 87 | Scrivania/future | 2026-04-12 |
| 39 | `/home/ludo/Scrivania/future/experiment/cross_language_20260405_052832/src/einstein_friedmann.py` | 86 | Scrivania/future | 2026-04-05 |
| 40 | `/home/ludo/SEC/src/monetization/cleanup_videos.py` | 84 | SEC | 2026-04-06 |
| 41 | `/home/ludo/Scrivania/SEC/src/monetization/cleanup_videos.py` | 84 | Scrivania/SEC | 2026-04-06 |
| 42 | `/home/ludo/Scrivania/future/reflect/security_audit_20260412_004637/physics_simulation_20260412_003753/euler_lagrange_simulation.py` | 84 | Scrivania/future | 2026-04-12 |
| 43 | `/home/ludo/Scrivania/future/create/physics_simulation_20260412_003753/physics_simulation_20260412_003753/euler_lagrange_simulation.py` | 84 | Scrivania/future | 2026-04-12 |
| 44 | `/home/ludo/Scrivania/future/practice/math_practice_20260402_211813/math_data_scraper.py` | 84 | Scrivania/future | 2026-04-02 |
| 45 | `/home/ludo/Scrivania/future/explore/architecture_study_20260404_224423/architecture_study_20260404_224423/src/Application/Service/HttpClientService.py` | 83 | Scrivania/future | 2026-04-04 |
| 46 | `/home/ludo/Scrivania/future/explore/learn_library_20260405_013611/src/json_yaml_toml_csv_converter.py` | 83 | Scrivania/future | 2026-04-05 |
| 47 | `/home/ludo/Scrivania/future/practice/design_pattern_20260409_144443/design_pattern_20260409_144443/repository.py` | 83 | Scrivania/future | 2026-04-09 |
| 48 | `/home/ludo/Scrivania/future/practice/math_practice_20260407_170507/math_practice_20260407_170507/math_solver.py` | 83 | Scrivania/future | 2026-04-07 |
| 49 | `/home/ludo/Scrivania/future/practice/design_pattern_20260405_121106/design_pattern_20260405_121106/experiment_instances.py` | 82 | Scrivania/future | 2026-04-05 |
| 50 | `/home/ludo/Scrivania/future/research/tech_trend_20260405_080852/tech_trend_20260405_080852/sympy_math.py` | 81 | Scrivania/future | 2026-04-05 |

## 3. Dead Public Functions (top 30)

Definition: public `def NAME(`/`async def NAME(` (not starting with `_`), not decorated with any decorator (framework or otherwise), not in the skip-list of generic names, and whose `NAME(` pattern has zero occurrences in the corpus outside the defining file.

Caveats: token-based counting; methods of classes sharing names with functions can be over-counted (so over-reporting of "alive" is biased - these are highly-confident dead). Skip-list excludes builtins/stdlib/duck-typed names like `open`, `read`, `run`, `main`, `setup`, `parse`, `fit`, `predict`, `to_dict`, etc.

| # | Path:Line | Function |
|---|-----------|----------|
| 1 | `/home/ludo/Scrivania/SEC/src/ml/finetune_builder.py:302` | `cli_export_dataset` |
| 2 | `/home/ludo/Scrivania/SEC/src/worker.py:32` | `run_kpi_sync` |
| 3 | `/home/ludo/Scrivania/SEC/src/worker.py:46` | `run_lit_scout` |
| 4 | `/home/ludo/Scrivania/SEC/src/worker.py:67` | `run_weekly_eval` |
| 5 | `/home/ludo/Scrivania/SEC/src/worker.py:75` | `run_distill_sample` |
| 6 | `/home/ludo/Scrivania/SEC/src/worker.py:85` | `sync_to_main` |
| 7 | `/home/ludo/Scrivania/SEC/src/worker.py:101` | `worker_loop` |
| 8 | `/home/ludo/Scrivania/SEC/src/research/bootstrap_conjecture003b.py:26` | `load_conjecture_003b` |
| 9 | `/home/ludo/Scrivania/SEC/src/research/bootstrap_conjecture001.py:28` | `load_conjecture_001` |
| 10 | `/home/ludo/Scrivania/SEC/src/bridges/tseitin_tw/bridge.py:147` | `find_sorry_sites` |
| 11 | `/home/ludo/Scrivania/SEC/src/bridges/tseitin_tw/bridge.py:197` | `probe_repo` |
| 12 | `/home/ludo/Scrivania/SEC/src/bridges/tseitin_tw/bridge.py:232` | `generate_suggestion` |
| 13 | `/home/ludo/Scrivania/SEC/src/bridges/tseitin_tw/bridge.py:311` | `persist_suggestion` |
| 14 | `/home/ludo/Scrivania/SEC/src/core/learning_hooks.py:146` | `reflexion_hints_for` |
| 15 | `/home/ludo/Scrivania/SEC/src/core/self_eval.py:39` | `ablation_flag` |
| 16 | `/home/ludo/Scrivania/SEC/src/core/self_eval.py:44` | `active_ablations` |
| 17 | `/home/ludo/Scrivania/SEC/src/monetization/retention_analytics.py:51` | `fetch_video_retention` |
| 18 | `/home/ludo/Scrivania/SEC/src/monetization/retention_analytics.py:130` | `refresh_channel_retention` |
| 19 | `/home/ludo/Scrivania/SEC/src/monetization/content_factory.py:92` | `pick_stock_queries` |
| 20 | `/home/ludo/Scrivania/SEC/src/monetization/continuous_run.py:232` | `telegram_alert` |
| 21 | `/home/ludo/Scrivania/SEC/src/monetization/continuous_run.py:250` | `validate_video` |
| 22 | `/home/ludo/Scrivania/SEC/src/monetization/continuous_run.py:285` | `retry_async` |
| 23 | `/home/ludo/Scrivania/SEC/src/monetization/continuous_run.py:305` | `load_used_topics` |
| 24 | `/home/ludo/Scrivania/SEC/src/monetization/continuous_run.py:316` | `save_used_topics` |
| 25 | `/home/ludo/Scrivania/SEC/src/monetization/continuous_run.py:342` | `pick_topic_smart` |
| 26 | `/home/ludo/Scrivania/SEC/src/monetization/continuous_run.py:408` | `boringness_gate` |
| 27 | `/home/ludo/Scrivania/SEC/src/monetization/continuous_run.py:432` | `log_ab_test` |
| 28 | `/home/ludo/Scrivania/SEC/src/monetization/continuous_run.py:507` | `produce_with_validation` |
| 29 | `/home/ludo/Scrivania/SEC/src/monetization/community_posts.py:122` | `pending_posts` |
| 30 | `/home/ludo/Scrivania/SEC/src/monetization/community_posts.py:128` | `mark_posted` |

## 4. Per-System Summary

| System | Files analyzed | Orphan files | Dead public funcs |
|--------|----------------|--------------|-------------------|
| Scrivania/future | 3,115 | 373 | 2701 |
| Scrivania/SEC | 2,838 | 8 | 187 |
| SEC | 156 | 5 | 0 |
| projects | 132 | 13 | 7 |
| kissat | 80 | 5 | 207 |
| tools | 27 | 5 | 26 |

## 5. Notable Orphans - Head Inspection

### `/home/ludo/Scrivania/future/research/research_proof_complexity_20260404_204925/research_proof_complexity_20260404_204925/complexity_research.py` (554 LOC)

Throw-away research scaffold. Functions like `extract_open_questions`, `analyze_complexity`, `find_complexity_barriers` look LLM-generated as a creative exercise rather than real research code. Inline `import re` inside function, hard-coded complexity tables. One-shot prototype under `future/research/`.

### `/home/ludo/Scrivania/future/create/cli_tool_20260413_055245/algorithm_kata_20260413_065514/billing_cycle.py` (342 LOC)

Patch-style file (begins with `--- EDIT:` and `<<<< OLD / >>>> NEW` markers) - looks like a raw diff dumped as .py by mistake, never actually executed. Artifact of an LLM session that produced edit hunks instead of source code.

### `/home/ludo/Scrivania/future/research/research_proof_complexity_20260407_200531/research_proof_complexity_20260407_200531/dictionary_processor.py` (333 LOC)

Starts with a literal triple-backtick markdown fence - this is markdown content saved as .py, will not parse. Definitely dead and likely broken on import. `process_dictionary` / `merge_dictionaries` are toy CRUD utilities.

### `/home/ludo/tools/Wav2Lip/evaluation/real_videos_inference.py` (305 LOC)

Third-party tool: Wav2Lip evaluation script. Standalone CLI (argparse, requires `--mode`, `--checkpoint_path`). Marked orphan because no other corpus file imports `real_videos_inference`, but it is a legitimate entry point for the Wav2Lip vendored repo. Not actually dead - false positive (no `__main__` guard, hence missed by the heuristic).

### `/home/ludo/tools/Wav2Lip/inference.py` (280 LOC)

Same situation: top-level CLI for Wav2Lip. False-positive orphan; this is the user-facing inference entry point. Should keep, but consider adding a `__main__` guard to satisfy the heuristic.

## 6. Methodology Notes

- Corpus: 6,348 .py files concatenated into 21 MB / 601 K lines.
- Orphan check: parsed all 41,169 `import`/`from` statements, extracted every imported leaf segment (2,331 distinct), then tested each candidate basename against that set. Avoids false-positive matches from substrings inside docstrings or strings.
- Dead-function check: single-pass tokenizer `re.findall("\\b\\w+\\s*\\(")` over corpus to count call sites for all 5,634 distinct candidate names; per-file Counters used to subtract self-references.
- Decorator-based framework exclusion uses a broad regex (`route|get|post|put|fixture|task|command|cli|...`) and ALSO excludes any function preceded by any decorator at all (so `@property`, `@staticmethod`, dataclass-generated, attr-validated, etc. are not flagged).
- The `Scrivania/future/` tree dominates findings (373 of 409 orphans, 2,701 of 3,128 dead funcs) - it is a collection of dated LLM-generated practice/research/explore sessions (`*_20260404_*` etc.), almost all of which are intentionally throw-away artefacts and not part of any production pipeline.
- Production-relevant signal lives in `Scrivania/SEC/` (187 dead funcs) and `SEC/` (5 orphans). Worth a manual look:
  - `Scrivania/SEC/src/worker.py` has 6 public functions (`run_kpi_sync`, `run_lit_scout`, `run_weekly_eval`, `run_distill_sample`, `sync_to_main`, `worker_loop`) all flagged dead - suggests `worker.py` is invoked as a script and these helpers are dispatched dynamically (likely via cron/CLI). Verify before deleting.
  - `Scrivania/SEC/src/monetization/continuous_run.py` has 9 dead helpers (`telegram_alert`, `validate_video`, `retry_async`, `load_used_topics`, `save_used_topics`, `pick_topic_smart`, `boringness_gate`, `log_ab_test`, `produce_with_validation`) - strong cleanup candidates IF the module's `__main__` does not reference them via `getattr`.
  - `Scrivania/SEC/src/bridges/tseitin_tw/bridge.py` has 4 dead helpers - bridge code possibly invoked only by a separate test harness.
  - `SEC/src/monetization/sec_revenue.py` and `Scrivania/SEC/src/monetization/sec_revenue.py` (216 LOC each) appear as orphans AND are duplicates - duplicate-file finding for sub-agent 3.
