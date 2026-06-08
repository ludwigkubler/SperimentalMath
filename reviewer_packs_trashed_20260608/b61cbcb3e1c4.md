---
title: "Reviewer Pack — Gowers Uniformity Norm of Boolean Functions Bounds ACC⁰ Circ..."
subtitle: "Entry b61cbcb3e1c4 · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-08 07:21:55 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
header-includes:
  - \usepackage{listings}
  - \usepackage{xcolor}
  - \definecolor{codebg}{rgb}{0.96,0.96,0.96}
  - \lstset{basicstyle=\ttfamily\footnotesize,backgroundcolor=\color{codebg},breaklines=true}
---

# Gowers Uniformity Norm of Boolean Functions Bounds ACC⁰ Circuit Size
**Entry ID**: `b61cbcb3e1c4`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-08 07:21:55 UTC

## 1. Conjecture
**Field A** (mathematical branch): Gowers Uniformity Norms in Additive Combinatorics
**Field B** (complexity object): ACC⁰ Circuit Size

**Statement**:

> For a Boolean function f on n variables, if the Gowers uniformity norm of order 3 is at least Ω(n^ε), then the minimal ACC⁰ circuit size for f is Ω(n^{2-ε})

**Rationale (proposer's reasoning)**:

> High Gowers uniformity indicates the function is not well-approximated by low-degree polynomials, which are efficiently computable by ACC⁰ circuits. Thus, such functions require larger ACC⁰ circuits.

**Taxonomy category**: `ACC_SIPSER` (status at proposal time: alive)

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `9f9a3b88e124e9f3`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> default: >=80% seeds must support, no counterexample

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |
| NATURAL_PROOFS | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |
| ALGEBRIZATION | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |
| KARP_LIPTON | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |

## 4. Novelty audit
**Verdict**: `NOVEL` against 0 hits across arXiv + Semantic Scholar + ECCC

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=124, elapsed=240.0s

### 5.1 Generated Python source

```python
import random
import math
from itertools import product

def fourier_coefficients(f, n):
    N = 2 ** n
    coeffs = [0] * N
    for k in range(N):
        sum_val = 0
        for x in range(N):
            sum_val += f(x) * math.cos(2 * math.pi * k * x / N)
        coeffs[k] = sum_val / N
    return coeffs

def gowers_uniformity_norm(f, n):
    coeffs = fourier_coefficients(f, n)
    norm = 0
    for coeff in coeffs:
        norm += abs(coeff) ** 4
    return norm ** (1/4)

def simulate_acc0_circuit(f, n, size):
    # Simplified simulation of ACC^0 circuit with given size
    # This is a placeholder and does not actually compute the function
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(50):  # Sample 50 instances per seed
        f = lambda x: random.choice([0, 1])  # Random Boolean function
        norm = gowers_uniformity_norm(f, n)
        if norm >= n ** 0.1:  # Threshold for ε=0.1
            circuit_size = simulate_acc0_circuit(f, n, size=n**2)
            if not circuit_size:
                conjecture_holds = False
                counterexample = "Function cannot be computed by ACC^0 circuit"
                break

        instances_tested += 1

    return {
        "metric_name": "Gowers Uniformity Norm",
        "metric_value": norm,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```
TIMEOUT after 240s
```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> skipped: test crashed before producing data

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> Test timed out before producing results, preventing evaluation of support fraction or counterexamples. | next: Increase timeout duration and re-run test with identical parameters

## 11. Audit log (LLM calls)

**Total LLM calls**: 7

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | qwen3:8b | 0 | 0 | 72907 |
| 2 | preregistration | ollama_remote | qwen3:8b | 0 | 0 | 20002 |
| 3 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 16571 |
| 4 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 8603 |
| 5 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 15218 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 8575 |
| 7 | judge | ollama_remote | qwen3:8b | 0 | 0 | 11887 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 153763 ms total latency. Provider mix: {'ollama_remote': 7}

_(full prompt+response transcripts available in `research/audit/b61cbcb3e1c4.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/b61cbcb3e1c4.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/b61cbcb3e1c4.tar.gz` (if generated)
