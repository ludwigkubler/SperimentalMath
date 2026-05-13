# 03_gaps — Gap analysis (sub-agent #5)

Score = Impact × (6 - Effort). Ordinato per Score desc.

| # | Sub-sistema | Tecnologia attuale | SOTA | URL SOTA | Impact (1-5) | Effort (1-5) | Score | VRAM 8GB? | Note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | GPU driver | Driver mismatch NVML 595.58 | nvidia-driver-555+ reinstall | https://www.nvidia.com/en-us/drivers/ | 5 | 1 | 25 | n/a | **BLOCKER assoluto**: senza fix tutto il resto è teorico. Reboot o purge+reinstall. |
| 2 | Lip-sync (Wav2Lip) | Wav2Lip 2020, 96×96 | MuseTalk v1.5 | https://github.com/TMElyralab/MuseTalk | 5 | 2 | 20 | Y | Drop-in replacement, real-time 30fps, identity-preserving |
| 3 | Finetune workflow | Vuoto (dirs scheletro) | Unsloth + QLoRA + Ollama Modelfile | https://unsloth.ai/docs/get-started/fine-tuning-llms-guide | 4 | 2 | 16 | Y (tight) | Wireare `lora_auto_train` esistente in scheduler_state.json |
| 4 | SD generation API | Forge solo SDXL base | ComfyUI + workflow JSON + Flux NF4 | https://github.com/comfyanonymous/ComfyUI | 4 | 2 | 16 | Y | Forge resta; ComfyUI affianca per pipeline programmatica |
| 5 | Model routing | Statico (ENTITY usa gemma3:4b) | Auto-routing via lm-eval benchmark | https://github.com/EleutherAI/lm-evaluation-harness | 3 | 2 | 12 | Y | Benchmark dei 7 modelli locali → cost/quality routing |
| 6 | Publication pipeline | Sink MD passivo | arxiv + openreview-py + tex2pdf | https://pypi.org/project/arxiv/ | 3 | 2 | 12 | n/a | Da "report sink" a "publishing pipeline" attivo |
| 7 | Defunct scheduler | scheduler_state.json + ~/projects/ vuoti | (a) revive con Unsloth o (b) archive+delete | https://docs.python.org/3/library/sched.html | 3 | 1 | 15 | n/a | Decisione binaria: usare o cancellare 6 dirs di scaffold morto |
| 8 | DB layer | sec.db, sec_learning.db, knowledge_graph.db vuoti | Wire produzione/consumo (es. ENTITY scrive lessons learned) | https://docs.python.org/3/library/sqlite3.html | 3 | 3 | 9 | n/a | Schema esiste, manca produttore. Risk: schema mai validato dall'uso. |
| 9 | SD models | Solo SDXL base | + Flux1.dev NF4, + SDXL Turbo, + 2-3 LoRA stilistiche | https://stable-diffusion-art.com/sdxl-vs-flux/ | 3 | 1 | 15 | Y (Flux NF4) | Asset enrichment, low effort |
|10 | Lip-sync alternative head motion | Solo Wav2Lip | + SadTalker | https://sadtalker.github.io/ | 2 | 2 | 8 | Y | Complementare a MuseTalk per "foto + audio → video full-head" |
|11 | Benchmark / observability | Nessun benchmark; nvidia-smi rotto | Add `gpustat`, `nvitop`, lm-eval cron weekly | https://github.com/wookayin/gpustat | 2 | 1 | 10 | n/a | Quick win operativo |
|12 | sd-webui auto-start | Solo Forge, no health-check | Add systemd unit con health-check + restart, fallback CPU | https://www.freedesktop.org/software/systemd/man/systemd.service.html | 2 | 2 | 8 | n/a | Sostituire cron @reboot con systemd unit + ExecStartPost health-check |

## Lettura

- **Tre BLOCKER+QUICKWIN** (#1 driver, #7 cleanup projects, #11 monitoring) sono effort 1, vanno fatti subito.
- **Tre BIG IMPACT upgrade** (#2 MuseTalk, #3 Unsloth, #4 ComfyUI) sono effort 2, sono le proposte chiave.
- **Layer dati vuoto (#8)** richiede design decision: chi scrive? Se ENTITY non li popola e nemmeno SEC, sono morti — meglio rimuovere lo schema o ricondurlo a un produttore reale.

## Vincoli ricorrenti

- Driver GPU rotto (D2) ricorre in 6 righe (#1-#5, #9, #10). Fix #1 sblocca tutta una catena.
- 8 GB VRAM esclude diffusion lip-sync top tier (LatentSync, EchoMimic, Hallo). MuseTalk è la scelta giusta.
- Modelli Ollama scaricati recenti (qwen3:8b, deepseek-r1:8b) suggeriscono sperimentazione attiva → benchmark è tempestivo.
