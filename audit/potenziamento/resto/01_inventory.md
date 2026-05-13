# 01_inventory — resto del server (sub-agent #5)

Server: `ludo@sec`. Cwd: `/home/ludo/`. Solo dirs/sistemi NON coperti dagli altri 4 sub-agent.

## A. SD Generation stack (`~/sd-webui/`)

- Fork: `stable-diffusion-webui-forge` (lllyasviel). 14 GB on disk.
- Mode: API only (`--api --nowebui --port 7860`), no Gradio UI.
- Autostart: cron `@reboot ~/sd-webui/start.sh`.
- Modelli:
  - `Stable-diffusion/sd_xl_base_1.0.safetensors` (solo questo)
  - `Lora/`: vuoto
  - `embeddings/`: presente come dir (non ispezionata in dettaglio)
  - `ControlNet/`, `ESRGAN/`, `GFPGAN/`, `Codeformer/`, `VAE/`, `karlo/`, `svd/`, `z123/`, `text_encoder/`, `diffusers/`, `hypernetworks/`, `deepbooru/`: presenti come dirs
- Extension dir custom: vuota (solo `extensions-builtin/`).
- Versione: commit `dfdcbab6` (presumibilmente recente, ma NEWS.md è ferma a 2024 Oct, branch `sd35`).
- Vincolo: **driver NVIDIA rotto** (NVML 595.58 mismatch) → questo server non può attualmente generare in GPU mode.

## B. Lip-sync / video stack (`~/tools/Wav2Lip/`)

- Fork: `Rudrabha/Wav2Lip` (originale, paper ACM MM 2020).
- Commit corrente: `bac9a81 Update README.md` (commit di solo doc).
- Checkpoints: solo `wav2lip_gan.pth`.
- `~/tools/` contiene **solo Wav2Lip** (no SadTalker, no Hallo, no MuseTalk, no LatentSync, no EchoMimic).
- Wav2Lip è ufficialmente non manutenuto, lip-sync grossolano 96×96, no head movement.

## C. Publications sink (`~/Scrivania/pubblicazioni/`)

- 180 KB totali, 44 file MD.
- Pattern: `report_YYYY-MM-DD.md` (40 file, daily 2026-04-04 → 2026-05-12) + `ALERT_walls_YYYY-MM-DD.md` (6).
- Generato da cron `daily_report.py` di pvnp_lab (non in scope).
- Nessuno script in questa dir.
- Non c'è automation di submit ArXiv / OpenReview.

## D. Projects scaffold MORTO (`~/projects/`)

- 1.5 MB, 6 sotto-dir tematiche.
- Tutte le sotto-sotto-dir create il **2026-04-02/03**, tutte VUOTE.
- Subdir counts: create 8, experiment 5, explore 8, practice 24, reflect ~10, research 11.
- Tipico naming: `physics_simulation_20260402_215732`, `algorithm_kata_20260402_231829`, `research_proof_complexity_20260402_231214`.
- Correla con scheduler_state.json: tutti i job hanno `last_run=null, run_count=0`.
- DIAGNOSI: sistema di "scheduled research projects" mai eseguito, abbandonato. Candidato a archiviazione/cleanup.

## E. Data layer (`~/data/`)

- `~/data/scheduler_state.json` (2.5 KB): definisce 5 job tracker (`health_check 5min`, `model_update 6h`, `dep_check 12h`, `full_maintenance 24h`, `lora_auto_train 6h`). Tutti con `enabled=true` ma `last_run=null`. Stato: scheduler MAI partito o stato resettato.
- `~/data/sec.db` (68 KB): schema `projects/tasks/messages/agent_metrics/code_artifacts/audit_log` — TUTTE 0 righe. Vuoto.
- `~/data/sec_learning.db` (104 KB): schema `task_feedback/prompt_history/error_patterns/knowledge_base/error_chains/cross_agent_lessons/quality_trends/error_reports` — TUTTE 0 righe. Vuoto.
- `~/data/memory/knowledge_graph.db` (4 KB + WAL): schema-only, probabilmente non popolato.
- `~/data/entity/entity.db` (4 KB + WAL): schema-only.
- `~/data/adapters/`, `~/data/finetune/`, `~/data/modelfiles/`: EMPTY.
- DIAGNOSI: layer di persistence pronto ma nessun produttore di dati lo sta scrivendo.

## F. Ollama (system service)

- `ollama.service`: loaded active running.
- 7 modelli locali totali ~22 GB:
  - LLM coding: `qwen2.5-coder:1.5b/3b/7b`
  - LLM reasoning/general: `qwen3:8b`, `deepseek-r1:8b`, `gemma3:4b`
  - Embedding: `nomic-embed-text:latest`
- Tutti modificati ~8h prima dell'audit (sospetta pull recente).

## G. systemd services attivi (rilevanti)

- `ollama.service` — running.
- `sec-entity.service` — running (cf. D3). Working dir `~/Scrivania/SEC/`, ascolta su 100.65.109.125:8420.
- `ssh.service` — running.

## H. Crontab attivo (12 entry totali, riassunto)

- `*/5` watchdog pvnp_lab
- `*/5` security_monitor pvnp_lab
- `0 18` daily_report
- `0 9` c003b_counterexample
- `0 8` literature_scan
- `0 23` git_sync pvnp_lab
- `0 3` cleanup_videos SEC monetization
- `@reboot` sd-webui start.sh
- (commentati: content factory video)

## I. GPU / VRAM

- Driver NVIDIA installato ma NVML library 595.58 in mismatch col kernel.
- `nvidia-smi` non funziona attualmente.
- Modello GPU (da memoria utente): **RTX 3070 Ti, 8 GB VRAM**.
- Vincolo per upgrade: qualunque modello SOTA deve stare in 8 GB (con offload accettato).

## J. Disk / Filesystem

- Root: 1 TB totale, 122 GB usati, 844 GB liberi (12% pieno). Spazio abbondante.
- Uso per dir di scope:
  - sd-webui: 14 GB
  - tools/Wav2Lip: 505 MB
  - data: 756 KB
  - projects: 1.5 MB
  - pubblicazioni: 180 KB

## K. Networking / esposizione

- ENTITY ascolta su Tailscale IP (100.65.x) porta 8420.
- SD-WebUI API su porta 7860 (locale, --api).
- ssh server attivo.

## Sommario quick

- **Vivo e in produzione**: sec-entity systemd, ollama, crontab pvnp_lab, sd-webui API auto-start.
- **Morto / scaffold inutile**: `~/projects/` (vuoto), `~/data/*.db` (vuoti), `~/data/{adapters,finetune,modelfiles}/` (vuoti), scheduler_state.json (mai usato).
- **Critico**: driver NVIDIA rotto → tutto il GPU stack è in failure mode.
- **Obsoleto e upgradabile**: Wav2Lip 2020, sd-webui Forge senza LoRA/ControlNet pratici.
