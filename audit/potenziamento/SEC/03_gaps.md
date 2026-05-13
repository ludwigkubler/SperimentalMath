# SEC vs SOTA — gap analysis

Date: 2026-05-13. Score = Impact × 5 / Effort (higher = better).
Sort: Score desc, ties broken by Impact.

| # | Capability | In SEC? | In SOTA | Sistema SOTA | Impact (1-5) | Effort (1-5) | Score | Note |
|---|------------|---------|---------|--------------|--------------|--------------|-------|------|
| 1 | Reflection (threshold-triggered memory synthesis) | N | Y | Smallville / Park 2023 | 5 | 2 | 12.5 | `scoring.py` + `consolidation.py` exist; just add Park-style `should_reflect()` trigger + summarizer call. |
| 2 | Executable Voyager-style skills (sandboxed code) | Parziale | Y | Voyager (Wang 2023) | 5 | 2 | 12.5 | `skills.py` stores prompt templates only — comment explicitly skips code execution. RestrictedPython + AST whitelist is ~150 LOC. |
| 3 | Reproducible Gym-style benchmark harness | N | Y | Aviary (FutureHouse) | 5 | 2 | 12.5 | Roadmap mandates measurability gates; no harness today. `env.reset/env.step` over conjecture_graph + sample tasks. |
| 4 | OpenTelemetry export (real, not in-process) | Parziale | Y | AutoGen v0.4 / MAF | 4 | 2 | 10 | `observability.py` mimics OTel API; wrap with OTel exporter to Tempo/Jaeger. 1 day. |
| 5 | Agentic tree search over research moves | N | Y | AI Scientist v2 (Sakana) | 5 | 3 | 8.3 | `conjecture_graph.py` is a state machine, not a search tree. Wrap with MCTS-lite over (hypothesis, experiment) nodes. |
| 6 | Task-aware self-verification critic (per agent) | Parziale | Y | Voyager / Reflexion | 4 | 2 | 10 | `learning_hooks` uses single 0.7 threshold; specialize per agent_type with task-shape rubrics. |
| 7 | VLM critic for plots / figures | N | Y | AI Scientist v2 | 3 | 2 | 7.5 | Run MiniCPM-V or Qwen2-VL via Ollama on plot PNGs; flag empty axes / no-legend / saturated. |
| 8 | Automatic curriculum (skill-frontier driven) | Parziale | Y | Voyager | 4 | 3 | 6.7 | `autonomy.py` has MAB but doesn't pick tasks extending existing skills. Roadmap 2 P1 mentions but not wired. |
| 9 | Group-chat / debate orchestration pattern | N | Y | AutoGen | 3 | 2 | 7.5 | `orchestrator.py` is linear pipeline; add SelectorGroupChat for math-vs-skeptic-vs-formalizer triads. |
| 10 | LitQA2-style literature regression benchmark | N | Y | Aviary | 4 | 3 | 6.7 | SEC already has arxiv_mirror, citations, taxonomy — assemble 30 P vs NP QA pairs as gold. |
| 11 | LoRA distillation loop actually running | N (code present, never executed) | n/a | gemma3:4b on RTX 3070 Ti | 5 | 4 | 6.25 | `run_count=0` per roadmap. Operational blocker, not architectural. Schedule + budget. |
| 12 | Plan-tree (hierarchical decomposition) | Parziale | Y | Smallville | 3 | 3 | 5 | Roadmaps/sprints/phases conceptually map to plan-tree; expose as data in `research_loop`. |
| 13 | YouTube Analytics ingestion verified end-to-end | Parziale | n/a | OAuth in place, untested | 4 | 4 | 5 | `kpi_sync.py` exists; cron disabled 2026-04-23. Re-enable + alarm on missing KPIs. |
| 14 | A/B reviewer agent for paper drafts | N | Y | AI Scientist v2 | 3 | 3 | 5 | Extend `pvsnp_reviewer_pack.py` with reviewer-score → revision-diff loop. |
| 15 | Real watchdog (systemd + liveness panic) | Parziale | Y | trans-roadmap debt | 4 | 4 | 5 | `observability.py` has watchdog API; no `/healthz` panic endpoint, no `Restart=always`. |
| 16 | Cross-agent shared OTel trace IDs | N | Y | AutoGen v0.4 | 3 | 3 | 5 | Required for debugging multi-agent flows; tied to #4. |
| 17 | Skill anti-spam dedup confirmed live | Parziale | Y | Voyager | 2 | 2 | 5 | Code exists in `skills.py` but no monitoring of dedup rate; emit metric. |
| 18 | Test coverage ≥ 60% on entity+memory+ml | N | n/a | trans-roadmap debt | 4 | 5 | 4 | Roadmap calls out 0% coverage today; mechanical but slow. |
