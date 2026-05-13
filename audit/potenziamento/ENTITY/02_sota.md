# ENTITY — SOTA comparison

5 sistemi confrontati. Per ognuno: cosa fa, capability chiave, URL, lezione per ENTITY.

## 1) SWE-agent (Princeton, NeurIPS 2024) — ACI

- **Repo**: https://github.com/SWE-agent/SWE-agent
- **Paper**: https://arxiv.org/abs/2405.15793 (NeurIPS 2024)
- **Docs**: https://swe-agent.com/
- **Cosa fa**: prende un GitHub issue + repo, autonomamente lo risolve. SOTA su SWE-bench (12.5% pass@1) e HumanEvalFix (87.7%).
- **Capability chiave — Agent-Computer Interface (ACI)**: l'LLM è trattato come un nuovo tipo di end-user che ha bisogno di interfacce ad-hoc. NON espone bash crudo. Espone:
  - `open`, `goto`, `scroll_down/up` con line-window di 100 righe (viewer paginato)
  - `edit start_line:end_line` con feedback immediato (linter, syntax check post-edit, auto-rollback se rompe)
  - `find_file`, `search_file`, `search_dir` con risultati compatti
  - `submit` finale
- **Lezione per ENTITY**: il dispatch `_execute_action` di `tool_executor.py` è "low-level" (shell crudo, read_file intero). Manca un viewer con line numbers, un editor che valida sintatticamente in-loop, e feedback "ti ho mostrato 100 righe, ne mancano 200" che mantiene l'LLM ancorato. Aggiungere ACI alza il tasso di successo dei micro-task.

## 2) Aider (Paul Gauthier) — repo-map

- **Repo**: https://github.com/Aider-AI/aider
- **Docs repo-map**: https://aider.chat/docs/repomap.html
- **Cosa fa**: AI pair programmer terminale. Edita file, commit git automatici. Considerato il più "pragmatico" del settore.
- **Capability chiave — repo-map**:
  - Estrae da TUTTO il repo classi, funzioni, signature, types (via tree-sitter).
  - Costruisce un grafo file→file (dipendenze) e applica PageRank/graph-ranking per importanza.
  - Seleziona top-k simboli rilevanti che entrano nel context budget dell'LLM.
  - Senza repo-map, l'LLM "non sa che il metodo `foo()` esiste in `bar.py`". Con repo-map, riceve un riassunto strutturato del codebase.
- **Lezione per ENTITY**: `code_access.search_code` fa grep, ma niente di simile a repo-map. SEC è ~4400 file Python — il LLM brancola. Una mappa scheletro (classi/funzioni/signature) pesata per PageRank cambierebbe drasticamente la qualità di `self_improve` e degli edit. Implementabile in <500 LOC con `tree-sitter-python` + `networkx`.

## 3) Open-Interpreter (Killian Lucas) — sandbox via container

- **Repo**: https://github.com/OpenInterpreter/open-interpreter
- **Docs safety**: https://docs.openinterpreter.com/safety/introduction
- **Cosa fa**: natural language → shell+python locale, "ChatGPT Code Interpreter" ma sulla TUA macchina.
- **Capability chiave — sandbox layered**:
  - User confirmation prima di ogni execute (analoga a `confirmation_gate` ENTITY).
  - **Docker mode**: tutto il code execution in container isolato. Quando l'esecuzione fallisce o è dubbia, il danno è contenuto.
  - **E2B mode**: sandbox cloud per Python (limite: solo Python, non shell/JS).
  - LLM alignment come prima linea (GPT-4 rifiuta `rm -rf /`).
- **Lezione per ENTITY**: oggi shell gira nello stesso namespace del processo SEC. Anche con `BLOCKED_PATTERNS` e `ALLOWED_COMMANDS`, un comando "creativo" può bypassare (es. `python -c "import os; os.system(...)"`: python è in allowlist!). Aggiungere modalità **Docker-wrap** per `shell_command` quando risk >= HIGH renderebbe l'attacco a SEC un attacco al container.

## 4) Devin / Devin 2.0 (Cognition Labs) — VM snapshotting

- **Blog**: https://cognition.ai/blog/introducing-devin
- **Devin 2.0**: https://cognition.ai/blog/devin-2
- **Agents 101**: https://devin.ai/agents101
- **Cosa fa**: closed-source. Software engineer autonomo cloud-based. SOTA originale su SWE-bench (13.86% end-to-end vs 1.96% precedente).
- **Capability chiave — hypervisor-level snapshotting**:
  - Ogni Devin run gira in VM isolata (ambiente dev: shell + editor + browser).
  - L'agent può aprire PR, attendere CI, rispondere a review, re-test → richiede stato persistente tra step (ore/giorni).
  - Soluzione: snapshot dell'intera macchina (memoria + process tree + filesystem). Quando idle, compute spento. Quando arriva un evento (CI done, review reply), si riaccende dallo snapshot esatto.
  - Knowledge management con `.rules`/`.md` permanenti.
- **Lezione per ENTITY**: ENTITY ha già self-restart via systemd (core.py), ma il ricordo è "stato cognitivo + DB". Manca uno snapshot dello "stato di task" (file work-in-progress, comandi parziali, hypothesis stack). Inoltre il knowledge management permanente esiste come `long_term`/`semantic` ma non come `.rules` file editabili dall'utente per imporre policy ("non toccare mai questo file") — oggi è hardcoded in `NEVER_TOUCH`.

## 5) HuggingFace smolagents CodeAgent

- **Repo**: https://github.com/huggingface/smolagents
- **Docs**: https://huggingface.co/docs/smolagents/en/index
- **Blog**: https://huggingface.co/blog/smolagents
- **Cosa fa**: agent framework barebones. La differenza chiave: il LLM scrive le sue azioni come **codice Python**, non come JSON o testo strutturato.
- **Capability chiave — code-as-actions + authorized_imports**:
  - Invece di `ACTION: shell ls` (ENTITY-style), il LLM scrive `result = shell("ls"); analyze(result)`. Più espressivo, meno step, riusa funzioni.
  - **Sandbox tier**: Blaxel, E2B, Modal, Docker, **Pyodide+Deno WebAssembly** (interessantissimo: WASM = isolamento puro a livello istruzione, niente container overhead).
  - **`authorized_imports`**: lista bianca di moduli Python importabili. Anche se LLM tenta `import os`, fallisce se non in lista.
- **Lezione per ENTITY**: il modello "ACTION: x args" di `tool_executor` è limitante. Step multipli costosi. Migrare a code-as-actions (con sandbox `authorized_imports`) ridurrebbe gli step ReAct. Pyodide WASM è il "santo graal" del sandbox: zero kernel attack surface.

## Bonus — Toolformer (Meta, 2023)

- **Paper**: https://arxiv.org/abs/2302.04761
- **Cosa fa**: auto-supervised tool learning. Il LLM stesso decide quando inserire una chiamata-tool nel suo output, addestrato su dataset generato da sé.
- **Lezione per ENTITY**: oltre lo scope di un audit ergonomico. Però l'idea che il LLM "scopra" il tool giusto da una libreria ricca è interessante per il dispatcher di `command_router.py` (oggi rule-based, 1265 LOC di if/elif).

## Tabella riassuntiva ranking

| Sistema | Punto forte per ENTITY | Difficoltà adozione |
|---|---|---|
| SWE-agent | ACI (viewer, edit window, linter loop) | Media |
| Aider | repo-map con PageRank | Media |
| Open-Interpreter | Docker sandbox per shell rischiosa | Bassa (container già usabili) |
| Devin | VM snapshot + .rules file utente | Alta (richiede infra) |
| smolagents | code-as-actions + WASM sandbox | Media-alta (refactor tool_executor) |
