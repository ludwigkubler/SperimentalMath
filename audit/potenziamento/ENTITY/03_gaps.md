# ENTITY — Gap analysis

Score = Impact × (6 - Effort). Range 1-25. Più alto = più conveniente.

| # | Capability | In ENTITY? | In SOTA | Sistema esempio | Impact | Effort | Score | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | Audit log strutturato (tabella `action_log`) | NO | YES | tutti i sistemi enterprise | 5 | 1 | 25 | Diary narrativo non basta. Una tabella `tool_calls(ts, tool, args_json, caller, risk, approved_by, outcome, duration_ms)` è 30 LOC + 1 tabella. Forensics + analytics + RL signal. |
| 2 | Agent-Computer Interface (file viewer paginato + edit con feedback) | NO (read_file legge tutto) | YES | SWE-agent | 5 | 3 | 15 | Riduce hallucination su file lunghi (oggi `read_file` 3000 char truncate cieco). Aggiungere `open(path, line=N, window=100)`, `goto`, `scroll`. |
| 3 | Repo-map (skeleton classi/funzioni pesato) | NO (solo grep) | YES | Aider | 5 | 3 | 15 | Per 4400 .py file SEC, fondamentale. tree-sitter + PageRank. Cache in DB. |
| 4 | Capability gating per pattern (non per tipo) | NO (auto_approve è per action_type) | parziale | Devin .rules | 4 | 2 | 16 | Oggi auto-approve `shell_command` approva QUALSIASI shell. Pattern-level: auto-approve `git status`, `git diff`, ma chiedi per `git push`. |
| 5 | Docker-wrap per shell HIGH/CRITICAL | NO | YES | Open-Interpreter | 5 | 3 | 15 | Container disposable per comandi rischiosi. Mitiga il bypass via `python -c "..."` (python è in ALLOWED_COMMANDS). |
| 6 | Tool registry decoupled (`@tool` decorator) | NO (if/elif hardcoded) | YES | smolagents, swe-agent | 3 | 2 | 12 | 12 azioni in if/elif → registry con metadata (name, args_schema, risk, side_effects). Riusabile, testabile, documentabile. |
| 7 | Code-as-actions (LLM scrive Python) | NO (ACTION: text) | YES | smolagents | 4 | 4 | 8 | Refactor sostanziale di `tool_executor`. Lo lascerei in P2. |
| 8 | Cost/budget tracker per LLM token | NO | parziale | Devin ACU | 3 | 2 | 12 | Counter su routing_engine. SEC usa Ollama locale (low cost) MA self_improve può spendere molto. Tracciabile in `data/entity/llm_usage.jsonl`. |
| 9 | Differential testing (run tests pre+post edit) | parziale (post solo via syntax_check) | YES | SWE-agent, Devin | 4 | 2 | 16 | `self_improve.react_tick` fa syntax_check ma non pytest. Pre+post pytest sui test di unità touched detecta breakage reale. |
| 10 | Sub-agent spawn (deferred secondo memory utente) | NO | YES | Devin (parallel instances), Claude Sub-agents | 4 | 4 | 8 | Memory utente segnala deferred. Proposta: tabella `sub_tasks(parent_id, goal, status, ...)` + scheduler che lancia un ToolExecutor isolato con propria conversation. |
| 11 | WASM sandbox per Python eval | NO | YES (sperimentale) | smolagents Pyodide | 3 | 5 | 3 | Bel sogno. Effort 5/5. Skip. |
| 12 | `.rules` file editabili dall'utente per policy | NO (NEVER_TOUCH hardcoded) | YES | Devin, Cursor | 4 | 1 | 20 | `~/Scrivania/SEC/.entityrules` letto al boot, popola NEVER_TOUCH e ALLOWED_COMMANDS. Ludo può cambiare policy senza editare codice. |
| 13 | Persistent confirmation_gate history | NO (in-memory) | YES | tutti enterprise | 3 | 1 | 15 | `gate._history` perso al restart. Tabella `confirmations` in entity.db. |
| 14 | Tool result caching (LRU) | NO | parziale | tutti | 3 | 2 | 12 | `system_status`, `gpu_info`, `network` ripetuti hanno output near-stable. Cache 30s riduce 30-50% chiamate. |
| 15 | Streaming output per shell long-running | NO | YES | Devin, swe-agent | 3 | 3 | 9 | Oggi `shell.run` aspetta intero output. Per build/test lunghi, stream incrementale a console + LLM context. |
| 16 | Per-tool rate limiting | NO | parziale | enterprise | 3 | 1 | 15 | Eviterebbe loop ReAct che chiama `system_status` 8 volte di fila. Token bucket per tool. |

## Top 6 (per score)

1. **Audit log strutturato** (25) — quick win critico, 2h lavoro.
2. **.entityrules file utente** (20) — empowerment Ludo, 4h.
3. **Capability gating per pattern** (16) — chiude un buco reale, 4h.
4. **Differential testing pre+post** (16) — self_improve safety++, 3h.
5. **ACI (viewer paginato + edit window)** (15) — qualità edit, 8h.
6. **Repo-map** (15) — qualità context LLM, 8h.
