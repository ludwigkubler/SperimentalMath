# 04_proposals — Proposte concrete (sub-agent #5)

Massimo 10 proposte cross-subsistema, ordine per priority (driver-fix + alta-leva prima).

## P1 — Fix driver NVIDIA mismatch (BLOCKER)

- **Titolo**: Restore CUDA / NVML coherence prima di qualunque upgrade GPU-bound.
- **Descrizione**: `nvidia-smi` fallisce con `NVML library version: 595.58 ... Driver/library version mismatch`. Significa modulo kernel vs userspace lib divergono. Tipico dopo `apt upgrade` senza reboot, o dopo install parziale.
- **Motivazione + URL**:
  - Senza CUDA funzionante, sd-webui-forge gira in CPU fallback (lentissimo) o crasha; Wav2Lip non parte; Ollama gira su CPU (qwen2.5-coder:7b → ~2 tok/s vs 30+ tok/s su GPU).
  - https://forums.developer.nvidia.com/t/nvml-driver-library-version-mismatch/167948
- **File/dir target sul server**: kernel module + userspace lib. Tipica fix:
  1. `lsmod | grep nvidia` per vedere se modulo è caricato.
  2. `sudo reboot` (most common fix se è solo lib aggiornata ma modulo vecchio).
  3. Se reboot non basta: `sudo apt purge nvidia-* && sudo apt install nvidia-driver-555` (versione coerente con CUDA toolkit installato).
- **Primo test**: `nvidia-smi` ritorna tabella senza errore; `python3 -c "import torch; print(torch.cuda.is_available())"` → True.
- **Ore-uomo**: 0.5-2h (dipende se basta reboot o serve purge+reinstall).
- **Vincolo VRAM**: n/a.

## P2 — Drop-in upgrade Wav2Lip → MuseTalk v1.5

- **Titolo**: Sostituire Wav2Lip con MuseTalk v1.5 in `~/tools/`.
- **Descrizione**: MuseTalk v1.5 di Tencent fa lip-sync in latent space (inpainting solo zona bocca), 30fps+ real-time, identity-preserving. Wav2Lip 2020 è 96×96 e mostra artifacts su volti laterali.
- **Motivazione + URL**:
  - Paper: https://arxiv.org/html/2410.10122v3
  - Repo: https://github.com/TMElyralab/MuseTalk
  - HF: https://huggingface.co/TMElyralab/MuseTalk
  - SEC content factory (video AI pipeline) ne beneficia direttamente.
- **File/dir target sul server**: `~/tools/MuseTalk/` (nuovo, accanto a Wav2Lip — non rimuovere Wav2Lip subito, è fallback CPU).
- **Primo test**:
  ```bash
  cd ~/tools && git clone https://github.com/TMElyralab/MuseTalk.git
  cd MuseTalk && pip install -r requirements.txt
  # scaricare modelli da HF
  python scripts/inference.py --inference_config configs/inference/test.yaml
  ```
- **Ore-uomo**: 3-5h (setup + dipendenze + 1 video di test).
- **Vincolo VRAM**: 8 GB OK (latent-space, ~4-6 GB tipica).

## P3 — Bootstrap Unsloth + QLoRA fine-tune pipeline

- **Titolo**: Riempire `~/data/{adapters,finetune,modelfiles}` con pipeline Unsloth funzionante.
- **Descrizione**: Le 3 dirs sono vuote ma `scheduler_state.json` definisce un job `lora_auto_train` (mai eseguito). Wirare Unsloth come backend: finetune di `qwen2.5-coder:3b` (o `gemma3:4b`) su dataset locale (es. report MD `~/Scrivania/pubblicazioni/`, conversation logs ENTITY).
- **Motivazione + URL**:
  - https://unsloth.ai/docs/get-started/fine-tuning-llms-guide
  - https://markaicode.com/ollama-fine-tuning-workflow/
  - 7B QLoRA fit in 8 GB VRAM (vincolo critico per noi).
- **File/dir target sul server**:
  - Script in nuovo `~/data/finetune/train.py` (Unsloth).
  - Output adapter in `~/data/adapters/<model-task>-lora.safetensors`.
  - Merged GGUF in `~/data/modelfiles/<model-task>.gguf` + Modelfile `FROM ./model.gguf`.
- **Primo test**:
  ```bash
  pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
  # train su 100 samples dummy
  python ~/data/finetune/train.py --base qwen2.5-coder:3b --data sample.jsonl --epochs 1
  # merge + GGUF + ollama create
  ollama create qwen-coder-pvnp -f ~/data/modelfiles/Modelfile
  ollama run qwen-coder-pvnp "lemma probability bound..."
  ```
- **Ore-uomo**: 8-12h (pipeline end-to-end + 1 finetune reale).
- **Vincolo VRAM**: 8 GB tight (rank=16, batch=1, seq≤512). 3B-4B più sicuri di 7B.

## P4 — Add ComfyUI accanto a Forge per pipeline JSON-API

- **Titolo**: Installare ComfyUI accanto a Forge per workflow programmatic API.
- **Descrizione**: Forge è ottimo per uso umano. ComfyUI è ottimo per **automation**: workflow JSON eseguibili da Python API, versionabili in git, riproducibili. SEC content factory ha bisogno di workflow image-gen riproducibili.
- **Motivazione + URL**:
  - https://github.com/comfyanonymous/ComfyUI
  - https://offlinecreator.com/blog/best-local-stable-diffusion-setup-2026
  - ComfyUI offload smart: SDXL gira su 4 GB; supporta Flux NF4 in ~5-7 GB.
- **File/dir target sul server**: `~/comfyui/` (nuovo), condividere `models/` con Forge via symlink (`ln -s ~/sd-webui/models/Stable-diffusion ~/comfyui/models/checkpoints` etc).
- **Primo test**:
  ```bash
  git clone https://github.com/comfyanonymous/ComfyUI.git ~/comfyui
  cd ~/comfyui && python -m venv venv && source venv/bin/activate
  pip install -r requirements.txt
  # symlink shared models
  ln -s ~/sd-webui/models/Stable-diffusion ~/comfyui/models/checkpoints
  python main.py --listen 127.0.0.1 --port 8188
  # POST /prompt con workflow JSON tester
  curl -X POST http://127.0.0.1:8188/prompt -d @workflow_sdxl_basic.json
  ```
- **Ore-uomo**: 4-6h (install + symlinks + 1 workflow JSON di esempio).
- **Vincolo VRAM**: 8 GB OK con offload automatico.

## P5 — Cleanup defunct scheduler + ~/projects/

- **Titolo**: Archiviare o eliminare lo scaffold morto `~/projects/` e decidere il destino di `scheduler_state.json`.
- **Descrizione**: 6 sotto-dir thematic (`create/experiment/explore/practice/reflect/research`) contengono ~60+ sotto-sotto-dir timestamped del 2026-04-02/03, **tutte vuote**. Lo state file scheduler ha tutti i job con `last_run=null`. Sistema mai partito.
- **Motivazione + URL**:
  - Sporcizia operativa, induce in errore audit futuri (vedi questo che ha consumato tempo per esaminarle).
  - Decisione binaria: revive (P3 può usare `lora_auto_train`) o `tar czf ~/archived_projects_20260513.tgz ~/projects ~/data/scheduler_state.json && rm -rf ~/projects` (read-only durante audit, ma per fase implementazione).
- **File/dir target sul server**: `~/projects/`, `~/data/scheduler_state.json`.
- **Primo test**: `du -sh ~/projects/*` per confermare emptiness, poi decision call.
- **Ore-uomo**: 0.5h.
- **Vincolo VRAM**: n/a.

## P6 — Multi-model benchmark con lm-evaluation-harness

- **Titolo**: Benchmark dei 7 modelli Ollama → tabella score per task → driving rules ENTITY model selection.
- **Descrizione**: 7 modelli installati (qwen2.5-coder 1.5/3/7B, qwen3:8b, deepseek-r1:8b, gemma3:4b, nomic-embed). Nessuno sa quale è migliore per quale task. lm-evaluation-harness produce score consistenti.
- **Motivazione + URL**:
  - https://github.com/EleutherAI/lm-evaluation-harness
  - I 7 modelli sono stati pull-ati ~8h fa (modificati di recente) → ipotesi: Ludo sta sperimentando, dati a supporto sarebbero utili.
- **File/dir target sul server**: `~/data/benchmarks/` (da creare). CSV output. Output anche in `~/Scrivania/pubblicazioni/benchmarks_YYYY-MM-DD.md` (sink esistente).
- **Primo test**:
  ```bash
  pip install lm-eval
  lm_eval --model ollama --model_args base_url=http://localhost:11434,model=gemma3:4b \
    --tasks mmlu,gsm8k,humaneval --output_path ~/data/benchmarks/gemma3_4b.json
  ```
- **Ore-uomo**: 4-6h (eseguire 3 task × 7 modelli ~6h GPU + parsing).
- **Vincolo VRAM**: 8 GB OK (modelli max 8b).

## P7 — Replace cron `@reboot sd-webui` with systemd unit

- **Titolo**: Promuovere sd-webui da `cron @reboot` a `sd-webui.service` systemd.
- **Descrizione**: cron @reboot non fa restart su crash, no health-check, no logging strutturato. systemd dà Restart=always, journalctl integration, ordering (`After=ollama.service`).
- **Motivazione + URL**:
  - Pattern identico già in uso per `sec-entity.service`.
  - https://www.freedesktop.org/software/systemd/man/systemd.service.html
- **File/dir target sul server**: `/etc/systemd/system/sd-webui.service` (nuovo). Rimuovere riga cron `@reboot`.
- **Primo test**:
  ```bash
  sudo cp /tmp/sd-webui.service /etc/systemd/system/
  sudo systemctl daemon-reload && sudo systemctl enable --now sd-webui
  sudo systemctl status sd-webui
  curl http://127.0.0.1:7860/sdapi/v1/sd-models  # API check
  ```
- **Ore-uomo**: 1-2h.
- **Vincolo VRAM**: n/a (operations).

## P8 — Wire pubblicazioni/ a arxiv + openreview submission pipeline

- **Titolo**: Da sink passivo a publishing-pipeline-attivo per `~/Scrivania/pubblicazioni/`.
- **Descrizione**: Aggiungere uno script `submit_arxiv.py` che, dato un `paper.tex` + bibliography, costruisce PDF e invia a arXiv via SWORD API.
- **Motivazione + URL**:
  - https://pypi.org/project/arxiv/
  - https://github.com/openreview/openreview-py
  - https://info.arxiv.org/help/api/user-manual.html
- **File/dir target sul server**: `~/Scrivania/pubblicazioni/papers/<topic>/{paper.tex,bib,figures}` + `~/Scrivania/pubblicazioni/tools/submit.py`.
- **Primo test**:
  ```bash
  pip install arxiv openreview-py
  python -c "import arxiv; r = arxiv.Client().results(arxiv.Search(query='P vs NP'))"
  # quindi un dry-run di submission con file tex già pronto
  ```
- **Ore-uomo**: 8-16h (full pipeline + LaTeX build + arXiv account configuration).
- **Vincolo VRAM**: n/a.

## P9 — Add Flux NF4 + 2-3 LoRA stilistiche a sd-webui

- **Titolo**: Asset enrichment SDXL/Flux per content factory SEC.
- **Descrizione**: Attualmente solo `sd_xl_base_1.0`. Aggiungere `flux1-dev-bnb-nf4.safetensors` (~6.7 GB, sta in 8 GB con offload) e 2-3 LoRA stilistiche tematiche (es. anime, photography, illustration).
- **Motivazione + URL**:
  - Flux supera SDXL su prompt adherence, text rendering, anatomia. https://stable-diffusion-art.com/sdxl-vs-flux/
  - Flux1.dev BnB NF4: https://huggingface.co/lllyasviel/flux1-dev-bnb-nf4
- **File/dir target sul server**: `~/sd-webui/models/Stable-diffusion/flux1-dev-bnb-nf4.safetensors`, `~/sd-webui/models/Lora/<style>.safetensors`.
- **Primo test**: Forge ha switch automatico per Flux NF4. Curl `POST /sdapi/v1/txt2img` con `override_settings.sd_model_checkpoint = "flux1-dev-bnb-nf4"`.
- **Ore-uomo**: 1-2h (download + smoke test).
- **Vincolo VRAM**: 8 GB OK con NF4.

## P10 — Quick observability: gpustat + nvitop + systemd journals

- **Titolo**: Quick win operativo — strumenti di monitoring leggeri.
- **Descrizione**: `nvidia-smi` rotto. Installare `gpustat` + `nvitop` per monitor leggibile, e un cron daily che dumpa `systemctl status sec-entity ollama sd-webui` in un file leggibile.
- **Motivazione + URL**:
  - https://github.com/wookayin/gpustat
  - https://github.com/Syllo/nvtop
- **File/dir target sul server**: nessun nuovo file di codice. Solo `pip install --user gpustat`, `apt install nvtop`. Aggiungere cron `0 7 * * * systemctl status sec-entity ollama > ~/Scrivania/pubblicazioni/health_$(date +\%F).txt`.
- **Primo test**: `gpustat` (dopo fix driver P1) → mostra utilization, processes, VRAM.
- **Ore-uomo**: 0.5h.
- **Vincolo VRAM**: n/a.

---

## Priorità d'esecuzione consigliata

1. **P1 (driver fix)** — blocca tutto il resto, 0.5-2h.
2. **P5 (cleanup) + P10 (monitoring)** — quick wins, < 1h totali.
3. **P2 (MuseTalk)** — più alto ROI di tutti gli upgrade.
4. **P3 (Unsloth)** + **P4 (ComfyUI)** — sblocca capability nuove (finetune locale, automation image gen).
5. **P6, P7, P8, P9** — incrementi.
