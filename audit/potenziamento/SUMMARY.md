# Audit potenziamento — SUMMARY cross-system

**Date**: 2026-05-13. **Audit conductor**: Claude Opus 4.7. **Sub-agents**: 5
(SEC, PvsNP Lab, ENTITY, sperimentalmath, resto). **Wall-clock**: ~6 min in
parallelo. **WebSearch totale**: ~25 query. **Server**: `ludo@sec` (read-only).

## Sintesi maturità

| Sistema | Maturità | Gap principali |
|---|---|---|
| SEC | **Alta** — molti SOTA già implementati (Park scoring, Reflexion, skills-lite, learning_hooks). Cron monetization disabilitato dal 2026-04-23. | Reflection trigger, Voyager skills eseguibili, Aviary gym, MCTS |
| PvsNP Lab | **Alta** — 11.706 LOC, 708 entries, pipeline dual-LLM live. F4 framework engine già scritto (679 LOC) ma listato "planned". | Premise retrieval, LeanDojo persistent kernel, autoformalize corpus, FunSearch |
| ENTITY | **Media-alta** — sandbox shell sorprendentemente forte; self_improve ReAct loop 863 LOC con rollback. | Audit log strutturato assente; `.entityrules` mancante; ACI viewer; sub-agent spawn deferred |
| sperimentalmath | **Bassa** — pipeline multi-agent paper-only (skeptic gate non invocato 405 volte in 168h). Path reale: `git_mirrors/SperimentalMath/` (non `~/Scrivania/future/`). | Retraction propagator, AST stub-detector, INDEX+badge, Lean Real-valued port |
| Resto server | **Critico operativo** — driver NVIDIA rotto (NVML mismatch). 7 modelli Ollama scaricati 8h prima audit, nessun benchmark. | Driver fix BLOCKER; Wav2Lip→MuseTalk; Unsloth pipeline; ComfyUI accanto a Forge |

## Top-10 cross-system (ranked per Impact × leverage / Effort)

| # | Sistema | Proposta | URL ispirazione | Ore | Score | Note |
|---|---|---|---|---|---|---|
| 1 | resto | **P1 Fix driver NVIDIA** — `nvidia-smi` rotto, NVML mismatch | https://forums.developer.nvidia.com/t/nvml-driver-library-version-mismatch/167948 | 0.5-2 | **BLOCKER** | Sblocca ogni capability GPU-bound (sd-webui, Wav2Lip, Ollama HW). Probabile solo reboot. |
| 2 | sperimentalmath | **P1 Retraction propagator** — `reports/supported_findings.md` mostra 4 SUPPORTED che `retractions.json` ha già retracted | https://retractionwatch.com/ | 4-6 | **Reputazione** | Repo pubblico ludwigkubler/SperimentalMath dichiara entry come SUPPORTED che sono falsificate. Rischio se Ludo cita pubblicamente. |
| 3 | ENTITY | **P1 Audit log strutturato** (tabella `tool_calls`) | swe-agent ACI | 2-3 | 25 | Forensics oggi impossibile. Quick win foundation per ogni RL/learning futuro. |
| 4 | SEC | **P1 Park-style reflection loop** — completa metà mancante Generative-Agents | arXiv:2304.03442 | 6 | 12.5 | `scoring.py` Park-style già presente; manca solo trigger di reflection→3 questions→new memories. |
| 5 | sperimentalmath | **P2 AST stub auditor** — Gate 1 enforcement automatico | https://leanprover-community.github.io/contribute/index.html | 8-12 | Alto | Detector che avrebbe catturato tutti i 4 SUPPORTED retracted retroattivamente. Previene recidiva. |
| 6 | SEC | **P2 Voyager executable skills** — `skills.py` esplicitamente skippa code-exec | arXiv:2305.16291 | 8 | 12.5 | Promuove skills da prompt-templates a funzioni callable (RestrictedPython). Compounding reuse. |
| 7 | resto | **P2 Wav2Lip → MuseTalk v1.5** | https://github.com/TMElyralab/MuseTalk | 3-5 | Alto | Drop-in real-time latent-space lip-sync. Wav2Lip 2020 è obsoleto. 8GB VRAM OK. ROI diretto su content factory SEC. |
| 8 | pvnp_lab | **P1 Premise retrieval (ReProver)** sul Lean gate | arXiv:2306.15626 | 14 | Alto | ≥2× pass@1 lift previsto; Mathlib già su disco (zero costo indicizzazione). |
| 9 | ENTITY | **P2 `.entityrules` policy file** | https://cognition.ai/blog/devin-2 | 3-4 | Alto | NEVER_TOUCH / ALLOWED_COMMANDS oggi hardcoded in 2 file. Pattern `.cursorrules` standard de facto. |
| 10 | pvnp_lab | **P2 LeanDojo persistent kernel** — cycle 6 min → 30 s | https://leandojo.org/ | 16 | Strategico | Abilita MCTS/best-first che oggi sono troppo cari (P6 sblocca). |

## 3 Quick Wins (esecuzione in 1 settimana totale)

**Tutti e tre realizzabili in ~8h cumulative; nessuno richiede architettura nuova.**

1. **Fix driver NVIDIA** (resto P1, 0.5-2h) — reboot o `apt purge nvidia-* && apt install nvidia-driver-555`. Primo test: `python -c "import torch; print(torch.cuda.is_available())"` → True. **Sblocca tutto il resto della factory video/audio.**

2. **ENTITY audit log strutturato** (ENTITY P1, 2-3h) — tabella SQLite `tool_calls` in `entity.db`. Modifica `src/entity/memory/store.py` (schema) + `src/entity/living/tool_executor.py` (wrap). Primo test: `SELECT tool_name, COUNT(*) FROM tool_calls GROUP BY tool_name;` ritorna ≥1 riga dopo 1h. **Foundation per debugging, RL, analytics.**

3. **Retraction propagator** (sperimentalmath P1, 4-6h) — script `apply_retractions.py` legge `retractions.json` e propaga ai report MD. Hook in `sync_output.sh`. Primo test: dopo run, `supported_findings.md` ha zero entry non-retracted. **Reputazione su repo pubblico.**

## 3 Moonshot (>1 mese, alto impatto)

1. **AI Scientist v2-style end-to-end manuscript loop** (combinazione pvnp_lab P8+P9, SEC P6+P8, ~40h+). Pipeline: agentic tree search sui conjecture moves → FunSearch islands per test → VLM critic su figure → multi-pass writeup con peer-review simulation. Sakana arXiv:2504.08066. *Potrebbe diventare la flagship feature di PvsNP Lab.*

2. **Symbolic deduction engine per proof complexity** (pvnp_lab P5, 40h+). Mini DDAR-style su CNF/treewidth/Tseitin. Pattern AlphaGeometry2 (DDAR risolve 84% delle olimpiadi geometria *senza* LM — arXiv:2502.03544). Asimmetria "deducer cheap first, LLM expensive only when stalled". *Trasformazione architetturale del Lean gate.*

3. **Sub-agent orchestration + capability gating fine-grained** (ENTITY P10 + P3 + SEC P6+P8 debate panel, ~40-60h). Spawn sub-agent isolati con sandbox subset di tool. Gate per pattern regex + max_uses_per_hour. Pattern Devin (cognition.ai/blog/devin-2). *Sblocca parallelismo reale per task lunghi (es. "analizza 100 paper").*

## Sinergie cross-system

- **Observability foundation**: ENTITY P1 (audit log) + ENTITY P9 (confirmation persist) + SEC P3 (Aviary gym) + SEC P4 (OTel exporter) → costruiscono insieme la base measurability che roadmap SEC chiama "non-negoziabile".
- **Compounding knowledge bases**: SEC P2 (Voyager executable skills) + pvnp_lab P7 (PvNPCommon lemma reuse) + sperimentalmath P3 (INDEX+badges) → tre libreries componibili (Python skills, Lean lemmi, math entries) che si rafforzano a vicenda.
- **Fine-tune pipeline**: resto P3 (Unsloth bootstrap) + pvnp_lab P3 (autoformalize corpus nightly LoRA) — entrambi necessitano driver fixed (resto P1) e popolano `~/data/adapters/` oggi vuoto.
- **Anti-stub defense**: sperimentalmath P2 (AST auditor) + sperimentalmath P10 (submission checklist) + pvnp_lab P10 (negative curriculum) → tre layer che impediscono ricomparsa di entries falsate.

## Frecce d'attenzione

- **Sicurezza ENTITY**: `python` in `ALLOWED_COMMANDS` → `python -c "os.system(...)"` bypassa allowlist comando-livello. Mitigazione: ENTITY P7 (Docker-wrap shell HIGH/CRITICAL, 4-6h).
- **PvsNP roadmap timing**: AlphaProof Nature paper uscito 2025-11-12 (recente). PvsNP Lab roadmap V2 (Apr 2026) menziona "tactic search Level 1-3" ma non ancora MCTS/RL. Finestra di assorbimento aperta.
- **Memoria utente stale**: lean_verified/ non è più vuoto (4 entries dal 2026-04-26). Tropical Fourier 4 FALSIFIED → 3 re-retracted, principal output collassato a 1. Path sink reale è `git_mirrors/SperimentalMath/` non `~/Scrivania/future/`.

## Stima totale

- 10 proposte top: **~78h** (1 sprint developer = 2 settimane intense).
- 3 quick wins: **~8h** (1 giornata).
- 3 moonshot: **~120-160h** (1-2 mesi).

## Output completo

Ogni sistema ha 4 file (5 per resto, include `00_DISCOVERIES.md`):
`/tmp/audit_potenziamento/{SEC,pvnp_lab,ENTITY,sperimentalmath,resto}/0{1,2,3,4}_*.md`
Totale: **21 file, 2492 righe**.

---

*Audit firmato: Ludovico Kubler*
