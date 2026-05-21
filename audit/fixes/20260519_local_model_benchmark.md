# Local Model Benchmark — 7 models × 3 tasks (2026-05-19)

**Sentinel:** `sec_local_model_mix_v2`
**Hardware:** RTX 3070 Ti 8 GB VRAM
**Method:** real prompts extracted from `audit/_global*.jsonl`, run via Ollama API, structurally graded (no LLM judge).

---

## Models tested

| Model | Size on disk | Source |
|:---|---:|:---|
| `qwen3:8b` | 5.2 GB | incumbent (reasoning) |
| `qwen2.5-coder:7b` | 4.7 GB | incumbent (coding) |
| `deepseek-r1:8b` | 5.2 GB | already on disk, unused |
| `glm4:latest` | 5.5 GB | new pull (THUDM 9B) |
| `command-r7b:latest` | 5.1 GB | new pull (Cohere 7B) |
| `mistral-nemo:latest` | 7.1 GB | new pull (Mistral 12B) |
| `phi4:latest` | 9.1 GB | new pull (MS 14B) |

## Tasks

Real prompts extracted from the audit log (5 sec ago to days ago):

| Task | System | User | Notes |
|:---|---:|---:|:---|
| `test_gen` | 2,396 chars | 3,892 chars | Generate Python test code for conjecture |
| `propose` | 2,216 chars | 14,911 chars | Propose new conjecture with full blacklist |
| `judge` | 639 chars | 2,519 chars | JSON verdict on test output |

Generation params: `temperature=0.3` (test_gen), `0.7` (propose), `0.1` (judge); `num_ctx=16384` for propose, 8192 elsewhere; `num_predict` 400-1200; **timeout 240s**.

---

## Results

### Latency (seconds, lower is better)

| task | qwen3:8b | qwen2.5-c:7b | deepseek-r1 | glm4 | cmd-r7b | mistral-nemo | phi4 |
|:---|---:|---:|---:|---:|---:|---:|---:|
| test_gen | 152.0 | **17.7** | 151.2 | 62.0 | ⏱ | ⏱ | ⏱ |
| propose | ⏱ | 171.4 | ⏱ | 197.0 | **124.9** | ⏱ | ⏱ |
| judge | 107.3 | **29.3** | 104.1 | 40.7 | 95.2 | 132.2 | ⏱ |

⏱ = timeout at 240 s

### Tokens / sec (higher is better)

| task | qwen3:8b | qwen2.5-c:7b | deepseek-r1 | glm4 | cmd-r7b | mistral-nemo | phi4 |
|:---|---:|---:|---:|---:|---:|---:|---:|
| test_gen | 24.6 | 68.3 | 24.6 | **92.4** | – | – | – |
| propose | – | 1.7 | – | 2.1 | **3.6** | – | – |
| judge | 25.7 | **106.5** | 25.6 | 94.5 | 3.6 | 0.9 | – |

### Structural score (out of 100)

| task | qwen3:8b | qwen2.5-c:7b | deepseek-r1 | glm4 | cmd-r7b | mistral-nemo | phi4 |
|:---|---:|---:|---:|---:|---:|---:|---:|
| test_gen | 0 | **100** | 0 | **100** | err | err | err |
| propose | err | 90 | err | 90 | **90** | err | err |
| judge | **100** | **100** | 0 | **100** | **100** | **100** | err |

---

## Findings

### `glm4:latest` — clear winner for reasoning role

- **2.6× faster** wall clock on `judge` than `qwen3:8b` (40.7s vs 107.3s)
- **3.7× higher tok/s** (94.5 vs 25.7)
- Same structural score (100)
- Same VRAM footprint (5.5 GB vs 5.2 GB)
- Also fastest tok/s on `test_gen` (92.4) among models that completed
- Completes `propose` task (only 3 of 7 models did)

### `qwen2.5-coder:7b` — KEEP for coding

- Already incumbent for `coding` task
- Best wall clock on `test_gen` (17.7 s, score 100)
- Best wall clock + tok/s on `judge` (29.3 s, 106.5 tok/s, score 100)
- Surprisingly competent on `propose` (score 90 — though slow at 1.7 tok/s)

### `deepseek-r1:8b` — UNSUITABLE despite hype

- Score 0 on `test_gen` and `judge`
- R1-family wraps every output in `<think>...</think>` reasoning chain
- The reasoning chain consumes the `num_predict` budget BEFORE producing the final answer
- Result: outputs are truncated reasoning, with no valid JSON or code at the end
- **Do not use as drop-in replacement for non-reasoning tasks**

### `phi4:latest` — does not fit 8 GB VRAM

- 9.1 GB Q4 model on 8 GB VRAM → all 3 tasks timed out at 240 s
- Either runs partially-on-CPU (slow) or fails to load
- **Not viable on current hardware**

### `mistral-nemo:latest` — too slow

- 12B model in 7.1 GB Q4 — barely fits, KV cache pushes into swap
- 0.9 tok/s on `judge` (132 s for 47 tokens) — useless throughput
- Produces correct structural output but at glacial pace
- **Not viable for high-frequency tasks**

### `command-r7b:latest` — niche

- Fits well (5.1 GB), produces correct outputs
- But unusually slow: 3.6 tok/s on judge despite 7B model
- Best on `propose` task (124.9 s, score 90), but Claude Opus is much better
- **Keep on disk; may be useful for specific high-context tasks**

---

## Router changes (`sec_local_model_mix_v2`)

`src/orchestration/router.py` `DEFAULT_MODEL_MAP["ollama_remote"]`:

```diff
-    "reasoning": "qwen3:8b",
+    "reasoning": "glm4:latest",
-    "conversation": "qwen3:8b",
+    "conversation": "glm4:latest",
-    "general": "qwen3:8b",
+    "general": "glm4:latest",
```

`ollama_local` (used as fallback when `ollama_remote` unreachable) keeps `qwen3:8b` for reasoning because `glm4:latest` would also need to be pulled on the local machine if/when this fallback path is exercised (it currently isn't).

**Claude Opus retained** for `propose`, `judge`, `critic`, `novelty`, `preregistration` — quality of those tasks is too important to trade for cost savings. Structural score doesn't measure mathematical novelty.

---

## Estimated impact

From the 24h audit log (1624 calls):
- 496 calls to `qwen3:8b` (reasoning) now go to `glm4:latest`
- At 40 s/call vs 107 s/call → **~9h/day saved on local inference**
- No quality regression (both score 100 on structural metrics)
- No VRAM cost (5.5 vs 5.2 GB)

---

## Procedure to revert

```bash
TS=20260521_092416
cp /home/ludo/Scrivania/SEC/src/orchestration/router.py.bak.${TS} \
   /home/ludo/Scrivania/SEC/src/orchestration/router.py
```

Models on disk to optionally clean up (`ollama rm <name>`):
- `phi4:latest` (9.1 GB) — doesn't fit 8 GB VRAM
- `mistral-nemo:latest` (7.1 GB) — too slow
- `deepseek-r1:8b` (5.2 GB) — wraps output in `<think>` tags
- `command-r7b:latest` (5.1 GB) — niche use; keep if disk OK

Disk reclaimable: ~26 GB. Currently disk is at 13%, so cleanup is optional.

---

## Raw data

- `/tmp/benchmark_results.json` on server (latencies, outputs, eval counts)
- `/tmp/benchmark_grades.json` on server (structural scores)
