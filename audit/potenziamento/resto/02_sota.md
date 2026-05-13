# 02_sota — SOTA comparison (sub-agent #5)

Hardware target: RTX 3070 Ti, 8 GB VRAM (memoria utente). Driver NVIDIA attualmente rotto (vedi D2).

## 1. Lip-sync (Wav2Lip → SOTA)

Stato corrente: Wav2Lip originale 2020, fork `Rudrabha/Wav2Lip` solo doc-commit. Limiti: 96×96, no head pose, fragile su volti laterali.

### MuseTalk v1.5 (Tencent / TMElyralab) — RACCOMANDATO

- Paper: arXiv 2410.10122 (v3 = 2025). Codice: https://github.com/TMElyralab/MuseTalk
- v1.5 release 2025-03-28: aggiunta Perceptual Loss + GAN Loss + Sync Loss, two-stage training, qualità realistica.
- Real-time 30 fps+ su NVIDIA V100. Su RTX 30-series consumer è documentato "sufficient VRAM" per inference — generalmente sta in 6-8 GB con risoluzione 256-512.
- Latent-space inpainting (non genera tutto il volto, inpaint solo bocca) → veloce e identity-preserving.
- **Vincolo VRAM 8 GB: OK** (modello distillato in latent space, peso reale on-GPU ~3-4 GB).
- Fonti:
  - https://github.com/TMElyralab/MuseTalk
  - https://arxiv.org/html/2410.10122v3
  - https://huggingface.co/TMElyralab/MuseTalk

### LatentSync 1.6 (ByteDance) — qualità top, VRAM TOO HIGH

- Paper / repo: https://github.com/bytedance/LatentSync ; https://huggingface.co/ByteDance/LatentSync-1.6
- Release 1.6: 2025-06-11. Training su 512×512.
- **VRAM richiesta per inference: 18 GB** → NON sta in 8 GB nativo. Issue aperta #29 menziona tweak per ~4 GB ma non documentato come stabile.
- Fonti:
  - https://github.com/bytedance/LatentSync
  - https://github.com/bytedance/LatentSync/issues/29

### SadTalker — qualità media, head motion ottimo

- https://sadtalker.github.io/ ; https://github.com/OpenTalker/SadTalker
- Buono per "talking head da singola foto + audio" (head pose naturale, espressioni).
- Lip-sync accuracy meno precisa di Wav2Lip secondo benchmark community (3DMM approach).
- VRAM: ~6 GB.
- Caso d'uso: complementare a Wav2Lip/MuseTalk se serve animazione full-head da immagine statica.

### EchoMimic / Hallo

- EchoMimic: https://arxiv.org/html/2407.08136v1 — audio + landmarks, diffusion two-stage.
- Hallo: simile, diffusion two-stage.
- Costo computazionale alto, VRAM 12-16 GB tipica → fuori budget su 8 GB.

### Verdetto

**MuseTalk v1.5** = swap drop-in best per RTX 3070 Ti 8 GB. Wav2Lip resta utile come fallback CPU/low-resource.

---

## 2. Stable Diffusion WebUI (Forge → ?)

Stato corrente: `lllyasviel/stable-diffusion-webui-forge`, autostart API mode, solo `sd_xl_base_1.0`.

### ComfyUI (RACCOMANDATO per pipeline programmatic API)

- https://github.com/comfyanonymous/ComfyUI
- Node editor visuale ma **soprattutto** workflow JSON eseguibili da API → ideale per automation di SEC monetization.
- Smart memory management: offload GPU/RAM automatico, gira SDXL su 4 GB VRAM.
- Nuove architetture (Flux, Wan 2.1, HunyuanVideo, CHROMA) arrivano in ComfyUI settimane prima di Forge.
- Workflow JSON è introspectable, versionable in git, riproducibile.
- Fonti:
  - https://toolhalla.ai/blog/comfyui-vs-invokeai-vs-fooocus-2026
  - https://offlinecreator.com/blog/best-local-stable-diffusion-setup-2026

### Forge (attuale) — già migliore di A1111

- Speed: 30-75% > A1111. Best per utente medio "easy + fast". OK come è ora.
- Estensioni A1111 compatibili.
- BitsAndBytes (NF4/GGUF) per Flux: 11 GB → 4 GB.
- Limite: backend Forge è meno aggiornato di ComfyUI sui nuovi modelli (per nostro caso d'uso autonomo è marginale).

### SD.Next

- Più riche di feature ma più lento sviluppo. Non incrementa significativamente sul Forge esistente per il nostro use case.

### Verdetto

Per SEC monetization (automated content factory) → **affiancare ComfyUI a Forge**, non sostituire. ComfyUI per workflow JSON-API-driven, Forge resta per uso ad-hoc. Aggiungere Flux NF4 quantizzato come prima vera capability cross-stack.

---

## 3. Ollama fine-tune workflow (data/finetune, data/modelfiles)

Stato corrente: dirs vuote. Nessun adapter, nessun finetune attivo.

### Unsloth + QLoRA — RACCOMANDATO

- https://unsloth.ai/docs/get-started/fine-tuning-llms-guide
- 7B QLoRA fit in **8 GB VRAM**. Anche 8B sotto i 10 GB con seq≤512, batch=1, gradient checkpointing.
- Velocità: 2x più veloce di axolotl/HF stock su consumer.
- Workflow end-to-end:
  1. Curate dataset (500 esempi puliti > 5000 noisy).
  2. Train LoRA con Unsloth (afternoon).
  3. Merge adapter → base weights, export GGUF.
  4. `ollama create modelname -f Modelfile` (Modelfile referenzia il GGUF locale).
- Iperparametri safe: 1-3 epochs, lr=1e-4..2e-4, rank=16, gradient ckpt on.
- Fonti:
  - https://unsloth.ai/docs/get-started/fine-tuning-llms-guide
  - https://markaicode.com/ollama-fine-tuning-workflow/
  - https://developers.redhat.com/articles/2026/04/01/unsloth-and-training-hub-lightning-fast-lora-and-qlora-fine-tuning

### Axolotl

- YAML-driven config. Buono per pipeline reproducible. Più lento di Unsloth.

### Verdetto

Le dirs `~/data/{adapters,finetune,modelfiles}` sono **scheletro perfetto** per Unsloth + QLoRA. La pipeline auto-train (`lora_auto_train` in scheduler_state.json) può essere wirata a Unsloth → finetune di `qwen2.5-coder:3b` o `gemma3:4b` su dataset locale (pubblicazioni MD, conversation logs ENTITY).

---

## 4. ArXiv / OpenReview automation

Stato corrente: `~/Scrivania/pubblicazioni/` ha solo report MD; nessun submission tooling.

### arxiv (PyPI) + openreview-py

- `pip install arxiv` — wrapper API, ultima release 2026-04-12. https://pypi.org/project/arxiv/
- `pip install openreview-py` — client ufficiale OpenReview. https://github.com/openreview/openreview-py (Python 3.9+).
- arXiv API doc: https://info.arxiv.org/help/api/user-manual.html — supporta search + (con account) submission via SWORD.
- ICLR/NeurIPS hanno API OpenReview per pull metadata, review scores, dispute threads.

### CI/CD per LaTeX → arXiv

- arXiv/submission-tools (https://deepwiki.com/arXiv/submission-tools/6.4-cicd-pipelines): tex2pdf-service, tex2pdf-tools, pdf_profile. Validation + build pipeline standard.

### Verdetto

Per il workflow di Ludo (paper P vs NP, paper SEC) costruire una mini-pipeline `latex/ → tex2pdf → arxiv API publish` è 1-2 giornate di lavoro e renderebbe `~/Scrivania/pubblicazioni/` da sink-passivo a publishing-pipeline-attivo.

---

## 5. Multi-LLM benchmark / model swap

Stato corrente: 7 modelli Ollama (qwen2.5-coder 1.5/3/7B, qwen3:8b, deepseek-r1:8b, gemma3:4b, nomic-embed). Tutti modificati 8h prima dell'audit → segnale di sperimentazione attiva.

### lm-evaluation-harness / EleutherAI

- https://github.com/EleutherAI/lm-evaluation-harness (de facto standard 2026 benchmark)
- Supporta Ollama backend via plugin.
- Tasks: MMLU, GSM8K, HumanEval, MATH, IFEval.

### Use case proposto

Con i 7 modelli locali → mini-benchmark "qual è il miglior modello per la nostra workload SEC su 8 GB?" → output: csv di scores per task → driving auto-routing in ENTITY (model selection per task type).

---

## Costraints summary

| Modello | VRAM inference | Fit 8 GB? | Best driver state needed |
|---|---|---|---|
| MuseTalk v1.5 | ~4-6 GB | YES | CUDA OK |
| LatentSync 1.6 | 18 GB | NO | NO (out of budget) |
| SadTalker | ~6 GB | YES | CUDA OK |
| EchoMimic/Hallo | 12-16 GB | NO | NO |
| ComfyUI + SDXL | 4-8 GB con offload | YES | CUDA OK |
| ComfyUI + Flux NF4 | ~5-7 GB | YES | CUDA OK |
| Unsloth + 7B QLoRA | ~7-8 GB | YES (tight) | CUDA OK |

**Pre-condizione assoluta a TUTTI gli upgrade GPU:** fix driver NVIDIA mismatch.
