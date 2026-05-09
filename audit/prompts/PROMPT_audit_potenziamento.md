# Prompt — AUDIT 2 di 2: potenziamento funzionalità (multi-agente, online)

Apri una nuova sessione di Claude Code (con ssh a `ludo@sec` + WebSearch
abilitato) e incolla esattamente questo prompt. **Lancia questo audit
DOPO l'audit di integrità** (PROMPT_audit_integrity.md) o in parallelo
in altra sessione.

---

# Audit di potenziamento: come massimizzare le funzionalità dei sistemi sul server

Sei un audit-conductor. Il tuo compito è valutare ciascuno dei sistemi
che girano sul server `ludo@sec`, confrontarli con lo stato dell'arte
pubblicato online (arXiv, GitHub, blog post, papers), e proporre
migliorie concrete.

## Vincoli

- **Solo lettura del server**. Non modificare codice, non installare
  pacchetti, non aggiornare niente senza esplicita richiesta dell'utente.
- Il tuo deliverable è una **lista di proposte ranked**, non
  un'implementazione. L'utente deciderà cosa adottare.
- Per ogni proposta: cita la fonte (URL del paper/repo), spiega cosa
  manca al sistema dell'utente, stima impact × effort.
- Non spendere più di ~15 minuti per sistema in WebSearch (per evitare
  rabbit hole). Se servono più ricerche, chiedi all'utente.

## Sistemi da auditare

L'utente ha quattro sistemi nominati + tutto ciò che il server contiene:

1. **SEC** (Self-sustaining research engine)
   - Path: `~/Scrivania/SEC/`
   - Cosa fa: secondo memoria, è un sistema autonomo 24/7 con 5 pipeline
     di monetization, agente con accesso completo al server, autonomy
     ON/OFF switch. Memoria: "5/7 capabilities reali (nmap, file R/W/edit,
     web search). Agent_spawn + self_fix deferred." E "Loop OBSERVE-THINK-
     ACT-VERIFY-LOG attivo, cron 6h, 6 attempts/3 successes test session,
     dry_run default."
   - Letteratura paragonabile: Smallville (Stanford), Voyager (NVIDIA),
     AI Scientist (Sakana 2024), Aviary (FutureHouse 2024), AutoGen
     (Microsoft), MetaGPT.

2. **PvsNP Lab**
   - Path: `~/kissat/pvnp_lab/`
   - Cosa fa: motore autonomo per attaccare P vs NP. Genera congetture,
     le testa, le valida (5-gate pipeline). Auto-sync su github
     `ludwigkubler/PvNP` e `ludwigkubler/SperimentalMath`.
   - Letteratura paragonabile: AI Scientist, FunSearch (DeepMind 2024),
     Lean copilot, GCT systems (Mulmuley-Sohoni), formal mathematics
     (Mizar, Coq, Lean 4, Mathlib4), AlphaProof (DeepMind 2024),
     LLM theorem provers (LeanDojo, Pythia).

3. **ENTITY**
   - Path: da scoprire (forse un sotto-modulo di SEC o standalone).
     Cerca con: `ssh ludo@sec "grep -rln 'class Entity\\|ENTITY_\\|entity_runtime\\|class.*Entity.*:' ~/ --include=\"*.py\" 2>/dev/null | head -20"`
   - Memoria utente: "SEC architecture: Multiagent + entity (full server
     access) + autonomia ON/OFF switch, lavora su pvnp_lab".
   - Quindi ENTITY sembra essere il "runtime" che dà a SEC accesso
     completo al server.
   - Letteratura paragonabile: Open-Interpreter, Aider, sweep.dev,
     CodeAgent (HuggingFace), Devin, swe-agent (Princeton), ReAct,
     ToolFormer.

4. **sperimentalmath**
   - Path: `~/Scrivania/future/` (subdirs: create, experiment, explore,
     practice, reflect, research) + sink github `ludwigkubler/SperimentalMath`
   - Cosa fa: output sink dell'engine PvsNP (verificato in audit di ieri).
     Storage di entry verificate / falsificate / inconclusive con Lean 4
     gates.
   - Letteratura paragonabile: AlphaGeometry, OpenAI o1-prover, Mathlib
     contributors automation, Conjecture (Lean tactic), Verified Compass.

5. **Tutto il resto** (scopri attivamente):
   - `~/sd-webui/`: Stable Diffusion webui (forse parte della monetization)
   - `~/tools/Wav2Lip/`: lip-sync per video (monetization)
   - `~/Scrivania/pubblicazioni/`: dove finiscono i report. È solo un sink
     o c'è codice di publishing?
   - Qualsiasi altra cartella con >50 file Python che non è in node_modules
     o venv.

## Architettura multi-agente

Spawna **5 sub-agent in parallelo** (`Agent` tool). Ognuno copre UN
sistema. Ogni sub-agent fa quattro cose:

### Per ogni sub-agent (pattern uniforme)

1. **Inventory funzionalità del sistema** (10-15 min):
   - Leggi i README/docstring/main entrypoint
   - Mappa: cosa fa il sistema, quali sono le capabilities chiave, quali
     sono le dipendenze, qual è l'architettura
   - Output: `audit/potenziamento/<sistema>/01_inventory.md`

2. **State-of-the-art comparison** (10-15 min, WebSearch):
   - Per ogni capability chiave, cerca online "<capability> SOTA 2025/2026"
   - Identifica 3-5 sistemi simili e cosa fanno meglio
   - Output: `audit/potenziamento/<sistema>/02_sota.md`
   - **Cita sempre URL di paper/repo concreti.**

3. **Gap analysis**:
   - Per ogni sistema simile: feature presente nello SOTA ma assente nel
     sistema dell'utente
   - Stima impact (1-5) × effort (1-5)
   - Output: `audit/potenziamento/<sistema>/03_gaps.md` con tabella
     ranked per impact/effort

4. **Proposte concrete** (top-10 per sistema):
   - Per ogni proposta: titolo, descrizione (≤100 parole), motivazione,
     riferimento bibliografico, file/modulo dell'utente da modificare,
     stima ore-uomo
   - Output: `audit/potenziamento/<sistema>/04_proposals.md`

### Sub-agent #1: SEC

Concentrati su: pipeline di monetization (gemma3:4b su RTX 3070 Ti),
autonomy loop, capabilities (file R/W/edit, web search, nmap),
agent_spawn (deferred), self_fix (deferred), few-shot examples,
ReAct loop, cron jobs.

Comparazione SOTA prioritaria:
- **Aviary** (https://github.com/Future-House/aviary) — agent gym for
  scientific tasks
- **AI Scientist** (Sakana, https://github.com/SakanaAI/AI-Scientist) —
  end-to-end automated paper writing
- **AutoGen** (Microsoft) — multi-agent framework
- **Smallville** (Stanford) — generative agents
- **Voyager** (NVIDIA) — lifelong learning agent

### Sub-agent #2: PvsNP Lab

Concentrati su: 5-gate pipeline, novelty filter, barrier checker
(dual LLM), Lean gate, sandbox (multi-seed test harness), proposer
prompt (recently patched), critic LLM, 6 framework live.

Comparazione SOTA prioritaria:
- **AlphaProof** (DeepMind 2024) — auto-formalization + proof search
- **AlphaGeometry** (DeepMind 2024) — for olympiad geometry
- **FunSearch** (DeepMind 2024) — LLM-guided program search for math
  conjectures
- **LeanDojo** (https://leandojo.org/) — Lean tactic prediction
- **AI Scientist** for the writeup pipeline

### Sub-agent #3: ENTITY

Prima task: **trova ENTITY**. Cerca con grep, leggi i file, capisci
l'architettura.

Concentrati su: come ENTITY dà accesso al server, quali tool ha, sandbox
o no, audit log, escalation path.

Comparazione SOTA prioritaria:
- **swe-agent** (Princeton, https://swe-agent.com/) — software engineering
  agent
- **Open-Interpreter** (Killian Lucas)
- **Aider** (Paul Gauthier)
- **Devin** (Cognition Labs) — closed but documented
- **CodeAgent** (HuggingFace transformers)
- **ToolFormer** (Meta) — paper

### Sub-agent #4: sperimentalmath

Concentrati su: l'output sink, la curation, i 4 sub-archivi
(notebook/, papers/, lean_verified/, frameworks/), retraction system,
crash rate da audit precedente.

Comparazione SOTA prioritaria:
- **OEIS** (Online Encyclopedia of Integer Sequences) — gold standard
  per math curation
- **PolyMath project** — collaborative math
- **Mathlib4** community — automated PR pipeline
- **AlphaGeometry / AlphaProof** writeup conventions

### Sub-agent #5: Resto del server

- `~/sd-webui/`: confronta con A1111 / ComfyUI ultime versioni
- `~/tools/Wav2Lip/`: confronta con Wav2Lip-HD, SadTalker, Hallo,
  EchoMimic ultime versioni — Wav2Lip originale è del 2020, molto
  superato
- `~/Scrivania/pubblicazioni/`: solo sink? Confronta con ArXiv submission
  automation, OpenReview pipelines, Overleaf-CLI

Anche: cerca attivamente altri sistemi non ancora identificati.
Pattern: `find ~/ -maxdepth 4 -name 'main.py' -o -name 'app.py' -o -name 'server.py' 2>/dev/null | head -30`.

## Coordinatore (tu)

Dopo che tutti i 5 sub-agent hanno consegnato:

1. **Synthesis**: produci `audit/potenziamento/SUMMARY.md` (max 250 righe):
   - Quale sistema è più maturo e quale ha più gap
   - Top 10 proposte cross-system ranked per (impact×effort)
   - Eventuali sinergie: feature presente in un sistema che potrebbe
     essere portata in un altro
   - 3 suggerimenti "quick wins" eseguibili in <1 settimana
   - 3 suggerimenti "moonshot" ad alto impatto e alto sforzo (>1 mese)

2. **Discoveries report**: se hai trovato sistemi/cartelle non documentati
   nella memoria utente, listali in `audit/potenziamento/00_DISCOVERIES.md`
   con cosa fanno e perché potrebbero essere rilevanti.

3. **Commit**: tutti i file sotto `audit/potenziamento/` su github
   SperimentalMath, commit message:
   `audit: functionality maximization (multi-agent, with SOTA comparison)`,
   firma: `Signed: Ludovico Kubler`. Push.

4. **Final summary all'utente** (≤400 parole): top 5 proposte con (impact,
   effort, dove modificare), link al SUMMARY, eventuali discoveries di
   sistemi non noti.

## Vincoli aggiuntivi

- **Non bloating**: l'utente non vuole un wishlist da 200 voci. Ogni
  sub-agent deve fermarsi a 10 proposte top per sistema. Il SUMMARY deve
  selezionare le 10 cross-system migliori.
- **Onestà**: se uno SOTA è già implementato nel sistema dell'utente,
  riconoscilo. Non inventare gap.
- **Pratico**: ogni proposta deve avere un "primo file da modificare" o
  "primo test da eseguire" concreto. No "research direction" senza
  azione.
- **Royal-Society standard**: ogni proposta deve essere giustificata da
  almeno un riferimento concreto (paper su arXiv, repo GitHub, post
  tecnico). Niente proposte da "best practice generica".

## Output finale richiesto

- Cartella `audit/potenziamento/` su github SperimentalMath con:
  - `00_DISCOVERIES.md` (scoperte di sistemi non noti)
  - `<sistema>/01_inventory.md`, `02_sota.md`, `03_gaps.md`,
    `04_proposals.md` per ognuno dei 5 sistemi
  - `SUMMARY.md` con top-10 cross-system + 3 quick wins + 3 moonshot
- Commit + push fatto
- Risposta finale all'utente (≤400 parole)

Inizia ora.
