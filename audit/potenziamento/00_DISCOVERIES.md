# 00_DISCOVERIES — Audit potenziamento 2026-05-13

Scoperte trasversali ai 5 sub-audit. Cose **non documentate o non chiare** nella
memoria utente al 2026-05-13, raccolte da tutti i sub-agent durante il sweep
read-only di `ludo@sec`.

## Operativi / Infrastruttura

### D1 — Driver NVIDIA è ROTTO ora (BLOCKER)
`nvidia-smi` fallisce con `Failed to initialize NVML: Driver/library version mismatch ... NVML library version: 595.58`. Modulo kernel divergente dalla userspace lib. Impatto: sd-webui-forge, Wav2Lip, Ollama HW-accel sono in fallback CPU o crashati. **Tutta la capacity GPU del server è offline.** Severità ALTA. Fix tipico: reboot. Vedi resto/04_proposals.md P1.

### D2 — `sec-entity.service` è un systemd unit attivo 24/7
`/etc/systemd/system/sec-entity.service`, `Restart=always`, `After=ollama.service`, `loaded active running`. Ascolta su Tailscale IP `100.65.109.125:8420`. Memoria utente menziona ENTITY ma non chiarisce che gira come systemd unit 24/7.

### D3 — sd-webui è **Forge**, non A1111
Git remote `https://github.com/lllyasviel/stable-diffusion-webui-forge`. Forge è già upgrade A1111 (più veloce, low-VRAM friendly). Avvio: `@reboot /home/ludo/sd-webui/start.sh` via crontab → `launch.py --api --nowebui --port 7860`. Solo `sd_xl_base_1.0` installato; nessuna LoRA.

### D4 — `~/projects/` è scaffold MORTO
6 sub-dir (create, experiment, explore, practice, reflect, research) con sub-sub-dir timestamped 2026-04-02/03, **tutte vuote**. Combacia con `~/data/scheduler_state.json` che ha **tutti i 5 job con `last_run=null, run_count=0`**. Sistema iniziato il 2-3 aprile e mai eseguito. Candidato all'archiviazione.

### D5 — DB SQLite tutti VUOTI
`sec.db`, `sec_learning.db`, `knowledge_graph.db`, `entity.db`: schema definiti (`projects, tasks, agent_metrics, task_feedback, prompt_history, error_patterns, knowledge_base, error_chains, cross_agent_lessons`, ecc.) ma **0 righe in tutte le tabelle**. Sistemi mai popolati. Memoria utente non li cita.

### D6 — 7 modelli Ollama scaricati 8h prima audit
`qwen2.5-coder:1.5b/3b/7b`, `qwen3:8b`, `deepseek-r1:8b`, `gemma3:4b`, `nomic-embed-text`. Memoria cita solo `gemma3:4b`. `qwen3:8b` e `deepseek-r1:8b` apparsi nelle 8h prima dell'audit. Implicazione: sessione recente di sperimentazione/benchmark in corso, ma nessuna tabella di confronto trovata.

### D7 — `~/tools/` contiene SOLO Wav2Lip 2020
Niente SadTalker, Hallo, EchoMimic, Wav2Lip-HD, MuseTalk, LatentSync. Wav2Lip pinato a commit di doc (`bac9a81`). 6 anni di SOTA video-AI mancanti dal toolkit.

### D8 — `~/Scrivania/pubblicazioni/` è solo SINK passivo
44 file totali, tutti `report_YYYY-MM-DD.md` (40) o `ALERT_walls_YYYY-MM-DD.md` (6). Nessun .py, .tex, .pdf. È output del daily report cron, non pipeline di publishing. (Era ambiguo dalla memoria.)

### D9 — `security_monitor.py` ogni 5 minuti
Cron: `*/5 * * * * /usr/bin/python3 /home/ludo/kissat/pvnp_lab/lab_c001/scripts/security_monitor.py >> ... security.log`. Gira costantemente. Non in scope di nessun sub-agent specifico.

### D10 — `~/ssh` (file vuoto, no dot) — innocuo
0 bytes, creato Apr 10 15:58. Probabile typo (`touch ssh` invece di `cd ~/.ssh`).

## SOTA già implementati ma non documentati (SEC)

### D11 — Park weighted retrieval già presente
`~/Scrivania/SEC/src/memory/scoring.py` implementa la formula `recency·importance·relevance` di Park 2023 (Generative Agents §3-4). Memoria utente non lo cita. **Manca solo la reflection trigger** (SEC P1).

### D12 — Voyager-lite skills library già presente
`~/Scrivania/SEC/src/entity/memory/skills.py` ha schema `skills(name, description, embedding, …)`. Commento esplicito nel file: "we skip the code-execution component" — è il salto qualitativo mancante per renderle Voyager-style eseguibili (SEC P2).

### D13 — Reflexion engine già presente
`~/Scrivania/SEC/src/entity/learning/reflexion.py` implementa Shinn 2023 Reflexion. Memoria utente non lo cita.

### D14 — `learning_hooks.py` post-task pipeline già attivo
`~/Scrivania/SEC/src/core/learning_hooks.py` con `on_task_complete()` esistente. Soglia hardcoded 0.7 (vedi SEC P5 verifier per-agent).

### D15 — 11 provider in `orchestration/router.py` (non 7)
Inclusi `claude_max`, `claude_pro_sonnet`, `claude_pro_haiku`, locali Ollama. Memoria parla di 7 capability ma il router gestisce 11 provider distinti.

### D16 — `self_improve.py` ReAct loop 863 LOC con risk-gating e env-toggled auto-apply
Memoria dice "agent_spawn + self_fix deferred", ma `src/entity/living/self_improve.py` è una ReAct loop OBSERVE-THINK-ACT-VERIFY-LOG completa, con whitelist + NEVER_TOUCH + rollback automatico su syntax check fail. Manca solo differential testing (ENTITY P4).

### D17 — Cron monetization DISABILITATO dal 2026-04-23
Solo `cleanup_videos.py` rimane attivo. Roadmap 3 (revenue) è di fatto in standby. Commento di disabilitazione: "focus on P vs NP".

## SOTA già implementati ma non documentati (PvsNP)

### D18 — F4 framework engine GIÀ scritto (679 LOC) ma listato "planned"
`~/kissat/pvnp_lab/system_v2/src/pvsnp_framework.py` con `fitness`, `mutate`, `elaborate`. README dichiara F4 "planned". Probabilmente serve solo wiring nel living loop.

### D19 — Mathlib già su disco
`~/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib`. Zero costo per il retriever proposto in pvnp_lab P1.

### D20 — Manca cross-conjecture lemma reuse
Ogni FORMAL_VERIFIED stub è isolato in un lake project monouso. Grosso opportunity cost (pvnp_lab P7 `PvNPCommon`).

### D21 — AlphaProof Nature paper recente (2025-11-12)
Finestra di assorbimento aperta. Roadmap V2 PvsNP Lab (Apr 2026) menziona "tactic search Level 1-3" ma non ancora MCTS/RL.

## ENTITY discoveries

### D22 — Sandbox shell sorprendentemente forte
`ALLOWED_COMMANDS` ~80 binari + `BLOCKED_PATTERNS` (fork-bomb, `systemctl start`, `journalctl --vacuum`) + tokenizer shell-aware con segment split. Migliore della maggioranza di agent runtimes confrontati.

### D23 — Buco di sicurezza: `python` in ALLOWED_COMMANDS
`python -c "import os; os.system('rm -rf ~')"` bypassa allowlist comando-livello. Mitigazione: ENTITY P7 (Docker-wrap risk-based).

### D24 — Audit log strutturato ASSENTE
Solo `self_improve_log.jsonl` e `self_fix_tickets` sono strutturati. Tutto il resto è "diary narrativo" non queryable. `confirmation_gate._history` è in-memory, perso al restart. Forensics impossibile (ENTITY P1+P9).

## sperimentalmath discoveries

### D25 — Path reale è `git_mirrors/SperimentalMath/` (non `~/Scrivania/future/`)
`~/Scrivania/SEC/research/git_mirrors/SperimentalMath/` è il sink vero, hourly-synced a `ludwigkubler/SperimentalMath`. `~/Scrivania/future/` contiene 3903 SEC self-tasks LLM toy files, non collegati. **Memoria utente da correggere.**

### D26 — lean_verified/ NON è più vuoto
4 entries dal 2026-04-26. **Ma**: `e14f176e4ef1/Eaudit.lean` self-admette "Float-based proofs are NOT rigorous over the reals" — verifica è su IEEE-754, non `ℝ`. Onesto, ma debole (sperimentalmath P7 porta a `IntervalArith`).

### D27 — Skeptic gate non invocato 405 volte in 168h
`MULTIAGENT_PIPELINE.md §3.1` definisce Gate 1 ma `health_report.skeptic_168h.not_invoked = 405`. 0 hardened, 0 downgraded. Pipeline multi-agent è "paper-only" — gate non runtime.

### D28 — 3/4 FALSIFIED Tropical Fourier RE-retracted
`retractions.json`: 3 dei 4 FALSIFIED entries hanno bug nel test (TFT definition). Principal scientific output collassato a **1 entry sopravvissuta**. Memoria utente "4 FALSIFIED Tropical Fourier reali" da aggiornare.

### D29 — `frameworks/dead/` vuoto nonostante 18 BARRIER_HIT
`stats.json` reports 18 BARRIER_HIT; README promette post-mortem; directory vuota.

### D30 — Public reports lie about 4 SUPPORTED
`reports/supported_findings.md` lista 4 entries come SUPPORTED. `retractions.json` ha già retracted/demoted tutte e 4. Rischio reputazione se repo pubblico viene citato.

## Implicazioni per la memoria utente

Da aggiornare in `~/.claude/projects/-home-ludo-kissat/memory/`:

1. **project_sperimentalmath_audit.md**: aggiornare path sink (`git_mirrors/SperimentalMath`), aggiornare stato (lean_verified non più vuoto; Tropical Fourier 1 entry residua).
2. **project_sec_capabilities.md**: aggiornare "5/7 capabilities reali" → 11 provider router; Park scoring, Voyager skills, Reflexion già implementati.
3. **project_sec_self_improve.md**: già ReAct loop completa 863 LOC, non "deferred" come da memoria.
4. **project_sec_revenue.md**: cron monetization disabilitato dal 2026-04-23 ("focus on P vs NP").
5. Nuova: **project_server_infrastructure.md** con D2 (sec-entity.service), D3 (Forge), D5 (DB vuoti), D6 (Ollama models).
6. Nuova: **project_nvidia_blocker.md** con D1 (driver mismatch, da fixare prima di GPU ops).
