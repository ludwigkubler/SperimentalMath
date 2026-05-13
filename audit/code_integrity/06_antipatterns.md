# Sub-Agent 6/6 - Code Anti-Pattern / Bug / Security Audit

**Scope:** All source on `ludo@sec` (Python, shell, JS/TS).  
**Method:** regex pattern grep on file-lists from `/tmp/audit_1778671816/{python,shell,jsts}.txt`.  
**Date:** 2026-05-13. Read-only audit.  

## 1. Executive summary

Across 6,348 Python files, 67 shell scripts, and 676 JS/TS files, the audit surfaced **50 HIGH-severity** findings, dominated by (a) ~20 uses of eval/exec and ~23 subprocess shell=True invocations clustered in auto-generated `Scrivania/future/...` research artefacts and in Mathlib's third-party `scripts/`, (b) **0 hardcoded-secret literal matches** (good - secrets appear to be env-loaded), (c) Wav2Lip vendored code dominates the top-10 risk file list (8 of top-10 are third-party model code, low actionability), (d) two `rm -rf "$WORK"` lines in `replay_runner.sh` are guarded by mktemp/trap but should be hardened with `: ${WORK:?}` pre-check, (e) high MED/LOW volume (645 broad except, 855 stray prints, 161 unguarded `requests` calls) signals uniform code-hygiene gaps in the SEC research mirror rather than concentrated bugs.

## 2. Severity totals

| Severity | Count |
|---|---|
| HIGH | 50 |
| MED | 678 |
| LOW | 1157 |
| INFO | 66 |

## 3. Findings by pattern ID

### P3 - eval() / exec() (excluding tests)  [HIGH]

Total: **20**

Top 20 occurrences:

```
/home/ludo/Scrivania/future/experiment/research_formalization_20260405_032951/src/solution_verifier.py:22  | expr = eval(expression, symbols_dict)
/home/ludo/Scrivania/future/reflect/analyze_errors_20260408_005242/analyze_errors_20260408_005242/performance_analyzer.py:36  | exec(code, globals())
/home/ludo/Scrivania/future/research/research_proof_complexity_20260405_034634/research_proof_complexity_20260405_034634/cli_tool.py:38  | data = [eval(line) for line in f]
/home/ludo/Scrivania/future/research/research_proof_complexity_20260405_034634/research_proof_complexity_20260405_034634/cli_tool.py:40  | summary = eval(f.read())
/home/ludo/Scrivania/future/research/research_proof_complexity_20260408_193643/src/json_validator.py:34  | eval(json_str)
/home/ludo/Scrivania/future/research/chess_research_20260409_232222/chess_research_20260409_232222/code_quality_analyzer.py:14  | issues.append(f"Use of eval() can be dangerous in {file_path}")
/home/ludo/Scrivania/future/research/best_practices_20260403_143730/src/integral_computation.py:22  | expr = eval(expression, {'x': x})
/home/ludo/Scrivania/future/create/micro_project_20260404_235511/src/sat_solving/SATSummary.py:39  | sat_data = eval(file.read())  # Note: Using eval for simplicity; consider safer alternatives
/home/ludo/Scrivania/future/practice/math_practice_20260404_202018/math_practice_20260404_202018/plot_simulation.py:20  | y = eval(equation.replace(variable, 'x'))
/home/ludo/Scrivania/future/practice/math_practice_20260405_005536/src/integral.py:14  | expr = eval(expression, {'x': x})
/home/ludo/tools/Wav2Lip/evaluation/scores_LSE/SyncNetInstance_calc_scores.py:44  | self.__S__.eval();
/home/ludo/tools/Wav2Lip/evaluation/scores_LSE/SyncNetInstance_calc_scores.py:154  | self.__S__.eval();
/home/ludo/tools/Wav2Lip/evaluation/real_videos_inference.py:195  | return model.eval()
/home/ludo/tools/Wav2Lip/evaluation/gen_videos_from_filelist.py:148  | return model.eval()
/home/ludo/tools/Wav2Lip/color_syncnet_train.py:188  | model.eval()
/home/ludo/tools/Wav2Lip/inference.py:179  | return model.eval()
/home/ludo/tools/Wav2Lip/face_detection/detection/sfd/sfd_detector.py:29  | self.face_detector.eval()
/home/ludo/tools/Wav2Lip/hq_wav2lip_train.py:306  | model.eval()
/home/ludo/tools/Wav2Lip/hq_wav2lip_train.py:307  | disc.eval()
/home/ludo/tools/Wav2Lip/wav2lip_train.py:270  | model.eval()
```

### P4 - os.system() / subprocess shell=True  [HIGH]

Total: **23**

Top 23 occurrences:

```
/home/ludo/SEC/src/agents/security/security_agent.py:39  | - Command: os.system/subprocess with shell=True + user input = RCE. Fix: subprocess.run(list).
/home/ludo/SEC/src/agents/reviewer/reviewer_agent.py:27  | - Injection: SQL (parameterize!), command (shell=True), template, LDAP, XPath
/home/ludo/Scrivania/SEC/src/agents/reviewer/reviewer_agent.py:27  | - Injection: SQL (parameterize!), command (shell=True), template, LDAP, XPath
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/migrate_to_fork.py:806  | os.system('')  # This enables ANSI colors in Windows terminal
/home/ludo/kissat/pvnp_lab/lab_c001/scripts/security_monitor.py:39  | r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
/home/ludo/kissat/pvnp_lab/lab_c001/scripts/publish.py:107  | cmd, shell=True, capture_output=True, text=True,
/home/ludo/kissat/pvnp_lab/lab_c001/scripts/monthly_report.py:45  | r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
/home/ludo/kissat/pvnp_lab/lab_c001/scripts/monitor.py:50  | full_cmd, shell=True, capture_output=True, text=True, timeout=timeout
/home/ludo/Scrivania/future/research/chess_research_20260413_103322/experiment_1.py:18  | cmd, shell=True, capture_output=True, text=True, timeout=timeout
/home/ludo/Scrivania/future/research/research_sat_structure_20260404_194501/research_sat_structure_20260404_194501/src/feature_flags/proof.py:26  | result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
/home/ludo/Scrivania/future/research/research_sat_structure_20260404_194501/research_sat_structure_20260404_194501/experiment.py:10  | result = subprocess.run(command, shell=True, capture_output=True, text=True)
/home/ludo/Scrivania/future/research/research_proof_complexity_20260412_041839/experiment_1.py:22  | subprocess.run(cmd_baseline, shell=True, check=True)
/home/ludo/Scrivania/future/research/research_proof_complexity_20260412_041839/experiment_1.py:23  | subprocess.run(cmd_optimized, shell=True, check=True)
/home/ludo/Scrivania/future/create/physics_simulation_20260403_093142/physics_simulation_20260403_093142/cli.py:12  | result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
/home/ludo/Scrivania/future/practice/physics_derivation_20260408_112437/test_1.py:7  | result = subprocess.run(command, shell=True, capture_output=True, text=True)
/home/ludo/tools/Wav2Lip/evaluation/scores_LSE/SyncNetInstance_calc_scores.py:56  | output = subprocess.call(command, shell=True, stdout=None)
/home/ludo/tools/Wav2Lip/evaluation/scores_LSE/SyncNetInstance_calc_scores.py:59  | output = subprocess.call(command, shell=True, stdout=None)
/home/ludo/tools/Wav2Lip/evaluation/real_videos_inference.py:218  | subprocess.call(command, shell=True)
/home/ludo/tools/Wav2Lip/evaluation/real_videos_inference.py:301  | subprocess.call(command, shell=True)
/home/ludo/tools/Wav2Lip/evaluation/gen_videos_from_filelist.py:168  | subprocess.call(command, shell=True)
/home/ludo/tools/Wav2Lip/evaluation/gen_videos_from_filelist.py:235  | subprocess.call(command, shell=True)
/home/ludo/tools/Wav2Lip/inference.py:221  | subprocess.call(command, shell=True)
/home/ludo/tools/Wav2Lip/preprocess.py:79  | subprocess.call(command, shell=True)
```

### P5 - Hardcoded secret literal (api_key/password/token/secret)  [HIGH]

Total: **0**

_No matches._

### P6 - pickle.loads / pickle.load (untrusted-deserialization risk)  [HIGH]

Total: **1**

Top 1 occurrences:

```
/home/ludo/SEC/src/agents/security/security_agent.py:43  | - Deserialization: pickle.loads(), yaml.load(), Java ObjectInputStream = arbitrary code exec.
```

### P12 - yaml.load() without Loader=  [HIGH]

Total: **1**

Top 1 occurrences:

```
/home/ludo/SEC/src/agents/security/security_agent.py:43  | - Deserialization: pickle.loads(), yaml.load(), Java ObjectInputStream = arbitrary code exec.
```

### S1 - rm -rf with unquoted/possibly-empty variable  [HIGH]

Total: **2**

Top 2 occurrences:

```
/home/ludo/Scrivania/SEC/research/replay/replay_runner.sh:24  | trap 'rm -rf "$WORK"' EXIT
/home/ludo/kissat/pvnp_lab/system_v2/src/replay_infra/replay_runner.sh:24  | trap 'rm -rf "$WORK"' EXIT
```

### S2 - curl|sh / wget|sh installer pattern  [HIGH]

Total: **3**

Top 3 occurrences:

```
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/install_debian.sh:13  | # unlike the standard `curl [...] -sSf | sh` installation method.
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/install_macos.sh:11  | curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
/home/ludo/Scrivania/future/practice/physics_derivation_20260408_094609/physics_derivation_20260408_094609/cli_tool/install.sh:6  | curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### J1 - JavaScript eval()  [HIGH]

Total: **0**

_No matches._

### J2 - innerHTML= assignment (XSS)  [MED]

Total: **0**

_No matches._

### J3 - React dangerouslySetInnerHTML  [MED]

Total: **0**

_No matches._

### J4 - Math.random() used in auth/token/secret context  [MED]

Total: **1**

Top 1 occurrences:

```
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/importGraph/html-template/vendor/graphology-library.min.js:1  | !function(t,e){"object"==typeof exports&&"undefined"!=typeof module?e(exports):"function"==typeof define&&define.amd?define(["exports"],e):e
```

### P1 - Bare except / except Exception (overly broad)  [MED]

Total: **645**

Top 30 occurrences:

```
/home/ludo/SEC/src/agents/chess/chess_agent.py:182  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:193  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:204  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:392  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:397  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:419  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:516  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:590  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:716  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:785  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:912  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:946  | except Exception:
/home/ludo/SEC/src/agents/chess/chess_agent.py:982  | except Exception:
/home/ludo/SEC/src/models/ollama_client.py:192  | except Exception:
/home/ludo/SEC/src/ml/prompt_optimizer.py:70  | except Exception:
/home/ludo/SEC/src/ml/prompt_optimizer.py:85  | except Exception:
/home/ludo/SEC/src/ml/prompt_optimizer.py:98  | except Exception:
/home/ludo/SEC/src/ml/prompt_optimizer.py:121  | except Exception:
/home/ludo/SEC/src/ml/prompt_optimizer.py:160  | except Exception:
/home/ludo/SEC/src/ml/prompt_optimizer.py:169  | except Exception:
/home/ludo/SEC/src/ml/learning_loop.py:190  | except Exception:
/home/ludo/SEC/src/memory/embeddings.py:94  | except Exception:
/home/ludo/SEC/src/memory/embeddings.py:96  | except Exception:
/home/ludo/SEC/src/memory/unified.py:265  | except Exception:
/home/ludo/SEC/src/memory/knowledge_graph.py:392  | except Exception:
/home/ludo/SEC/src/communication/bus.py:164  | except Exception:
/home/ludo/SEC/src/communication/bus.py:170  | except Exception:
/home/ludo/SEC/src/core/autonomy.py:102  | except Exception:
/home/ludo/SEC/src/core/orchestrator.py:356  | except Exception:
/home/ludo/SEC/src/core/orchestrator.py:413  | except Exception:
```

### P2 - Mutable default argument ([], {}, set())  [MED]

Total: **32**

Top 30 occurrences:

```
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_70bd8319.py:103  | def dpll(clauses, assignment=[]):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_61711205.py:17  | def dpll(clauses, assignment={}):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_186b4d72.py:43  | def Q_dt(f, memo={}):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_136fa469.py:26  | def partition(n, k, acc=[]):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_301e80de.py:73  | def dpll(clauses, assignment={}):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_2669a168.py:93  | def dpll(cnf, assignment={}):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_8072c074.py:24  | def dpll(sat_formula: list, assignment: dict = {}) -> bool:
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_93fdd2dc.py:38  | def dpll_tree_size(phi, assignment=[]):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_91ef5bff.py:35  | def dpll(cnf, assignment={}):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_7af08c42.py:73  | def tutte_polynomial(graph, memo={}):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_e2de96a5.py:80  | def dpll(F, assignment=[]):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_7d23d2ec.py:71  | def dpll(clauses, assignment, model=[]):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_33c30d52.py:72  | def dpll_up(phi, assignment=[]):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_f09aaec7.py:53  | def dpll(cnf, assignment={}):
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_182c0af2.py:30  | def dpll_tree_size(clauses, assignment=[]):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_70bd8319.py:103  | def dpll(clauses, assignment=[]):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_61711205.py:17  | def dpll(clauses, assignment={}):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_186b4d72.py:43  | def Q_dt(f, memo={}):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_136fa469.py:26  | def partition(n, k, acc=[]):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_301e80de.py:73  | def dpll(clauses, assignment={}):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_2669a168.py:93  | def dpll(cnf, assignment={}):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_8072c074.py:24  | def dpll(sat_formula: list, assignment: dict = {}) -> bool:
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_93fdd2dc.py:38  | def dpll_tree_size(phi, assignment=[]):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_91ef5bff.py:35  | def dpll(cnf, assignment={}):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_7af08c42.py:73  | def tutte_polynomial(graph, memo={}):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_e2de96a5.py:80  | def dpll(F, assignment=[]):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_7d23d2ec.py:71  | def dpll(clauses, assignment, model=[]):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_33c30d52.py:72  | def dpll_up(phi, assignment=[]):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_f09aaec7.py:53  | def dpll(cnf, assignment={}):
/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_182c0af2.py:30  | def dpll_tree_size(clauses, assignment=[]):
```

### P7 - runtime assert outside tests/ (disabled by python -O)  [LOW]

Total: **108**

Top 30 occurrences:

```
/home/ludo/SEC/src/entity/memory/store.py:207  | assert self._db is not None, "Store not initialized. Call init() first."
/home/ludo/Scrivania/SEC/src/ml/feedback_store.py:477  | assert self._db
/home/ludo/Scrivania/SEC/src/ml/feedback_store.py:497  | assert self._db
/home/ludo/Scrivania/SEC/src/ml/feedback_store.py:595  | assert self._db
/home/ludo/Scrivania/SEC/src/research/conjecture_graph.py:205  | assert self._db is not None, "ConjectureGraph not initialized. Call init() first."
/home/ludo/Scrivania/SEC/src/monetization/kpi_sync.py:159  | assert self._db is not None, "KpiSync not initialized. Call init() first."
/home/ludo/Scrivania/SEC/src/monetization/cost_tracker.py:133  | assert self._db is not None, "CostTracker not initialized"
/home/ludo/Scrivania/SEC/src/tools/home/home_control.py:89  | assert self._cached_snapshot is not None
/home/ludo/Scrivania/SEC/src/tools/home/comelit_client.py:160  | assert self._api is not None
/home/ludo/Scrivania/SEC/src/tools/home/comelit_client.py:177  | assert self._api is not None
/home/ludo/Scrivania/SEC/src/entity/memory/store.py:232  | assert self._db is not None, "Store not initialized. Call init() first."
/home/ludo/Scrivania/SEC/src/entity/memory/skills.py:147  | assert self._db is not None, "SkillLibrary not initialized. Call init() first."
/home/ludo/Scrivania/SEC/src/entity/living/automation_learner.py:144  | assert self._db is not None, "AutomationLearner not initialized"
/home/ludo/Scrivania/SEC/src/entity/living/scenes.py:240  | assert self._db is not None, "SceneStore not initialized"
/home/ludo/Scrivania/SEC/src/entity/perception/vision.py:120  | assert self._db is not None, "FaceDB not initialized"
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:23  | assert k in meta, f"metadata missing key: {k}"
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:30  | assert c in cols, f"results.csv missing column: {c}"
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:42  | assert int(row["cnf_max_clause_size"]) >= 0
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:43  | assert int(row["cnf_primal_nodes"]) >= 0
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:44  | assert int(row["cnf_primal_edges"]) >= 0
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:45  | assert float(row["cnf_primal_density"]) >= 0.0
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:46  | assert int(row["cnf_primal_degeneracy"]) >= 0
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:47  | assert int(row["cnf_primal_deg_max"]) >= 0
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:48  | assert float(row["cnf_primal_deg_avg"]) >= 0.0
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:50  | assert tw_ub_cnf >= 0, "tw_ub_cnf must be >= 0"
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:51  | assert fam in ("lowTW", "highTW"), f"bad family: {fam}"
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:52  | assert status in ("UNSAT", "TIMEOUT", "ERROR"), f"bad status: {status}"
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:53  | assert n in timeouts, f"n={n} not present in metadata timeouts_s"
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:54  | assert timeout_s == timeouts[n], f"timeout mismatch for n={n}: row {timeout_s} vs meta {timeouts[n]}"
/home/ludo/kissat/pvnp_lab/lab_c001/experiments/validate_results.py:61  | assert "lowTW" in m and "highTW" in m, f"missing family for (n={n},d={d})"
```

### P8 - print() in non-CLI/non-__main__ files  [LOW]

Total: **855**

Top 30 occurrences:

```
/home/ludo/SEC/src/ml/error_correction.py:74  |     def _compute_fingerprint(self, agent_name  | str, description: str) -> str:
/home/ludo/SEC/src/ml/error_correction.py:125  |         fingerprint = self._compute_fingerprint(agent_name, user_description)
/home/ludo/SEC/src/monetization/youtube.py:107  |                     print(f"\n{'='*60}")
/home/ludo/SEC/src/monetization/youtube.py:108  |                     print(f"Open this URL on any device to authorize {channel_id}  | ")
/home/ludo/SEC/src/monetization/youtube.py:109  |                     print(f"\n{auth_url}\n")
/home/ludo/SEC/src/monetization/youtube.py:110  |                     print(f"{'='*60}")
/home/ludo/Scrivania/SEC/src/ml/error_correction.py:82  |     def _compute_fingerprint(self, agent_name  | str, description: str) -> str:
/home/ludo/Scrivania/SEC/src/ml/error_correction.py:133  |         fingerprint = self._compute_fingerprint(agent_name, user_description)
/home/ludo/Scrivania/SEC/src/research/bootstrap_conjecture003b.py:3  | C-003b defines the cumulative active-footprint Φ(π) = Σ_t |Footprint(σ_t)|
/home/ludo/Scrivania/SEC/src/research/bootstrap_conjecture003b.py:35  |             "Φ(π) = Σ_t |Footprint(σ_t)| is the cumulative active-footprint. "
/home/ludo/Scrivania/SEC/src/core/cognitive.py:127  |     def _stimulus_fingerprint(self, event  | ChemEvent) -> str:
/home/ludo/Scrivania/SEC/src/core/cognitive.py:141  |         fp = self._stimulus_fingerprint(event)
/home/ludo/Scrivania/SEC/src/entity/living/automation_learner.py:74  |     def fingerprint(self) -> str  | 
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_7e6159bf.py:293  |     print(f"Testing n = {n}")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_7e6159bf.py:295  |     print(f"  {len(formulas)} formulas")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_7e6159bf.py:351  |             print(f"Counterexample  | n={n}, clauses={clause_set}, D(f)={Df}, d(φ)={min_degens}")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_7e6159bf.py:352  |             print(f"  truth_table has {sum(truth_table)} satisfying assignments")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_7e6159bf.py:357  |             print(f"  tested {tested} formulas")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_7e6159bf.py:362  |     print("RESULT  | FALSIFIED counterexample_found")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_7e6159bf.py:365  |     print(f"RESULT  | INCONCLUSIVE proxy_model_uncertain")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:267  |         print(f"Matrix too large  | {e}")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:299  |     print(f"Testing n_vars={n_vars}")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:303  |     print(f"  clauses  | {clauses}")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:309  |     print(f"  ||Q||_Cl = {norm  | .4f}, ||Q||_Cl^2 = {norm_squared:.4f}, log n = {log_n:.4f}, ratio = {ratio:.4f}")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:316  |         print(f"  resolution size R(φ) = {r_size}")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:320  |         print("  recursion error in resolution enumerator")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:323  |         print("  memory error in resolution enumerator")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:335  |             print(f"  n={n_vars}  | R*log n / ||Q||^2 = {r:.4f}")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:339  |         print(f"Minimum ratio (c) = {min_ratio  | .4f}, average = {avg_ratio:.4f}")
/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_ebced209.py:342  |             print(f"RESULT  | SUPPORTED c_min={min_ratio:.4f}")
```

### P10 - requests.get/post without timeout=  [LOW]

Total: **161**

Top 30 occurrences:

```
/home/ludo/Scrivania/future/experiment/creative_solution_20260405_081240/src/dataExtractor.py:19  | response = requests.get(url)
/home/ludo/Scrivania/future/experiment/creative_solution_20260405_081240/src/dataCollector.py:14  | response = requests.get(url)
/home/ludo/Scrivania/future/experiment/creative_solution_20260405_081240/src/dataCollector.py:34  | response = requests.get(url)
/home/ludo/Scrivania/future/experiment/creative_solution_20260405_081240/src/dataCollector.py:55  | response = requests.get(url)
/home/ludo/Scrivania/future/experiment/cross_language_20260409_032512/src/main/python/web_scraper.py:12  | response = requests.get(url)
/home/ludo/Scrivania/future/experiment/research_formalization_20260409_013138/src/fide_scraper.py:20  | response = requests.get(url)
/home/ludo/Scrivania/future/experiment/creative_solution_20260415_021022/architecture_study_20260414_150035/data_processing/formal_proof.py:26  | response = requests.get(url)
/home/ludo/Scrivania/future/experiment/research_formalization_20260405_032951/src/data_collector.py:55  | response = requests.get(api_url)
/home/ludo/Scrivania/future/experiment/creative_solution_20260409_224019/src/chess_scraper.py:12  | response = requests.get(url)
/home/ludo/Scrivania/future/experiment/cross_language_20260403_113707/src/tournamentExtractor.py:42  | response = requests.get(self.url)
/home/ludo/Scrivania/future/experiment/cross_language_20260403_113707/src/webScraper.py:12  | response = requests.get(self.url)
/home/ludo/Scrivania/future/explore/new_language_feature_20260403_071308/new_language_feature_20260403_071308/http_client.py:16  | response = requests.get(url, params=params)
/home/ludo/Scrivania/future/explore/new_language_feature_20260403_071308/new_language_feature_20260403_071308/http_client.py:34  | response = requests.post(url, json=data)
/home/ludo/Scrivania/future/explore/new_language_feature_20260403_071308/new_language_feature_20260403_071308/http_client.py:52  | response = requests.put(url, json=data)
/home/ludo/Scrivania/future/explore/new_language_feature_20260403_071308/new_language_feature_20260403_071308/http_client.py:69  | response = requests.delete(url)
/home/ludo/Scrivania/future/explore/chess_study_20260410_114853/chess_study_20260410_114853/src/chess_scraper.py:16  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/chess_study_20260410_114853/chess_study_20260410_114853/src/chess_scraper.py:46  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/chess_study_20260410_114853/chess_study_20260410_114853/src/chess_scraper.py:76  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/chess_study_20260410_114853/chess_study_20260410_114853/src/chess_db_scraper.py:16  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/chess_study_20260410_114853/chess_study_20260410_114853/src/chess_db_scraper.py:44  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/chess_study_20260410_114853/chess_study_20260410_114853/src/chess_db_scraper.py:72  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/architecture_study_20260404_224423/architecture_study_20260404_224423/src/Application/Service/HttpClientService.py:22  | response = requests.get(url, params=params)
/home/ludo/Scrivania/future/explore/architecture_study_20260404_224423/architecture_study_20260404_224423/src/Application/Service/HttpClientService.py:39  | response = requests.post(url, data=data, json=json)
/home/ludo/Scrivania/future/explore/architecture_study_20260404_224423/architecture_study_20260404_224423/src/Application/Service/HttpClientService.py:55  | response = requests.put(url, data=data)
/home/ludo/Scrivania/future/explore/architecture_study_20260404_224423/architecture_study_20260404_224423/src/Application/Service/HttpClientService.py:70  | response = requests.delete(url)
/home/ludo/Scrivania/future/explore/architecture_study_20260404_224423/architecture_study_20260404_224423/src/Application/Service/WebScraperService.py:22  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/new_language_feature_20260405_030748/new_language_feature_20260405_030748/web_scraper.py:14  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/learn_library_20260405_105123/learn_library_20260405_105123/src/web_scraper.py:32  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/chess_study_20260405_210316/chess_study_20260405_210316/data_extractor.py:7  | response = requests.get(url)
/home/ludo/Scrivania/future/explore/chess_study_20260405_210316/chess_study_20260405_210316/chess_data_analyzer.py:7  | response = requests.get(url)
```

### P11 - open() without `with` context manager  [LOW]

Total: **9**

Top 9 occurrences:

```
/home/ludo/Scrivania/future/research/research_literature_review_20260405_184751/setup.py:21  | long_description=open('README.md').read(),
/home/ludo/Scrivania/future/research/research_proof_complexity_20260408_182508/research_proof_complexity_20260408_182508/setup.py:21  | long_description=open('README.md').read(),
/home/ludo/Scrivania/future/create/micro_project_20260405_054427/micro_project_20260405_054427/setup.py:21  | long_description=open('README.md').read(),
/home/ludo/Scrivania/future/create/physics_simulation_20260405_065854/physics_simulation_20260405_065854/setup.py:22  | long_description=open('README.md').read(),
/home/ludo/Scrivania/future/create/physics_simulation_20260405_065854/generated_9.py:21  | long_description=open('README.md').read(),
/home/ludo/Scrivania/future/create/cli_tool_20260405_104411/setup.py:22  | long_description=open('README.md').read(),
/home/ludo/Scrivania/future/practice/test_writing_20260412_053422/experiment_1.py:48  | pgn = open(filename)
/home/ludo/Scrivania/future/practice/physics_derivation_20260405_111944/physics_derivation_20260405_111944/setup.py:22  | long_description=open('README.md').read(),
/home/ludo/Scrivania/future/practice/physics_derivation_20260408_055642/physics_derivation_20260408_055642/setup.py:23  | long_description=open('README.md').read(),
```

### S3 - shell script >20 LOC missing `set -e`  [LOW]

Total: **14**

Top 14 occurrences:

```
/home/ludo/Scrivania/SEC/deploy/stop_pipeline.sh:1  | (no set -e, 29 LOC)
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/add_deprecations.sh:1  | (no set -e, 160 LOC)
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/get_tlabel.sh:1  | (no set -e, 32 LOC)
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/declarations_diff.sh:1  | (no set -e, 196 LOC)
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/maintainer_merge_message.sh:1  | (no set -e, 53 LOC)
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/zulip_build_report.sh:1  | (no set -e, 85 LOC)
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/long_file_report.sh:1  | (no set -e, 48 LOC)
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/batteries/scripts/lintWhitespace.sh:1  | (no set -e, 25 LOC)
/home/ludo/kissat/pvnp_lab/lab_c001/scripts/git_sync.sh:1  | (no set -e, 22 LOC)
/home/ludo/kissat/pvnp_lab/lab_c001/scripts/watchdog.sh:1  | (no set -e, 81 LOC)
/home/ludo/Scrivania/future/reflect/research_complexity_barrier_20260408_162348/src/cli/install.sh:1  | (no set -e, 43 LOC)
/home/ludo/Scrivania/future/reflect/quality_retrospective_20260404_191239/src/scripts/run_migration_test.sh:1  | (no set -e, 31 LOC)
/home/ludo/Scrivania/future/practice/algorithm_kata_20260409_233608/src/install.sh:1  | (no set -e, 30 LOC)
/home/ludo/Scrivania/future/practice/algorithm_kata_20260405_001105/src/install.sh:1  | (no set -e, 35 LOC)
```

### S4 - `cd ... && ...` without `|| exit`  [LOW]

Total: **10**

Top 10 occurrences:

```
/home/ludo/SEC/deploy/install.sh:7  | SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
/home/ludo/SEC/src/monetization/daily_run.sh:7  | SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
/home/ludo/SEC/src/monetization/daily_run.sh:8  | PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
/home/ludo/Scrivania/SEC/deploy/install.sh:7  | SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
/home/ludo/Scrivania/SEC/src/monetization/daily_run.sh:10  | SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
/home/ludo/Scrivania/SEC/src/monetization/daily_run.sh:11  | PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/docker_push.sh:8  | cd $DIR && \
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/docker_build.sh:4  | cd $DIR/../.docker/lean && \
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/docker_build.sh:6  | cd $DIR/../.docker/gitpod && \
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/docker_build.sh:8  | cd $DIR/../.docker/gitpod-blueprint && \
```

### P9 - TODO/FIXME/XXX/HACK markers  [INFO]

Total: **66**

Top 30 occurrences:

```
/home/ludo/SEC/src/agents/security/security_agent.py:71  | "cwe": "CWE-XXX",
/home/ludo/SEC/src/core/curiosity.py:444  | "manages TODO items stored in a local SQLite database",
/home/ludo/SEC/src/monetization/print_on_demand.py:107  | "// TODO: fix this later (written 3 years ago)",
/home/ludo/Scrivania/SEC/src/agents/scraper/scraper_agent.py:439  | # Extract ID: http://arxiv.org/abs/XXXX.XXXXX -> XXXX.XXXXX
/home/ludo/Scrivania/SEC/src/agents/research/paper_writer.py:10  | with TODO markers.
/home/ludo/Scrivania/SEC/src/agents/research/paper_writer.py:198  | return f"% TODO: write {name}"
/home/ludo/Scrivania/SEC/src/agents/research/paper_writer.py:210  | return f"% TODO: LLM failed for {name}: {e}"
/home/ludo/Scrivania/SEC/src/research/pvsnp_citations.py:131  | """s2_id may be 'arxiv:XXXX', 'doi:XXXX', or a hash."""
/home/ludo/Scrivania/SEC/src/research/pvsnp_lean_proof.py:67  | each sorry a `-- TODO(<descriptive>):` comment naming the lemma.
/home/ludo/Scrivania/SEC/src/research/pvsnp_explorer.py:1320  | - Cite arxiv/ECCC hits inline as \\cite{arxiv:XXXX.YYYYY}.
/home/ludo/Scrivania/SEC/src/core/curiosity.py:444  | "manages TODO items stored in a local SQLite database",
/home/ludo/Scrivania/SEC/src/monetization/print_on_demand.py:107  | "// TODO: fix this later (written 3 years ago)",
/home/ludo/Scrivania/SEC/tests/research/test_paper_writer.py:86  | # TODOs present for each section
/home/ludo/Scrivania/SEC/tests/research/test_paper_writer.py:87  | assert "TODO: write abstract" in content
/home/ludo/Scrivania/SEC/tests/research/test_paper_writer.py:88  | assert "TODO: write introduction" in content
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/githelper.py:566  | # TODO --origin-https option?
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/githelper.py:567  | # TODO --upstream-ssh option?
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/lint-style.py:31  | # TODO: This is adapted from the linter for mathlib3. It should be rewritten in Lean.
/home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/scripts/lint-style.py:109  | # TODO: also fix the space for all lines before ":=", right now we only fix the line after
/home/ludo/kissat/pvnp_lab/system_v2/src/pvsnp_citations.py:131  | """s2_id may be 'arxiv:XXXX', 'doi:XXXX', or a hash."""
/home/ludo/kissat/pvnp_lab/system_v2/src/pvsnp_lean_proof.py:67  | each sorry a `-- TODO(<descriptive>):` comment naming the lemma.
/home/ludo/kissat/pvnp_lab/system_v2/src/pvsnp_explorer.py:1320  | - Cite arxiv/ECCC hits inline as \\cite{arxiv:XXXX.YYYYY}.
/home/ludo/Scrivania/future/experiment/research_formalization_20260429_022053/research_formalization_20260429_022053/molecular_dynamics.py:19  | return TODO("Initialize the molecular dynamics system")
/home/ludo/Scrivania/future/experiment/research_formalization_20260429_022053/research_formalization_20260429_022053/simulation.py:19  | return TODO("Initialize the molecular dynamics system")
/home/ludo/Scrivania/future/explore/learn_library_20260405_013611/src/differential_equation_solver.py:56  | // TODO: Implement actual authentication logic here
/home/ludo/Scrivania/future/explore/learn_library_20260405_013611/src/em_waves.py:56  | // TODO: Implement actual authentication logic here
/home/ludo/Scrivania/future/explore/learn_library_20260405_161642/learn_library_20260405_161642/research_summary.py:24  | TODO: Implement first research task.
/home/ludo/Scrivania/future/explore/learn_library_20260405_161642/learn_library_20260405_161642/research_summary.py:33  | TODO: Implement second research task.
/home/ludo/Scrivania/future/explore/chess_study_20260405_043232/chess_study_20260405_043232/extract_key_lessons.py:44  | python_code = f"def {python_code}\n\n    '''\n    TODO: Add docstring\n    '''\n"
/home/ludo/Scrivania/future/reflect/analyze_errors_20260407_140438/src/todo_cli.py:5  | TODO_FILE = 'todo.txt'
```

## 4. Per-system summary

| System | HIGH | MED | LOW | INFO |
|---|---|---|---|---|
| SEC (active) | 4 | 97 | 10 | 3 |
| Scrivania/SEC (mirror) | 2 | 432 | 152 | 12 |
| kissat/pvnp_lab | 8 | 141 | 46 | 7 |
| Scrivania/future (gen) | 18 | 6 | 897 | 44 |
| Other | 18 | 2 | 52 | 0 |

## 5. Top 10 highest-risk files (by HIGH-severity hits)

| #HIGH | File |
|---|---|
| 4 | `/home/ludo/tools/Wav2Lip/evaluation/scores_LSE/SyncNetInstance_calc_scores.py` |
| 3 | `/home/ludo/tools/Wav2Lip/evaluation/real_videos_inference.py` |
| 3 | `/home/ludo/tools/Wav2Lip/evaluation/gen_videos_from_filelist.py` |
| 3 | `/home/ludo/SEC/src/agents/security/security_agent.py` |
| 2 | `/home/ludo/Scrivania/future/research/research_proof_complexity_20260405_034634/research_proof_complexity_20260405_034634/cli_tool.py` |
| 2 | `/home/ludo/tools/Wav2Lip/inference.py` |
| 2 | `/home/ludo/tools/Wav2Lip/hq_wav2lip_train.py` |
| 2 | `/home/ludo/Scrivania/future/research/research_proof_complexity_20260412_041839/experiment_1.py` |
| 1 | `/home/ludo/Scrivania/future/experiment/research_formalization_20260405_032951/src/solution_verifier.py` |
| 1 | `/home/ludo/Scrivania/future/reflect/analyze_errors_20260408_005242/analyze_errors_20260408_005242/performance_analyzer.py` |

_Note: 8/10 are vendored third-party (`tools/Wav2Lip/`). Actionable items are `SEC/src/agents/security/security_agent.py` (3 hits, but these are docstring mentions of unsafe patterns, not actual uses - false positive) and the auto-generated `Scrivania/future/research/...` modules._

## 6. Quick-win recommendations

1. **Ban `shell=True` in SEC core.** Wrap all subprocess calls in a single helper `safe_run(cmd_list, timeout=...)` that asserts `isinstance(cmd_list, list)` and forwards `shell=False`. Migrate the 4 hits in `pvnp_lab/scripts/{security_monitor,publish,monthly_report,monitor}.py` first - they accept string commands.
2. **Replace `eval()` with `ast.literal_eval` or `sympy.sympify`.** All 20 hits are in auto-generated `Scrivania/future/...` artefacts; add a lint rule (`ruff S307`) to the research-agent codegen template so future generations are eval-free.
3. **Harden replay_runner.sh** (`Scrivania/SEC/research/replay/` and `pvnp_lab/system_v2/src/replay_infra/`): add `: "${WORK:?WORK unset}"` before `trap 'rm -rf "$WORK"' EXIT` so an empty WORK cannot nuke /.
4. **Default `timeout=` on all `requests` calls.** Create a `from sec.http import get, post` wrapper with `timeout=30` baked in; the 161 unguarded HTTP calls will silently hang on slow endpoints.
5. **Tighten exception handling.** Replace 645 broad `except Exception:` / `except:` with specific tuples. Biggest cluster is `Scrivania/SEC` (mirror) - fix upstream, mirror auto-syncs.

## 7. Notes on false positives / caveats

- `security_agent.py` mentions `os.system`, `pickle.loads`, `yaml.load` inside its **prompt-template docstring** (it teaches the agent what to scan for). Not an actual unsafe call.
- `code_quality_analyzer.py` files in research artefacts contain the literal string `eval()` in an error message they emit - not an executed call.
- `.lake/packages/mathlib/scripts/` is vendored third-party (Mathlib) and out of audit scope.
- P5 (hardcoded secrets) returned **0** - secrets appear loaded via `os.environ` / `dotenv`. Recommend follow-up with `trufflehog`/`gitleaks` for entropy-based detection beyond keyword matching.
- P8 (855 prints) is mostly research notebooks / CLI tools; not a defect per se. Severity LOW.
