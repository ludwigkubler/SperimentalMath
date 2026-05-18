# AS-IS Architecture — Module Inventory

Date: 2026-05-18
Author: Explore subagent (delegated by coordinator Claude)
Repository: ~/Scrivania/SEC

---

## A. Research Modules (~/Scrivania/SEC/src/research/)

Total LOC: 13,158 across 33 files.

### pvsnp_barriers.py (608 LOC)
- Purpose: Multi-stage barrier filter (relativization/natural-proof/algebrization); rejects conjectures via dual-LLM confirmation.
- Triggers: Called by pvsnp_explorer each cycle.
- Reads: None (stateless).
- Writes: pvsnp_barriers_rejected.jsonl.
- Key external imports: asyncio, json, re.
- Key src.* deps: src.orchestration.router, src.entity.pvsnp_capabilities.
- Key data structures: BarrierFilterResult(verdict, confidence, checks_log).
- Public entry points: async def barrier_filter(conjecture: dict) -> BarrierFilterResult.
- Algorithm: Two-stage LLM evaluation; HITS only if both confirm with confidence >= 0.6.
- Failure modes: Loud (JSON parse); LLM timeout propagates.

### pvsnp_compute.py (534 LOC)
- Purpose: Invokes kissat SAT solver on generated instances; Layer 4 of skeptic gate.
- Triggers: CLI --sweep or --run-target; cron 23 0,12 * * *.
- Reads: linkage_graph nodes; generates DIMACS via cnf_encoders.
- Writes: research/compute_evidence/<node_id>_<date>.json (kissat metrics).
- Key external imports: subprocess, tempfile, statistics.
- Key src.* deps: src.research.conjecture_graph, cnf_encoders.
- Key data structures: KissatResult(sat, runtime_s, n_vars, n_clauses, conflicts, decisions).
- Public entry points: async def compute_evidence_for_node(node_id: str).
- Algorithm: Regex parsing of kissat output; scaling deviation > 3 sigma triggers DOWNGRADE.
- Failure modes: Loud (kissat missing/timeout).

### pvsnp_lean_counterexample.py (498 LOC)
- Purpose: Formalizes refutation counterexamples in Lean 4; generates self-contained proofs.
- Triggers: After FALSIFIED+CONFIRM verdict.
- Reads: notebook entries (FALSIFIED+CONFIRM), seed_results.
- Writes: research/lean_counterexamples/{entry_id}.lean, pvsnp_lean_counterexample_log.jsonl.
- Key external imports: subprocess, tempfile, asyncio.
- Key src.* deps: src.orchestration.routed_llm (Opus).
- Algorithm: LLM generates Lean stub; lake build; on error, retry up to 2x; 30 min budget/entry.
- Failure modes: Loud (lake compile errors logged).

### pvsnp_lean_gate.py (471 LOC)
- Purpose: Transforms SUPPORTED+CONFIRM into Lean theorems; attempts mechanically-verified proofs.
- Triggers: After SUPPORTED_HARDENED verdict.
- Reads: notebook (SUPPORTED+CONFIRM); Mathlib4.
- Writes: research/pvsnp_verified/{entry_id}.lean, pvsnp_lean_gate_log.jsonl.
- Algorithm: Tier-1 (decide/rfl) -> Tier-2 (exact?/loogle) -> Tier-3 (LLM+goal feedback); 1800s budget.
- Failure modes: Loud (compile errors); produces Lean with sorrys; sorry-count is research data.

### pvsnp_lean_proof.py (354 LOC)
- Purpose: Attempts formal PROOF of SUPPORTED conjectures; target mix: 1-5% full, 10-20% partial, 75-90% sorry.
- Triggers: After SUPPORTED_HARDENED.
- Writes: research/lean_proofs/{entry_id}.lean, pvsnp_lean_proof_log.jsonl.
- Algorithm: LLM prioritizes native_decide, norm_num, simp, linarith, aesop; honest sorrys for non-decidable.

### pvsnp_linkage_graph.py (463 LOC)
- Purpose: DAG of atomic claims (Lean theorems/sorry stubs) with logical dependencies; discovers frontier.
- Triggers: Cron 31 */4 * * * (refresh every 4h).
- Reads: notebook (compiled Lean), linkage_graph nodes/edges.
- Writes: research/linkage_graph/nodes.jsonl, edges.jsonl, graph.dot.
- Algorithm: Seeds with TARGET_* nodes (P!=NP, AC0/PARITY, monotone CLIQUE); LLM infers new edges.

### pvsnp_taxonomy.py (277 LOC)
- Purpose: Curated catalog of 60 research approaches; samples weighted-random approach; adjusts weights by outcomes.
- Triggers: Cron 0 */6 * * * (reweight every 6h).
- Reads: research/pvsnp_taxonomy.yaml, notebook.
- Algorithm: Productivity decay on BARRIER_HIT/INCONCLUSIVE; WEIGHT_CLAMP = [0.1, 3.0].

### pvsnp_problem_focus.py (260 LOC)
- Purpose: Rotation through 8 well-known lower-bound targets (AC0/PARITY, MONOTONE/CLIQUE, etc.); 60% cycles focus-mode.
- Reads: None (static in-memory list).
- Algorithm: Round-robin with 60/40 bias; biases proposer toward tractable sub-targets.

### pvsnp_arxiv_mirror.py (355 LOC)
- Purpose: Offline local arxiv mirror with semantic search; fetches from 7 categories; embeds via nomic-embed-text.
- Triggers: Cron 11 2,10,18 * * * (3x/day).
- Reads: arxiv API, Ollama embedding service.
- Writes: research/arxiv_mirror.sqlite (papers table), arxiv_mirror_state.json.
- Data structures: SQLite papers(id, primary_category, title, abstract, authors, submitted_at, embedding[768]).

### pvsnp_citations.py (387 LOC)
- Purpose: For each novelty_hit, LLM judges if paper SUPPORTS/REFUTES/ORTHOGONAL/INSUFFICIENT.
- Reads: notebook (novelty_hit), S2 API or arxiv mirror (abstract).
- Writes: research/citations/{entry_id}.json (judge verdicts).

### pvsnp_reviewer_pack.py (361 LOC)
- Purpose: Self-contained PDF reviewer pack per entry: statement, preregistration, novelty audit, test code, results, critic review, audit log.
- Triggers: CLI --entry/--all-supported/--since.
- Reads: notebook, preregistrations, citations, audit logs.
- Writes: research/reviewer_packs/{entry_id}.pdf.
- Algorithm: Markdown to PDF via pandoc/xelatex.

### pvsnp_few_shot.py (283 LOC)
- Purpose: Curates top-K examples (FALSIFIED+Lean, SUPPORTED_HARDENED, INCONCLUSIVE) for proposer few-shot.
- Triggers: Cron 33 2 * * 0 (Sunday 02:33).
- Writes: research/few_shot_examples.md (injected into proposer prompt).
- Algorithm: Tier-1 (FALSIFIED+Lean) through Tier-4; anonymizes details.

### pvsnp_reflection.py (398 LOC)
- Purpose: Daily reflection + scoop detection; flags papers with cosine similarity > 0.72 vs conjecture embeddings.
- Triggers: Cron 33 3 * * * (daily 03:33).
- Writes: research/daily_reflection/daily_{date}.md.
- Algorithm: Cosine similarity; empirically calibrated SCOOP_THRESHOLD = 0.72.

### pvsnp_review_alert.py (251 LOC)
- Purpose: Weekly digest of SUPPORTED_HARDENED entries; sends review prompt Monday 09:13.
- Triggers: Cron 13 9 * * 1.

### pvsnp_sec_bridge.py (258 LOC)
- Purpose: Bridge between SEC entity and pvsnp_explorer; returns markdown context (cycles, Lean refutations, kissat sweeps) for entity to quote.
- Triggers: Called by entity.conversation.context_builder each chat (~50ms).
- Reads: notebook tail, health_report.json, daily_reflection, linkage_graph.
- Writes: None (ephemeral context).
- Algorithm: Formats markdown sections; truncates to 2400 chars.

### pvsnp_weekly_replay.py (188 LOC)
- Purpose: Weekly replay (Sunday 03:00): picks N random entries from past 7 days; detects drift.
- Triggers: Cron 0 3 * * 0.
- Writes: research/weekly_replay/weekly_{date}.json (drift report).

### pvsnp_audit.py (196 LOC)
- Purpose: Thread-local audit context; records every LLM call (provider, model, tokens, latency).
- Triggers: Called on each LLM invocation.
- Writes: research/audit/{entry_id}.jsonl (append-only).
- Algorithm: Thread-local contextvars; atomic append with file lock.

### conjecture_graph.py (445 LOC)
- Purpose: SQLite-backed DAG of conjectures and obligations; state machine for conjecture status.
- Triggers: Seeded by seed_conjectures.py; used by external agents.
- Reads/Writes: entity.db (conjectures, obligations tables).
- Data structures: Conjecture(id, statement_nl, status, confidence), Obligation(type, status, agent_assigned).

### cnf_encoders.py (260 LOC)
- Purpose: CNF encoders for Tseitin formulas on arbitrary graphs; encodes XOR equations as SAT clauses.
- Reads: None (pure computation).
- Writes: None (returns CNF in memory).
- Algorithm: Expands XOR per vertex into 2^(degree-1) clauses; cap degree at 20.

### seed_conjectures.py (216 LOC)
- Purpose: Idempotent seeding of conjecture graph with Ludos active research (C-001, C-003b).
- Triggers: CLI invocation (one-time).
- Writes: entity.db (conjectures, obligations).

### bootstrap_conjecture001.py (204 LOC)
- Purpose: Bootstrap test harness for C-001 (Tseitin hardness); empirical test on small n <= 40.

### bootstrap_conjecture003b.py (187 LOC)
- Purpose: Bootstrap test harness for C-003b (cumulative entropy); measures proof entropy.

---

## B. ENTITY Runtime (~/Scrivania/SEC/src/entity/) — 17,967 LOC across 61 files

### Core (core.py, 434 LOC)
- Purpose: Central DigitalEntity singleton; orchestrates all subsystems (memory, cognition, autonomous, code access, network).
- Triggers: Instantiated once at startup.
- Key data structures: DigitalEntity singleton with ~15 subsystems as attributes.

### Conversation (command_router.py 1,265 LOC, chat.py 511 LOC, context_builder.py 696 LOC, intent.py 323 LOC)
- command_router: Parses user input into intent+arguments; routes to handler.
- chat: Main loop; builds context, injects prompts, logs to entity.db.
- context_builder: Assembles system prompt from identity, memory, emotions, research, autonomy.
- intent: Intent classification (~30 types); entity extraction.

### Memory (store.py 796 LOC, dreamscape.py 449 LOC, skills.py 333 LOC, consolidation.py 325 LOC, bridge.py ~180 LOC)
- store: Central episodic+semantic store; SQLite FTS5; semantic search via embeddings.
- dreamscape: Dream narrative during deep idle (2+ hrs no interaction).
- skills: Skill registry; tracks tool reuse rate (target > 30%).
- consolidation: STM -> LTM periodic extraction of insights.
- bridge: Syncs entity.db <-> memory/knowledge_graph.db.

### Cognition (empathy.py 403 LOC, growth.py 323 LOC, thought_generator.py 322 LOC, values.py, question_engine.py, arbiter.py)
- empathy: Detects user emotion; adjusts response tone.
- growth: Tracks learning progress; skill acquisition metrics.
- thought_generator: Inner monologue; chain-of-thought during idle.
- values: Core values system (honesty, privacy, autonomy).
- question_engine: Generates curious questions for user.
- arbiter: Multi-objective decision arbitration.

### Living (autonomous.py 1,482 LOC, self_improve.py 863 LOC, home_automation.py 664 LOC, code_access.py 499 LOC, tool_executor.py 428 LOC, confirmation.py 339 LOC, scenes.py 330 LOC, network_discovery.py 317 LOC)
- autonomous: Master 5-min loop; drives via (curiosity, competence, exploration, protection); kept 7 actions (pursue_obligation 95% success, consolidate, explore_web, self_improve, learn, research_topic, fix_error).
- self_improve: Self-modifying; audits own code; proposes patches; tests and applies if pass.
- home_automation: Smart home via Comelit API (lights, doors, alarm).
- code_access: Safe sandbox execution (timeout, resource limits, permissions).
- tool_executor: Orchestrates tool invocation with retries.
- confirmation: Safety gate; prompts for dangerous actions.
- scenes: Narrative scenes (sleeping, working, resting); adjusts autonomy per scene.
- network_discovery: LAN ARP scans; logs new devices.

### Proactivity (triggers.py 336 LOC)
- Purpose: Event-driven rules; if-then automation.

### API (routes.py 335 LOC, backup.py 329 LOC)
- routes: FastAPI REST endpoints (/chat, /status, /action).
- backup: Backup/restore entity state to versioned JSON snapshots.

### Learning (reflexion.py ~210 LOC)
- Purpose: Reflection on past performance; reviews code patches, skill use; generates lessons.

### Capabilities
- pvsnp_capabilities.py (420 LOC): Interface to pvsnp_explorer state; query conjecture status, propose conjectures, search papers.

---

## C. Orchestration (~/Scrivania/SEC/src/orchestration/) — 1,949 LOC

### router.py (441 LOC)
- Purpose: Multi-provider LLM router; selects provider (Claude Max, Ollama, Groq, Mistral, Google, etc.) by task type.
- Task types: CODING, REASONING, REVIEW, DOCS, SECURITY, CONVERSATION, GENERAL.
- Algorithm: Checks provider status; selects from chain per task; round-robins on equal quality.

### routed_llm.py (159 LOC)
- Purpose: High-level wrapper; retries, token counting, cost estimation.

### providers/ (8 major implementations + 4 stubs)
- base.py (217): Abstract interface.
- claude_max.py (335): Claude API (Anthropic); highest quality, most expensive.
- ollama.py (179): Local Ollama; used for embedding, light reasoning, cost-free fallback.
- google.py (167): Gemini API.
- Others (groq, mistral, cerebras, sambanova, together, fireworks, deepinfra, openrouter): <65 LOC each.

---

## D. Tools (~/Scrivania/SEC/src/tools/) — 2,976 LOC

- system_info.py (557): System introspection (CPU, memory, disk, processes).
- literature.py (287): Literature search (S2, arxiv, ECCC); abstract fetch.
- web_search.py (249): DuckDuckGo web search.
- web.py (202): General HTTP fetch + HTML parsing.
- sat.py (249): SAT utilities; CNF representation, DIMACS I/O.
- lean.py (172): Lean 4 integration; lake invocation.
- package_manager.py (267): Dependency resolution (pip, cargo, etc.).
- home/ (298+252+43 LOC): Comelit smart home client.
- shell.py (374): Shell execution (skipped per constraints).

---

## E. Other Top-Level src/ Subdirs

- agents/ (6,971 LOC): chess_agent (1,288), scraper_agent (559), others <300.
- bridges/ (388 LOC): tseitin_tw bridge (388) to Lean project TseitinTw.
- communication/ (497 LOC): bus.py (294), notifier.py (203) — pub/sub, desktop alerts.
- core/ (6,328 LOC): research_loop.py (902), curiosity.py (739) — main loop, novelty/barrier/test/critic.
- evaluation/ (290 LOC): weekly_eval.py — audit system health.
- memory/ (2,183 LOC): knowledge_graph.py (657), unified.py (424) — FTS5 graph DB.
- ml/ (5,326 LOC): app.py (1,056), feedback_store.py (669) — inference server, feedback loop.
- models/ (335 LOC): ollama_client.py (193), router.py (142).
- monetization/ (12,892 LOC): DISABLED 2026-04-23; script_generator.py (1,197), content_factory.py (1,017) — video generation (SD-WebUI).
- monitor/ (155 LOC): monitor_cli.py — status display.
- security/ (0 LOC): Placeholder; checks done inline.
- storage/ (243 LOC): database.py — thin ORM.
- web/ (1,324 LOC): app.py — Flask; /chat, /status, /action, WebSocket.

---

## F. Data Model Schemas

### NotebookEntry
entry_id (str), ts (float), phase (str), title, field_A, field_B, statement, rationale, novelty_queries, novelty_hits, novelty_verdict, test_code, test_stdout, test_returncode, test_elapsed_s, final_verdict, final_reason, embedding (768-dim), preregistration_hash, acceptance_criterion, seed_results (list), aggregate_stats (dict), critic_verdict, critic_reasoning, parent_entry_id, mutation_type, paper_path, lean_stub_path.

### Framework
framework_id, ts, generation, parent_framework_id, mutation_from_parent, name, taxonomy_category, primitives, operations, target_invariant, axioms_tentative, status (PROPOSED|ELABORATING|EVALUATED|PROMOTED|PUBLISHED|DEAD|SUSPENDED), sub_conjecture_entry_ids, fitness_components, fitness, paper_path, lean_module_path.

### Refutation
entry_id, title, field_A, field_B, statement, rationale, counterexample, test_code_snippet, lean_file, lean_compiled, timestamp.

### retractions.json
{
  "_meta": {audit_document, audit_date, audit_author, schema_version},
  "retracted": [{entry_id, original_verdict, title, reason, action: "RETRACTED"}]
}

---

## G. Runtime DBs

- ~/data/sec.db: projects, tasks, messages, agent_metrics (task queue, agent communication).
- ~/data/entity/entity.db: identity, episodes, diary, long_term (SEC persistence).
- ~/data/memory/knowledge_graph.db: nodes (FTS5), edges (unified KG).
- ~/data/sec_learning.db: task_feedback, prompt_history, error_patterns, knowledge_base (ML feedback loop).
- ~/Scrivania/SEC/research/arxiv_mirror.sqlite: papers (id, primary_category, title, abstract, authors, submitted_at, embedding[768]).

---

## H. Cron Map (24 active jobs)

*/5 * * * * | pvsnp_explorer watchdog | pvsnp_explorer.log
*/5 * * * * | sec_watchdog.py | watchdog.log, STATUS.md
*/30 * * * * | pvsnp_monitor | monitor.log
*/5 * * * * | entity solar_schedule | solar_schedule.log
0 3 * * * | monetization cleanup | (DISABLED)
0 3 * * 0 | pvsnp_weekly_replay | weekly_replay.json
0 4 * * 0 | pvsnp_compendium | compendium.log
11 2,10,18 * * * | pvsnp_arxiv_mirror --update | arxiv_mirror.sqlite
13 9 * * 1 | pvsnp_review_alert | review_alert.log
17 * * * * | system_v2 sync | sync.log
17 */6 * * * | sec_healthcheck.sh | healthcheck.log
23 0,12 * * * | pvsnp_compute --sweep | compute_evidence/*.json
31 */4 * * * | pvsnp_linkage_graph --refresh | linkage_graph/*.jsonl
33 2 * * 0 | pvsnp_few_shot --regenerate | few_shot_examples.md
33 3 * * * | pvsnp_reflection | daily_reflection/daily_*.md
0 */6 * * * | pvsnp_taxonomy --reweight | taxonomy_reweight.log
0 */6 * * * | entity self_improve --tick | self_improve.log
41 * * * * | pvsnp_sec_diary | entity.db diary
47 * * * * | SperimentalMath sync_output.sh | sync.log

---

## I. Running Processes

PID 925 (02:22): /home/ludo/Scrivania/SEC/.venv/bin/python -m src gui --host 100.65.109.125 --port 8420 --with-daemon
PID 945 (02:22): python launch.py --api --nowebui (Stable Diffusion WebUI, port 7860)
PID 1868 (00:41): /home/ludo/Scrivania/SEC/.venv/bin/python -m src research --config config/research_gpu.yaml --max-cycles 200

---

## Summary

- Total modules: 122+ (33 research, 61 entity, 17 orchestration, 13 tools, 10+ other)
- Total LOC: ~54,000
- Active DBs: 5
- Cron jobs: 24
- External APIs: arxiv, S2, DuckDuckGo, Comelit, Ollama, Claude (Anthropic), 12+ LLM providers
- Key decision: Research disabled monetization 2026-04-23 for P vs NP focus; pruned 0-artifact entity actions.
