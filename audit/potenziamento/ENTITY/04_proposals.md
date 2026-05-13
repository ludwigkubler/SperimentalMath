# ENTITY — Proposte concrete (10)

Ordine = score gap × adozione realistica. Tutte cite URL concreto.

---

## P1 — Audit log strutturato (`tool_calls` table)

**Descrizione**: aggiungere tabella SQLite `tool_calls` in `entity.db` con riga per ogni invocazione tool (shell, read_file, write_file, edit_file, network_scan, web_search, git_*). Schema: `id, ts, tool_name, args_json, caller (entity|user|self_improve|tool_executor), risk_level, approved_by, outcome (ok|error|denied|timeout), duration_ms, output_size, error_msg`.

**Motivazione**: oggi gli unici log strutturati sono `self_improve_log.jsonl` e `self_fix_tickets`. Tutto il resto è "diary narrativo" tramite `code_access._log_edit`. Impossibile rispondere a "quanti shell command nelle ultime 24h?", "quale tool fallisce di più?", "chi ha modificato file X?".
URL ispirazione: https://leehanchung.github.io/blogs/2026/04/24/hidden-technical-debt-agent-runtime/ (agent runtime audit pattern).

**File da modificare**:
- `~/Scrivania/SEC/src/entity/memory/store.py` — aggiungere `tool_calls` allo SCHEMA + helper `log_tool_call()`.
- `~/Scrivania/SEC/src/entity/living/tool_executor.py` — chiamare `log_tool_call` in `_execute_action`.
- `~/Scrivania/SEC/src/entity/living/code_access.py` — sostituire `_log_edit` con doppia scrittura (diary + tool_calls).
- `~/Scrivania/SEC/src/entity/pvsnp_capabilities.py` — wrap delle capability reali.

**Primo test**: dopo 1 ora di runtime, `SELECT tool_name, COUNT(*), AVG(duration_ms) FROM tool_calls GROUP BY tool_name;` ritorna >0 righe e l'invariante "ogni edit_file ha riga corrispondente" passa.

**Ore-uomo**: **2-3h**.

---

## P2 — `.entityrules` policy file editabile da Ludo

**Descrizione**: al boot, `core.py` legge `~/Scrivania/SEC/.entityrules` (YAML o TOML). Estende NEVER_TOUCH / ALLOWED_COMMANDS / auto_approve list senza modificare codice. Esempio:
```yaml
never_touch:
  - data/sperimentalmath/lean_verified/
  - "research/published/*"
allow_shell_patterns:
  - "^git status"
  - "^git diff"
  - "^pytest tests/.*"
shell_blocked_patterns:
  - "ollama rm "
```

**Motivazione**: oggi le regole sono hardcoded in `self_improve.NEVER_TOUCH` e `shell.ALLOWED_COMMANDS`. Cambiare richiede edit del codice + restart. Devin/Cursor usano `.cursorrules`/`.windsurfrules` da anni come standard de facto. URL: https://cognition.ai/blog/devin-2 ("dedicated knowledge management system, with many products offering .rules files").

**File da modificare**:
- `~/Scrivania/SEC/src/entity/core.py` — `_load_rules()` invocato in `init()`.
- `~/Scrivania/SEC/src/entity/living/self_improve.py` — `NEVER_TOUCH` e `WHITELIST_PREFIXES` letti dal rules-store.
- `~/Scrivania/SEC/src/tools/shell.py` — `ALLOWED_COMMANDS`/`BLOCKED_PATTERNS` estesi a runtime.
- Nuovo: `~/Scrivania/SEC/src/entity/policy.py` (50-100 LOC).
- Esempio: `~/Scrivania/SEC/.entityrules.example`.

**Primo test**: scrivere `.entityrules` con `never_touch: ["src/research/foo.py"]`, chiamare `self_improve.react_tick` → verifica che il file non venga toccato anche se non in NEVER_TOUCH hardcoded.

**Ore-uomo**: **3-4h**.

---

## P3 — Capability gating per pattern (non solo per tipo)

**Descrizione**: estendere `confirmation_gate.py`. Auto-approve list oggi è `set[str]` di action_type. Diventa `list[PatternRule]` con: `action_type`, `arg_pattern` (regex), `risk_override` (opzionale), `max_uses_per_hour`. Esempio:
```yaml
auto_approve:
  - action: shell_command
    pattern: "^git (status|diff|log)$"
  - action: edit_file
    pattern: "^research/.*\\.md$"
    max_per_hour: 20
```

**Motivazione**: oggi `auto_approve.add("shell_command")` apre la porta a TUTTI gli shell — perde il senso del gate. URL: https://swe-agent.com/latest/background/ (ACI = "fine-grained, scoped controls per action").

**File da modificare**:
- `~/Scrivania/SEC/src/entity/living/confirmation.py` — `_auto_approve` da `set[str]` a `list[PatternRule]`. Aggiungere `_matches_rule()`.
- `~/Scrivania/SEC/src/entity/api/routes.py` — endpoint `POST /api/entity/policy/add_rule`.

**Primo test**: configurare rule `shell_command` regex `^df ` → `df -h` passa senza prompt; `df && rm x` viene gated.

**Ore-uomo**: **3-4h**.

---

## P4 — Differential testing nel self_improve loop (pre+post)

**Descrizione**: estendere `self_improve.react_tick` VERIFY step. Prima dell'edit, identifica i test che importano (transitively) il file editato → run baseline. Dopo l'edit, ri-run gli stessi test. Se passavano-→passavano = OK. Se passavano-→falliscono = rollback automatico + log come "regression detected".

**Motivazione**: oggi VERIFY è solo `run_syntax_check` (ast.parse). Codice sintatticamente valido che rompe semanticamente non viene catturato. URL: https://arxiv.org/abs/2405.15793 §3.4 ("agent verifies via test execution").

**File da modificare**:
- `~/Scrivania/SEC/src/entity/living/self_improve.py` — `_verify_edit()` arricchito con `_find_tests_for(file)` + diff results.
- `~/Scrivania/SEC/src/entity/living/code_access.py` — `run_tests` accetta lista path specifici (già implementato, basta usarlo).

**Primo test**: inserire bug semantico (es. `return False` invece di `return True` in funzione testata) in un file whitelist. `react_tick` deve rilevarlo e rollback.

**Ore-uomo**: **3-4h**.

---

## P5 — ACI: viewer paginato + edit window

**Descrizione**: aggiungere a `tool_executor` 3 nuove azioni stile swe-agent:
- `open <path> [line=N]` → mostra 100 righe centrate su N con indicatore "Showing lines N-M of TOTAL".
- `goto <line>` → muove la window.
- `scroll_down` / `scroll_up` → +50 righe.
- `edit_window <start>:<end> <new_text>` → sostituisce range esatto, post-edit ri-mostra +/-10 righe + warning se syntax check fallisce.

Stato del viewer (path + cursor) persistente per conversation_id.

**Motivazione**: oggi `read_file` legge fino a 3000 char (MAX_OBSERVATION_LENGTH) silenziosamente troncando. Su file >300 righe l'LLM allucina su cosa c'è "in fondo". URL: https://arxiv.org/abs/2405.15793 §3.2 ("file viewer with line numbers significantly improves edit success rate").

**File da modificare**:
- `~/Scrivania/SEC/src/entity/living/tool_executor.py` — nuove azioni + state per conversation.
- Nuovo: `~/Scrivania/SEC/src/entity/living/file_viewer.py` (200 LOC).

**Primo test**: su un file 500 LOC, `open src/entity/core.py line=250` ritorna righe 200-300 con header. `edit_window 250:255 "new content"` modifica solo quel range.

**Ore-uomo**: **6-8h**.

---

## P6 — Repo-map (aider-style) cached in DB

**Descrizione**: parser tree-sitter-python scansiona `SAL_ROOT/**/*.py`, estrae per ogni file `{classes: [{name, methods, line}], functions: [{name, signature, line}], imports: [str]}`. Salva in tabella `repo_map(file, mtime, symbols_json)`. Costruisce grafo (NetworkX) file→file via imports, calcola PageRank. Espone API `get_repo_skeleton(focus_files=[...], budget_tokens=2000)` che ritorna top-k simboli più rilevanti.

**Motivazione**: SEC ha ~4400 file Python. `self_improve` LLM riceve solo `git log` + tail di log + 1 file campione (whitelist round-robin). Niente "context-aware" map. URL: https://aider.chat/docs/repomap.html ("graph ranking ... most important parts of the codebase that will fit into the active token budget").

**File da modificare**:
- Nuovo: `~/Scrivania/SEC/src/entity/cognition/repo_map.py` (~400 LOC).
- `~/Scrivania/SEC/src/entity/memory/store.py` — schema `repo_map`.
- `~/Scrivania/SEC/src/entity/living/self_improve.py` — `_gather_observe()` usa repo_map invece di sample round-robin.
- Dipendenza: `tree-sitter`, `tree-sitter-python` (pip install, no system).

**Primo test**: `get_repo_skeleton(focus_files=["src/entity/living/self_improve.py"], budget_tokens=1000)` ritorna primaria `code_access`, `confirmation_gate`, `error_correction`. Tempo costruzione iniziale <30s, lookup <50ms.

**Ore-uomo**: **6-10h**.

---

## P7 — Docker-wrap per shell HIGH/CRITICAL

**Descrizione**: in `shell.ShellExecutor.run`, se risk >= HIGH e env `SEC_SHELL_SANDBOX=docker`, esegue il comando in container Docker disposable (`docker run --rm --network=none -v ${SAL_ROOT}:/work:ro python:3.12-slim bash -c "..."`). Stdout/stderr ritorna identico. Permessi write disabilitati di default; volumi RW solo se esplicitamente in argomento.

**Motivazione**: `ALLOWED_COMMANDS` include `python`, ma `python -c "import os; os.system('rm -rf ~')"` bypassa il check command-level. Docker isola namespace. URL: https://docs.openinterpreter.com/safety/introduction (Docker mode pattern).

**File da modificare**:
- `~/Scrivania/SEC/src/tools/shell.py` — `_run_in_docker()` branch.
- `~/Scrivania/SEC/src/entity/living/confirmation.py` — risk-based dispatch.

**Primo test**: `shell.run("rm -rf ~", risk='critical')` con `SEC_SHELL_SANDBOX=docker` → container parte, fallisce dentro (no permission), host home intatta.

**Ore-uomo**: **4-6h**.

---

## P8 — Tool registry decoupled con metadata

**Descrizione**: introdurre `~/Scrivania/SEC/src/entity/tools/registry.py` con decoratore `@tool(name, args_schema, risk, side_effects, rate_limit)`. Le 12 azioni di `tool_executor._execute_action` (if/elif) diventano 12 funzioni decorate. Auto-generato il system prompt per LLM ("Available tools: ...") dal registry.

**Motivazione**: oggi if/elif rigido, no introspection. Aggiungere un tool richiede edit di tool_executor + REACT_SYSTEM_PROMPT. URL: https://huggingface.co/docs/smolagents/en/index ("Tools are exposed as Python functions").

**File da modificare**:
- Nuovo: `~/Scrivania/SEC/src/entity/tools/registry.py` (~200 LOC).
- Refactor: `~/Scrivania/SEC/src/entity/living/tool_executor.py` da if/elif → `registry.dispatch(action_type, args)`.

**Primo test**: aggiungere un nuovo tool `@tool("get_load_avg", ...)` in registry; chiamare `ACTION: get_load_avg` da una sessione ReAct → eseguito senza modifiche a tool_executor.

**Ore-uomo**: **4-6h**.

---

## P9 — Persistent confirmation history + analytics

**Descrizione**: aggiungere tabella `confirmations(id, ts, action_type, description, details_json, risk_level, reason, status, resolved_at, resolved_by)` in `entity.db`. `ConfirmationGate.request_confirmation` la popola; `_history` in memoria diventa cache + persistenza. Endpoint `GET /api/entity/confirmations/stats?days=7` per dashboard.

**Motivazione**: oggi `_history` è in memoria, perso al restart, max 200 trim a 100. Impossibile tracciare "ho approvato 50 self_improve in marzo, di cui 3 hanno rotto qualcosa" → niente apprendimento RL. URL: https://swe-agent.com/latest/ (ACI promuove logging strutturato delle azioni umane come segnale).

**File da modificare**:
- `~/Scrivania/SEC/src/entity/living/confirmation.py` — `request_confirmation` chiama `_persist()`.
- `~/Scrivania/SEC/src/entity/memory/store.py` — schema + helper `list_confirmations()`.

**Primo test**: approvare 5 azioni via WS, riavviare ENTITY, `GET /api/entity/confirmations/stats` ritorna 5.

**Ore-uomo**: **2-3h**.

---

## P10 — Sub-agent spawn (deferred secondo memoria; proposta strutturata)

**Descrizione**: introduzione di un mini-orchestratore `sub_agent_manager.py`. Espone tool `spawn_subagent(goal, max_steps, sandbox_level)` che:
1. Persiste `sub_tasks(id, parent_id, goal, status, started_ts, ended_ts, result, cost_tokens)` in entity.db.
2. Lancia un `ToolExecutor` isolato con propria conversation history, propri tool_executor allowlist (subset di quelli del parent).
3. Result ritorna in async (callback o polling).
4. Default sandbox_level = "isolated" (no write a SEC, no shell, solo read+web).

**Motivazione**: la memoria utente segnala "agent_spawn deferred". Senza sub-agent, il main loop di ENTITY blocca su task lunghi (es. "analizza 100 paper"). Devin gestisce questo con instances parallele in VM. URL: https://cognition.ai/blog/devin-2 ("multiple parallel Devin instances, each running in an isolated virtual machine").

**File da modificare**:
- Nuovo: `~/Scrivania/SEC/src/entity/orchestration/sub_agent_manager.py` (~300 LOC).
- `~/Scrivania/SEC/src/entity/memory/store.py` — schema `sub_tasks`.
- `~/Scrivania/SEC/src/entity/living/tool_executor.py` — tool `spawn_subagent` (con gate).

**Primo test**: spawn sub-agent con goal "leggi src/entity/core.py e ritorna le 5 dipendenze import principali" → produce result, sub_tasks row con status=success, tokens contati.

**Ore-uomo**: **8-12h**.

---

## Totale stima

| Proposta | Ore | Cumulato |
|---|---|---|
| P1 audit log | 2-3 | 3 |
| P9 confirmation persist | 2-3 | 6 |
| P2 .entityrules | 3-4 | 10 |
| P3 capability gating | 3-4 | 14 |
| P4 differential testing | 3-4 | 18 |
| P7 docker shell | 4-6 | 24 |
| P8 tool registry | 4-6 | 30 |
| P5 ACI viewer | 6-8 | 38 |
| P6 repo-map | 6-10 | 48 |
| P10 sub-agent | 8-12 | 60 |

**Sprint consigliato (2 settimane, 30h)**: P1+P9+P2+P3+P4+P7+P8 = layer di sicurezza/audit completo prima di toccare ACI/repo-map (che sono "qualità del lavoro").
