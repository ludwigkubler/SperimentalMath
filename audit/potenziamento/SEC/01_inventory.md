# SEC — Inventory (read-only audit)

Date: 2026-05-13. Source: `ssh ludo@sec ~/Scrivania/SEC/`.

## Identity
- Name in README: "Software Engineering Crew" (SEC) but roadmap renames it **Sentient Entity Computer**.
- Author: Ludovico Kubler. Python 3.11+. `pyproject.toml` package name `sec-agents` v0.1.0.
- Entry points: `src/__main__.py`, `src/cli.py`, `src/monetization/cli.py`. Console script `sec = src.cli:main`.
- Code volume: ~95 .py files (per SEC_REPORT.md), ~25.5k LOC. Living/core/ml subset alone = 17.7k LOC.
- Local model: gemma3:4b on Ollama; remote GPU provider configured (RTX 3070 Ti via LAN).
- Server path: `~/Scrivania/SEC/` (NOT `~/SEC/` which is leftover).

## High-level architecture
SEC unifies four "souls" (per `roadmap/00_README.md`):
1. **Researcher** (P vs NP) — `src/research/` 33 files, `src/core/research_loop.py` (902 LOC).
2. **Sentient entity** — `src/entity/` with cognition, perception, conversation, living, memory, learning, proactivity.
3. **Revenue/content** — `src/monetization/` ~40 modules incl. video, blog, ebook, POD, stock media.
4. **Companion** — home automation (Comelit), STT/TTS, presence detection (Roadmap 4, partly stub).

## Module map (key files, with line counts)
```
src/
  agents/{architect,coder,reviewer,tester,debugger,security,docs,research,math,physics,chess,scraper,analyst,executor,devops}/  # 15 agent dirs
  bridges/tseitin_tw/             # P vs NP bridge code
  communication/{bus.py, notifier.py}    # async message bus
  core/
    agent.py 368, agent_registry.py 147, agent_spawner.py 273,
    autonomy.py 548, cognitive.py 705, curiosity.py 739,
    learning_hooks.py 168, memory_tree.py 184, node_memory.py 252,
    orchestrator.py 522, research_loop.py 902, scheduler.py 236,
    self_eval.py 434, subagent.py 165, auto_updater.py 292
  entity/
    cognition/  values, empathy, growth, arbitro, thought_generator
    conversation/ chat, context, intent, command_router
    learning/ reflexion.py, skill_extractor.py   # NEW since roadmap
    living/ autonomous.py 1482, self_improve.py 863, web_explorer.py 310, ...
    memory/ store, episodic, semantic, autobiographical, consolidation, dreamscape, skills.py
    perception/  (audio, presence, vision stubs)
    proactivity/ (telegram, importance)
    api/ (REST + WebSocket: routes, monitoring, backup, voice, vision)
  evaluation/weekly_eval.py       # rolling regressions
  memory/ (knowledge_graph, unified, scoring.py, embeddings, extractor, consolidation)
  ml/
    feedback_store.py 669, learning_loop.py 411, lora_trainer.py 408,
    distill_pipeline.py 220, distill_builder.py 125, finetune_builder.py 338,
    hard_sampler.py 160, prompt_optimizer.py 251, error_correction.py 262,
    model_promoter.py 200, ab_evaluator.py 247, router.py 421, training.py 408
  models/                         # ollama client + model router
  monetization/
    content_factory.py, continuous_run.py, sec_revenue.py,
    ab_testing.py, mab.py, linucb.py, kpi_sync.py, analytics.py,
    platform_kpi.py, retention_analytics.py, boringness.py,
    ebook_pipeline.py, blog_affiliate.py, print_on_demand.py,
    stock_media.py, video_gen.py, video_composer.py, thumbnail_gen.py,
    script_generator.py, voice_synth.py, kling_client.py,
    image_fetcher.py, video_fetcher.py, cleanup_videos.py,
    comment_replies.py, community_posts.py, cross_post.py,
    cost_tracker.py, character_state.py
  monitor/cli/                    # CLI monitor
  observability.py                # in-process spans + Prom metrics + watchdog
  orchestration/router.py + providers/
    ollama, groq, mistral, cerebras, google, openrouter, sambanova,
    together, fireworks, deepinfra, claude_max     # 11 providers
  research/  pvsnp_* 26 files (explorer, benchmark, lean_gate, lean_proof,
    skeptic, citations, weekly_replay, taxonomy, problem_focus, linkage_graph,
    arxiv_mirror, audit, monitor, reviewer_pack, sec_bridge, reflection, replay)
    conjecture_graph.py, bootstrap_conjecture001/003b.py, cnf_encoders.py
  security/                       # vestigial, only __init__.py
  storage/                        # sqlite layer + migrations
  tools/                          # shell, fs, package_manager, web
  web/app.py 1049                 # FastAPI dashboard + WS
  worker.py                       # background runner
```

## ReAct loop — `src/entity/living/self_improve.py` (863 LOC)
**Already implemented and active.** Comment in source:
> "Proactive ReAct loop (react_tick): OBSERVE: git log, recent diary, pvsnp INCONCLUSIVE/BARRIER_HIT, log tails. THINK: LLM proposes ONE conservative change. ACT: enforce NEVER_TOUCH + WHITELIST + risk gating; edit_file via code_access. VERIFY: run_syntax_check (.py); rollback on failure. LOG: append to data/entity/self_improve_log.jsonl"

Has `NEVER_TOUCH` paths, `WHITELIST_PREFIXES`, risk gating (low/medium/high), env `SEC_SELF_IMPROVE_AUTO_APPLY`. So `self_fix` capability is NOT "deferred" anymore — at minimum the ReAct skeleton runs.

## Capabilities already real
- File R/W/edit: `src/tools/filesystem.py` + `entity/living/code_access.py`.
- Web search: `src/tools/` web client + `src/research/pvsnp_arxiv_mirror.py`.
- Nmap: `src/entity/living/network_discovery.py` (317 LOC).
- Shell exec: `src/tools/shell` (multi-agent uses it).
- Self-fix / self-improve ReAct loop: `src/entity/living/self_improve.py` ACTIVE.
- Agent spawner: `src/core/agent_spawner.py` (273 LOC) — exists.

## Learning / memory (key gems)
- **Weighted retrieval already DONE**: `src/memory/scoring.py` implements `α·recency + β·importance + γ·relevance` exactly as Park 2023. `MemoryScorer` class, default `α=0.3 β=0.3 γ=0.4`, `τ=168h`. ⚠️ Roadmap 2 Phase 0 marked TODO is in fact already shipped.
- **Voyager-lite skills library already DONE**: `src/entity/memory/skills.py` — table `skills(id, name, description, prompt_template, tags, embedding, usage_count, success_count, ...)`. Dedup via cosine > threshold. Source comment cites "Wang et al. 2023 Voyager — we adopt the skills-library idea but skip the code-execution component".
- **Skill extractor**: `src/entity/learning/skill_extractor.py`. Hooked in `src/core/learning_hooks.py` (`on_task_complete`, `SUCCESS_QUALITY=0.7`, `FAILURE_QUALITY=0.5`).
- **Reflexion (Shinn 2023) already DONE**: `src/entity/learning/reflexion.py` — `ReflexionEngine`, `build_retry_prompt`, `maybe_retry_with_reflection` with sqlite persistence.
- **LoRA + distillation**: `src/ml/lora_trainer.py` 408 LOC, `distill_pipeline.py` 220 LOC, `teacher_solver.py` 143 LOC, `finetune_builder.py` 338 LOC. Per roadmap: `run_count=0` (pipeline scritta, mai girata).
- **Feedback store**: `src/ml/feedback_store.py` (669 LOC). Per roadmap: "raccoglie dati che nessuno consuma".
- **Weekly evaluation**: `src/evaluation/weekly_eval.py` — rolling KPIs + regressing detection.
- **Observability**: `src/observability.py` — in-process spans, Prom metrics endpoint, watchdog (no OTel dep).

## Multi-provider routing
`src/orchestration/router.py` with 11 providers (ollama_local, ollama_remote, groq, mistral, cerebras, google, openrouter, sambanova, together, fireworks, deepinfra, claude_max). Strategies: quality_first, speed_first, local_first, round_robin. Tasks: coding/reasoning/review/docs/security/general.

## Conjecture graph
`src/research/conjecture_graph.py` + `seed_conjectures.py` + `bootstrap_conjecture001.py` + `bootstrap_conjecture003b.py`. Roadmap 1 Phase 1 (graph) appears built.
Lean gate: `src/research/pvsnp_lean_gate.py`, `pvsnp_lean_proof.py`, `pvsnp_lean_counterexample.py`. SAT encoders: `cnf_encoders.py`.

## Monetization pipelines (5 declared, all wired)
`src/monetization/sec_revenue.py` orchestrates: stock_media, ebook, pod_designs, blog_articles + the video pipeline as separate daemon. Schedule in code (hours between runs). State at `data/content_factory/revenue_state.json`.
KPI sync (`kpi_sync.py`), MAB (`mab.py`), LinUCB (`linucb.py`), A/B (`ab_testing.py`), retention (`retention_analytics.py`) — all present. KPI ingestion (Roadmap 3 P1) appears built.

## Cron / how it runs
- watchdog every 5 min — `lab_c001/scripts/watchdog.sh`
- daily report 18:00, c003b counterexample 09:00, literature scan 08:00, git sync 23:00, security monitor every 5 min.
- monetization daily_run.sh DISABLED 2026-04-23 ("focus on P vs NP"). Only video cleanup at 03:00 daily.
- SD-WebUI @reboot.
- Roadmap mentions cron 6h `youtube_kpi_sync`; not visible in current crontab.

## Tests
Dir tree exists (core/e2e/entity/integration/memory/ml/monetization/research/unit) — coverage details not inspected.

## Surprises vs project notes
- "SEC capabilities reali" memory says `agent_spawn` + `self_fix` deferred. **In fact `self_improve.py` is a 863-line working ReAct loop**, and `agent_spawner.py` exists (273 LOC) — at minimum scaffold present.
- Roadmap 2 Sprint 0 (weighted retrieval) marked "current state: cosine-only" but `src/memory/scoring.py` already implements the Park formula. Probably shipped after the roadmap was written.
- Skills library + Reflexion both implemented. Roadmap 2 Phase 1 done at code level (usage data unknown).
- Memory note says C-003b cumulative entropy; SEC has `bootstrap_conjecture003b.py` matching it. Bridge active.
