# ENTITY — Inventory (2026-05-13)

Target: `~/Scrivania/SEC/src/entity/` su `ludo@sec`. ENTITY è il runtime "vivente" che dà a SEC accesso al server (file R/W/edit, shell, nmap, web search) + memoria long-term + cognizione + autonomia diurna.

## Layout sorgenti (60 .py)

```
src/entity/
├── core.py                 (DigitalEntity singleton; 17.8 KB)
├── identity.py
├── pvsnp_capabilities.py   (REAL nmap, file R/W/edit, web_search; 15.9 KB)
├── conversation/           (chat, intent, command_router 12 KB, context_builder, message)
├── memory/                 (store 32 KB + 9 layer modules)
├── cognition/              (values, empathy, question_engine, growth, arbiter, verification, thought_generator)
├── living/                 (autonomous 67 KB, self_improve 33 KB, self_fix 8 KB,
│                            code_access 17.7 KB, tool_executor 16 KB,
│                            confirmation 11 KB, network_discovery, home_automation 27.7 KB,
│                            web_explorer 11.8 KB, scenes, automation_learner,
│                            solar_schedule 7.4 KB, inner_life, dreamscape via memory)
├── learning/               (reflexion, skill_extractor)
├── perception/             (presence, vision, stt)
├── proactivity/            (proactivity engine, triggers: PaperMatch, CVEAlert, Milestone, WelcomeBack)
└── api/                    (routes, websocket, voice, vision, monitoring, backup 10.8 KB)
```

## Tool/capability surface (cosa ENTITY può fare sul server)

Punti di ingresso principali:
1. **`tool_executor.py`** — ReAct loop classico (THOUGHT/ACTION/OBSERVATION/ANSWER). Modello default `qwen2.5-coder:3b`. Max 8 step. 12 azioni: `shell`, `read_file`, `system_status`, `cpu_temp`, `disk_info`, `memory_info`, `battery`, `gpu_info`, `process_list`, `network`, `ollama_status`, `sensors`. **Read-only** (system prompt esplicito). Ogni `shell` passa per il `confirmation_gate`.
2. **`code_access.py`** — operazioni filesystem complete su `SAL_ROOT=/home/ludo/Scrivania/SEC`:
   - read_file, list_files, search_code, file_tree
   - **write_file, edit_file** (con backup automatico in `data/entity/backups/`)
   - git_status, git_diff, git_commit, git_log
   - run_tests (pytest -x), run_syntax_check (ast.parse)
   - rollback() per ripristinare backup
   - Read-only extra: `AUTHORIZED_READ_PATHS` = {kissat, sd-webui, tools, projects}
   - `PROTECTED_PATHS` = {.env, .git, config/providers.yaml, data/entity/entity.db}
   - `PROTECTED_GLOBS` = {*.key, *.pem, *.secret, .env*}
   - Ogni edit logga via `autobiographical.reflect_on_activity()` nel diario.
3. **`pvsnp_capabilities.py`** — sostituiscono stub fake con implementazioni reali:
   - `network_scan_real`: subprocess `nmap` TCP-connect (no sudo), auto-detect LAN
   - `read_file_real` / `write_file_real` / `edit_file_real` → delegano a code_access + bump counter
   - `web_search_real`: (a) arxiv mirror locale (b) DuckDuckGo HTML scrape
4. **`command_router.py`** (1265 LOC) — dispatch testuale degli intent verso le capability. Conta su `pvsnp_capabilities` per tutte le azioni reali.
5. **`api/routes.py`** + **`websocket.py`** — REST + WS per dashboard + chat + confirmation.
6. **`self_improve.py`** (33 KB) — ReAct OBSERVE-THINK-ACT-VERIFY-LOG. Whitelist `src/research/pvsnp_*`, `src/entity/pvsnp_capabilities.py`, `research/`, `tests/`. NEVER_TOUCH `intent.py`, `pvsnp_explorer.py`, `entity.db`, `.env`, `config/`, `data/`. Auto-apply low-risk solo se `SEC_SELF_IMPROVE_AUTO_APPLY=1` (default 0). VERIFY = `run_syntax_check`, rollback automatico se fallisce.
7. **`self_fix.py`** — chiusura del loop error→analysis→patch→test. **Solo PROPOSE** (no auto-apply): legge top error pattern, LLM debugger genera ticket persistito in `data/sec_learning.db` (`self_fix_tickets`) + JSONL `data/self_fix/analyses.jsonl`. Auto-apply gated da `SEC_SELF_FIX_AUTO_APPLY=1` (non implementato).

## Sandboxing — stato attuale

**Shell sandbox (`src/tools/shell.py`)**: FORTE.
- `ALLOWED_COMMANDS` set di ~80 binari (git, python, pip, docker, curl, find, grep…). Tutto fuori dalla lista è bloccato.
- `BLOCKED_PATTERNS` per fork-bomb, `rm -rf /`, `curl | sh`, `shutdown`, `systemctl start/stop/restart/enable/disable`, `journalctl --vacuum`.
- Tokenizer shell-aware via `shlex` con segment splitting (`;`, `|`, `&&`, `||`).

**Path sandbox (`code_access._resolve`)**: FORTE.
- Tutte le path risolte sotto `SAL_ROOT` con `.resolve().relative_to()` (anti-traversal).
- Read esterno solo via `_resolve_read` con whitelist `AUTHORIZED_READ_PATHS`.

**Confirmation gate (`confirmation.py`)**: PRESENTE ma fragile.
- Risk levels: LOW/MEDIUM/HIGH/CRITICAL mappati ad action_type (shell_command=CRITICAL, write_file/edit_file=HIGH, git_commit=MEDIUM).
- Timeout default 5 min → **DENY** (sicuro).
- 3 canali: WebSocket / REST / CLI / Notifier Telegram.
- Auto-approve list configurabile per action_type (NON per pattern di comando: un'unica voce "shell_command" approva qualunque shell).

## Audit log — stato attuale

**ASSENTE come tabella dedicata.** Quello che esiste:
- Schema entity.db ha: identity, episodes, diary, long_term, semantic, dreams, milestones, lessons, episode_embeddings + FTS5. **Nessuna tabella tipo `action_log`/`audit_log`/`tool_calls`**.
- `code_access._log_edit` → scrive nel **diario** (testo narrativo, non strutturato, non queryable per analisi forensica).
- `self_improve` → JSONL `data/entity/self_improve_log.jsonl` (solo self-improve).
- `self_fix` → tabella `self_fix_tickets` nel DB separato `data/sec_learning.db` + JSONL.
- `confirmation_gate._history` → SOLO IN MEMORIA, perso al restart (max 200 entries trim a 100).
- `tool_executor._action_log` → SOLO IN MEMORIA per la singola call.

→ **Gap critico**: nessuna persistenza centrale di "chi ha fatto cosa, quando, con quale risultato" per shell/file_ops/network_scan. Forensics impossibile.

## Memoria long-term

Sofisticata. 9 layer:
- `episodes` (FTS5) + `episode_embeddings` (vettori)
- `diary` (FTS5) autobiografico
- `long_term` (consolidato, importance score, access_count, emotion_tag, category, FTS5)
- `semantic` (concept→statement, confidence)
- `dreams` (subconscious symbolic)
- `lessons` (learned behaviors, strength, applied_count)
- `milestones`
- Skills + bridge (skills.py + bridge.py)
- Consolidation engine (`consolidation.py`, 11.7 KB) per movimento episodes→long_term

## Escalation / dry_run

- `dry_run` solo in `confirmation.py` (commenti) e `self_improve.py` (proposed vs applied).
- Nessun "human escalation" automatico tipo "if risk>=HIGH and N retries: page Ludo via Telegram" — Telegram esiste (notifier) ma è invocato solo dal gate.

## Solar schedule (autonomia diurna)

`solar_schedule.py`: cron tick via `--check`. Calcola sunrise/sunset Milano (astral lib). Se day → garantisce autonomia ON via API `/api/entity/chat` POST. Se night → OFF. Stato in `data/entity/solar_state.json`. Razionale: rumination notturna spreca token, consolidare via dream/consolidate solo on trigger.

## Backup

`api/backup.py`: copia `entity.db` (+ WAL/SHM) in `data/entity/backups/entity_YYYYMMDD_HHMMSS.db`, mantiene ultimi 30. Inoltre `export_personality()` → snapshot JSON di identity+values+traits+milestones per "clone".

## Proattività

`proactivity/proactivity.py` + `triggers.py`: tick ogni 5 min nel living loop. Triggers: PaperMatch (arxiv vs interessi), CVEAlert (`pip-audit --format=json` su deps Python), Milestone (raggiunti goal), WelcomeBack (presenza dopo assenza). Output → LogChannel + Telegram.

## Self-restart

`core.request_restart()` scrive marker JSON e SIGTERM se stesso; systemd `Restart=always` ricrea. Cooldown 60s. Solido.

## Mancano (vs SOTA agent runtime tipici)

- **Audit log strutturato** (tabella dedicata).
- **Tool registry decoupled** (oggi le 12 azioni sono hardcoded in `_execute_action` if/elif).
- **Agent-Computer Interface (ACI)** strutturata stile swe-agent (linter feedback, file viewer con line numbers, syntax-aware edit).
- **Sub-agent spawn** (deferred secondo memoria utente).
- **Capability gating granulare per pattern** (oggi è on/off per action_type).
- **Repo-map** (aider): mappa simbolica del codebase per LLM context.
- **Cost/budget tracker** per LLM tokens.
- **Differential testing** stile Devin (run tests both before/after edit).
