# 00_DISCOVERIES — sub-agent #5 (resto del server)

Date: 2026-05-13. Read-only audit, server `ludo@sec`.

Scoperte non documentate (o non chiare) nella memoria utente.

## D1 — sd-webui NON è A1111, è Forge (lllyasviel)

- Path: `~/sd-webui/` (14 GB)
- Git remote: `https://github.com/lllyasviel/stable-diffusion-webui-forge`
- Ultimi commit pulled: `dfdcbab6 Fix SD upscale Batch count (#2950)`, `d6b1d188 Add support for fp8 scaled (#2946)`, `715c24b0 Multithreading softinpainting (#2927)`
- Forge è già di per sé un upgrade di A1111 (più veloce, low-VRAM friendly). La memoria diceva "probabile A1111" -> aggiornare.
- Modelli: solo `sd_xl_base_1.0.safetensors`. Nessuna LoRA, nessun checkpoint custom.

## D2 — Driver NVIDIA è ROTTO

- `nvidia-smi` fallisce: `Failed to initialize NVML: Driver/library version mismatch ... NVML library version: 595.58`
- Significa che il modulo kernel e la userspace lib NVIDIA divergono → CUDA non utilizzabile finché non si reboota o reinstalla.
- Impatto: SD-WebUI, Wav2Lip, qualunque cosa CUDA è BROKEN. La capacity di video/audio AI di SEC è offline.
- Severità: ALTA. Va riportato a Ludo prima di proporre upgrades GPU-bound.

## D3 — systemd service `sec-entity.service` attivo 24/7

- Unit: `/etc/systemd/system/sec-entity.service`
- Description: "SEC Entity - Sentient Digital Child (24/7 living)"
- ExecStart: `/home/ludo/Scrivania/SEC/.venv/bin/python -m src gui --host 100.65.109.125 --port 8420 --with-daemon`
- Restart=always
- After=ollama.service. Stato: `loaded active running`.
- Listening su Tailscale IP (100.65.x) porta 8420 — accessibile da rete privata.
- Memoria utente menziona ENTITY ma non chiarisce che gira come systemd unit (24/7).

## D4 — `sd-webui` autostart at @reboot via crontab

- Linea crontab: `@reboot /home/ludo/sd-webui/start.sh >> /home/ludo/sd-webui/sd.log 2>&1`
- `start.sh` lancia `launch.py --api --nowebui --port 7860` → Forge gira solo come API server (no UI Gradio).
- Quindi c'è uno SD generation server perennemente in attesa, ma:
  - Solo sdxl_base, nessun LoRA → output generico.
  - GPU rotta (D2) → probabilmente in fallback CPU o crashato.

## D5 — `~/projects/` è scheletro di ex-scheduler vuoto

- 6 sotto-dir (create, experiment, explore, practice, reflect, research) con sotto-dir timestamped del 2026-04-02 / 03 — TUTTE vuote.
- Combaciano con `~/data/scheduler_state.json` che ha tutti i job (`health_check`, `model_update`, `lora_auto_train`, `dep_check`, `full_maintenance`) con `last_run: null, run_count: 0`.
- Sembra un sistema di scheduler iniziato il 2-3 aprile e mai eseguito (defunct).
- Aree morte: 6 subsys × ~10 micro-progetti vuoti ciascuno.

## D6 — `~/data/` ha DB SQLite ma sono VUOTI

- `sec.db` (68KB): tables `projects, tasks, messages, agent_metrics, code_artifacts, audit_log` — 0 righe in tutte.
- `sec_learning.db` (104KB): tables `task_feedback, prompt_history, error_patterns, knowledge_base, error_chains, cross_agent_lessons, quality_trends, error_reports` — 0 righe in tutte.
- `data/memory/knowledge_graph.db` e `data/entity/entity.db`: 4KB main + WAL files. Probabilmente schema creato, mai popolato.
- `data/adapters/`, `data/finetune/`, `data/modelfiles/`: tutte VUOTE.
- Sembra un altro sistema iniziato mai usato. Memoria utente NON menziona questi DB.

## D7 — Ollama service running + 7 modelli (alcuni nuovi vs memoria)

- `ollama.service` attiva.
- Modelli installati (8h fa): `qwen2.5-coder:3b/1.5b/7b`, `qwen3:8b`, `deepseek-r1:8b`, `gemma3:4b`, `nomic-embed-text`.
- Memoria utente cita solo `gemma3:4b`. Sono apparsi recentemente `qwen3:8b` e `deepseek-r1:8b` (entrambi nelle ultime 8h secondo il timestamp `MODIFIED`).
- Implicazione: c'è stata una sessione recente di download modelli — forse un setup di benchmark/swap LLM in corso.

## D8 — `~/Scrivania/pubblicazioni/` è solo SINK di report MD

- 44 file, tutti `report_YYYY-MM-DD.md` (40) o `ALERT_walls_YYYY-MM-DD.md` (6).
- Nessuno script Python, nessun .tex, nessun .pdf.
- Memoria utente conferma "sink report" — discovery: niente codice qui, è proprio solo output del daily_report cron.

## D9 — `~/tools/` contiene SOLO Wav2Lip

- Niente SadTalker, niente Hallo, niente EchoMimic, niente Wav2Lip-HD.
- Wav2Lip stesso fork pinato a `bac9a81 Update README.md` (commit di doc, niente upstream recente).
- Wav2Lip è del 2020 — è obsoleto, vedi 02_sota.md.

## D10 — `security_monitor.py` ogni 5 minuti

- `*/5 * * * * /usr/bin/python3 /home/ludo/kissat/pvnp_lab/lab_c001/scripts/security_monitor.py >> ... security.log`
- Non in scope nostro (pvnp_lab è di altro sub-agent), ma utile sapere che gira costantemente.

## D11 — `~/ssh` (file vuoto 0 bytes)

- `~/ssh` (no dot) — un file di 0 bytes, creato `Apr 10 15:58`. Probabilmente typo di Ludo (`touch ssh` invece di `cd ~/.ssh`). Innocuo.
