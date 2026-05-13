# SEC — 10 proposte concrete, ranked by Score (Impact × 5 / Effort)

Date: 2026-05-13. All paths under `~/Scrivania/SEC/` on `ludo@sec`.

---

## P1 — Park-style reflection loop on memory stream
**Score 12.5 (impact 5, effort 2).**

**Descrizione.** SEC ha già `src/memory/scoring.py` (formula recency·importance·relevance, Park 2023) e `src/memory/consolidation.py`, ma manca la **reflection trigger**: quando la somma di `importance` delle ultime N memorie supera una soglia (default 150 in Park), il sistema chiede al LLM "quali 3 high-level questions emergono?", risponde via retrieval+LLM, e re-scrive le risposte come *nuove* memorie con importance auto-rated. È la metà mancante della Generative-Agents recipe e moltiplica il valore della scoring già implementata.

**Motivazione.** Park et al. 2023, *Generative Agents: Interactive Simulacra of Human Behavior*. https://arxiv.org/abs/2304.03442 — sezione "Reflection" §4.2.

**File/modulo.** Nuovo: `src/memory/reflection.py` (~120 LOC). Wire in: `src/memory/unified.py` (chiama `should_reflect()` dopo ogni `write`). Test: `tests/memory/test_reflection.py`.

**Primo test/azione.** Script che ingurgita 200 memorie sintetiche, conta reflection prodotte ≥ 3, verifica importance media reflection > importance media base.

**Ore-uomo.** 6h.

---

## P2 — Voyager executable skills (sandboxed Python snippets)
**Score 12.5 (impact 5, effort 2).**

**Descrizione.** Estendere `src/entity/memory/skills.py` da "prompt templates" a **skills eseguibili**: una skill può contenere un blob Python (whitelisted imports: math, statistics, re, json, hashlib; no fs/network/subprocess) eseguito in `RestrictedPython` o subprocess con ulimit. Quando il SkillExtractor osserva un task che produce codice puro deterministico (es. una funzione SAT-encoding), promuove a executable. Reuso compositivo: nuovi prompt possono `call_skill("encode_pigeonhole", n=8)` invece di ri-prompt.

**Motivazione.** Wang et al. 2023, *Voyager*. https://arxiv.org/abs/2305.16291 — il commento in `skills.py` esplicitamente dice "we skip the code-execution component". Re-introducirlo è il salto qualitativo.

**File/modulo.** `src/entity/memory/skills.py` (estendere schema con colonne `code_blob TEXT`, `signature_json TEXT`, `is_executable INTEGER`). Nuovo `src/entity/memory/skill_runner.py` (sandbox via `RestrictedPython` o `subprocess` con `prlimit`). Migrazione: `src/storage/migrations/NNN_executable_skills.sql`.

**Primo test/azione.** `tests/entity/memory/test_skill_runner.py` con 5 skill semplici (fattoriale, MD5, regex match, parse JSON, encoding CNF clausola). Verificare: timeout duro a 2s, no import non-whitelistati, output deterministico.

**Ore-uomo.** 8h.

---

## P3 — Aviary-style sec-gym harness
**Score 12.5 (impact 5, effort 2).**

**Descrizione.** Modulo `src/evaluation/gym.py` che espone `env.reset(task_id) -> obs; env.step(action) -> obs, reward, done, info` su 3 task suite: (a) `conjecture_lifecycle` — N congetture seed devono attraversare OPEN→BUILDABLE in M step, (b) `pvsnp_qa` — 30 domande P vs NP con risposta gold da `pvsnp_compendium.py`, (c) `skill_reuse` — task ripetuto deve usare skill esistente, non re-derivarla. Ogni PR può essere A/B-tested con `python -m src eval gym --suite all`. Risolve il "non-negoziabile measurability" del roadmap.

**Motivazione.** FutureHouse Aviary. https://github.com/Future-House/aviary, paper https://arxiv.org/abs/2412.21154.

**File/modulo.** Nuovo: `src/evaluation/gym.py` (~250 LOC) + `data/eval/suites/{conjecture_lifecycle,pvsnp_qa,skill_reuse}.yaml`. CLI: extend `src/cli.py` con `eval gym`.

**Primo test/azione.** Run suite `pvsnp_qa` con 5 domande, baseline gemma3:4b vs claude_max provider; produrre report JSON in `data/evaluations/gym_<ts>.json`.

**Ore-uomo.** 10h.

---

## P4 — Real OpenTelemetry exporter
**Score 10 (impact 4, effort 2).**

**Descrizione.** `src/observability.py` già emula la *forma* delle span OTel. Aggiungere `opentelemetry-sdk` + `opentelemetry-exporter-otlp-proto-http` come dep opzionale; ogni `tracer.span()` esistente acquisisce un real OTel span context. Export to Jaeger o Tempo locale via docker compose. Sblocca debugging multi-agent (trace-id cross `agents/coder` → `agents/reviewer` → `learning_hooks`).

**Motivazione.** AutoGen v0.4 redesign — "OpenTelemetry for industry-standard observability". https://www.microsoft.com/en-us/research/project/autogen/

**File/modulo.** `src/observability.py` (wrap esistente, ~80 LOC nuove). `pyproject.toml` (extra `[otel] = ["opentelemetry-sdk", "opentelemetry-exporter-otlp-proto-http"]`). `deploy/docker-compose.tempo.yml` opzionale.

**Primo test/azione.** `python -m src run "ping"` con `SEC_OTEL_ENDPOINT=http://localhost:4318` esporta ≥ 1 trace visible in Tempo UI.

**Ore-uomo.** 6h.

---

## P5 — Per-agent self-verification critics
**Score 10 (impact 4, effort 2).**

**Descrizione.** `src/core/learning_hooks.py` usa una soglia hardcoded 0.7. Voyager mostra che il verifier deve essere *task-shape aware*. Aggiungere `src/core/verifiers.py` con verifier dict per agent_type: `coder` → ruff+py_compile+tests pass, `math` → Lean build OK, `research` → arxiv citation valid + statement coherent, `monetization` → KPI delta positive vs baseline. Ogni verifier ritorna `(quality 0-1, structured_feedback)` usato dal Reflexion engine già presente.

**Motivazione.** Voyager iterative prompting + self-verification, Wang 2023. https://arxiv.org/abs/2305.16291 §3.3. Anche Shinn 2023 Reflexion, https://arxiv.org/abs/2303.11366.

**File/modulo.** Nuovo: `src/core/verifiers.py`. Wire: `src/core/learning_hooks.py` (`on_task_complete` accetta `agent_type` → dispatch verifier).

**Primo test/azione.** Per ogni agent_type, un task fixture; verifier ritorna quality reasonable e feedback non-vuoto. Gate: `pytest tests/core/test_verifiers.py`.

**Ore-uomo.** 8h.

---

## P6 — Agentic tree search over conjecture moves
**Score 8.3 (impact 5, effort 3).**

**Descrizione.** `src/research/conjecture_graph.py` modella state-machine lineare. Wrappare con MCTS-lite in `src/research/conjecture_tree.py`: ogni nodo = (conjecture_state, proposed_action ∈ {formalize, weaken, strengthen, refute, decompose, literature_search}). UCB1 selection; budget = N obligations totali. Espansione via LLM "what's the next promising move?". Rollout valuta progress score via verifier (Lean build state, SAT result). Sostituisce la heuristica critical-path attuale.

**Motivazione.** Sakana AI Scientist v2, *Workshop-Level Automated Scientific Discovery via Agentic Tree Search*. https://github.com/SakanaAI/AI-Scientist-v2, paper https://pub.sakana.ai/ai-scientist-v2/paper/paper.pdf.

**File/modulo.** Nuovo: `src/research/conjecture_tree.py` (~300 LOC). `src/core/autonomy.py` (sostituire `pursue_obligation` con `pursue_tree_node`). Migration SQLite per `mcts_visits, mcts_value` su `obligations`.

**Primo test/azione.** Su 5 congetture seed, MCTS budget=20 step, log produced tree to `data/research/mcts_<conj>.json`. Verificare diversità mosse (≥ 3 azioni diverse esplorate).

**Ore-uomo.** 16h.

---

## P7 — VLM critic on monetization & research plots
**Score 7.5 (impact 3, effort 2).**

**Descrizione.** SEC produce: (1) thumbnail PNG per YouTube, (2) plot retention/KPI nel dashboard, (3) plot scientifici sotto `lab_c001/`. Aggiungere `src/entity/perception/vision_critic.py` che chiama `qwen2-vl:7b` o `minicpm-v` (Ollama remote, RTX 3070 Ti) su ogni image generata con prompt "rate clarity 1-10, list issues". Output usato come reward extra in `ab_testing.py` per thumbnail e come gate in `pvsnp_report.py`.

**Motivazione.** Sakana AI Scientist v2 §4 "VLM feedback on figures". https://github.com/SakanaAI/AI-Scientist-v2.

**File/modulo.** Nuovo: `src/entity/perception/vision_critic.py` (~150 LOC). Wire: `src/monetization/ab_testing.py`, `src/research/pvsnp_report.py`.

**Primo test/azione.** 10 thumbnail esistenti → scores VLM. Verificare correlazione (Pearson) tra VLM clarity score e CTR storica > 0.2 — segnale minimo prima di abilitarlo in produzione.

**Ore-uomo.** 8h.

---

## P8 — Group-chat / debate orchestration pattern
**Score 7.5 (impact 3, effort 2).**

**Descrizione.** Aggiungere a `src/core/orchestrator.py` un pattern `DebatePanel` che orchestra triade per congetture critiche: `MathAgent` (proponente) + `PvsnpSkeptic` (attaccante, già esistente `src/research/pvsnp_skeptic.py`) + `LeanFormalizer` (giudice via build OK). Round-robin con max 5 turni, terminazione su consensus o budget esaurito. Pattern from AutoGen `SelectorGroupChat`.

**Motivazione.** AutoGen v0.4. https://github.com/microsoft/autogen — pattern documentato in tutorial v0.4 e Microsoft Agent Framework.

**File/modulo.** Nuovo: `src/core/debate_panel.py`. Wire: `src/core/orchestrator.py` dispatch quando `task.priority == critical`.

**Primo test/azione.** 1 congettura seed (C-003b) attraverso debate 3-turni. Verificare ≥ 1 contestazione skeptic e ≥ 1 controrisposta math.

**Ore-uomo.** 8h.

---

## P9 — Skill-frontier curriculum picker
**Score 6.7 (impact 4, effort 3).**

**Descrizione.** `src/core/autonomy.py` ha MAB-style behavior dispatch ma non guarda il *frontiere delle skill*. Aggiungere `src/core/curriculum.py` che ogni N tick legge `skills` table e propone:
- 30% "extend": task simile a skill con `usage_count < 3` ma `success_rate > 0.7` (consolidare)
- 40% "explore": task con embedding distante da tutte le skill esistenti (frontiera nuova)
- 30% "exploit": skill con `success_rate` top-quartile usate nel task pertinente

Pattern Voyager curriculum.

**Motivazione.** Voyager §3.1 "Automatic Curriculum". https://arxiv.org/abs/2305.16291.

**File/modulo.** Nuovo: `src/core/curriculum.py` (~180 LOC). Wire: `src/core/autonomy.py` (sostituire random behavior pick).

**Primo test/azione.** Simulare 100 tick offline; verificare che proporzione extend/explore/exploit rispetti i target ±10%.

**Ore-uomo.** 12h.

---

## P10 — LitQA2-style P vs NP regression benchmark
**Score 6.7 (impact 4, effort 3).**

**Descrizione.** Costruire 30 question-answer pair su P vs NP / proof complexity (derivabili da `pvsnp_compendium.py` + 5 risposte gold-labeled da Ludo). Suite consumata da `eval/gym.py` (P3). Ogni release / cambio modello → re-run, compara accuracy. Replica spirito LitQA2 di Aviary applicato al dominio P vs NP. Forza regressioni di routing-engine + LoRA a essere misurabili invece di silent.

**Motivazione.** FutureHouse Aviary LitQA2. https://arxiv.org/html/2412.21154v1.

**File/modulo.** `data/eval/suites/pvsnp_qa.yaml` (30 entries). Reuse `src/evaluation/gym.py` (P3).

**Primo test/azione.** Generare draft 30 QA via gemma3:4b + Ludo edit 5 gold; baseline accuracy run su provider chain. Target stable ≥ 60% per provider claude_max.

**Ore-uomo.** 10h.
