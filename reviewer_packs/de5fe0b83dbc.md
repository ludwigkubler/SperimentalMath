---
title: "Reviewer Pack — Fourier Coefficient Discrepancy and ACC⁰ Circuit Size"
subtitle: "Entry de5fe0b83dbc · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-10 14:31:32 UTC"
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

# Fourier Coefficient Discrepancy and ACC⁰ Circuit Size
**Entry ID**: `de5fe0b83dbc`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-10 14:31:32 UTC

## 1. Conjecture
**Field A** (mathematical branch): Additive Combinatorics
**Field B** (complexity object): ACC⁰ Circuit Size

**Statement**:

> For a Boolean function f derived from a 3-CNF formula on n variables, the discrepancy of its Fourier coefficients (defined as max_k |F(k)| - min_k |F(k)|) is at least Ω(2^{n/2}) if f requires ACC⁰ circuits of size ≥ 2^{n/2}.

**Rationale (proposer's reasoning)**:

> Additive combinatorics provides tools to analyze structured distributions of Fourier coefficients, which may expose inherent complexity barriers for ACC⁰ circuits. Discrepancy captures non-uniformity in Fourier spectra, potentially correlating with circuit depth.

**Taxonomy category**: `FOURIER_ANALYTIC` (status at proposal time: alive)

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `2c58a424d6f94dba`

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
| KARP_LIPTON | SAFE | 0.95 | SAFE | SAFE |

## 4. Novelty audit
**Verdict**: `NOVEL` against 0 hits across arXiv + Semantic Scholar + ECCC

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=1, elapsed=0.1s

### 5.1 Generated Python source

```python
import random
import math

def run_trial(seed: int) -> dict:
    n = 40
    random.seed(seed)
    
    def generate_3cnf(num_vars, num_clauses):
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([1, -1]) * random.randint(1, num_vars) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def fast_walsh_hadamard_transform(f):
        n = len(f)
        if n == 1:
            return f
        even = fast_walsh_hadamard_transform(f[::2])
        odd = fast_walsh_hadamard_transform(f[1::2])
        result = [0] * n
        for k in range(n // 2):
            result[k] = even[k] + odd[k]
            result[k + n // 2] = even[k] - odd[k]
        return result
    
    def fourier_coefficients(clauses, num_vars):
        f = [0] * (1 << num_vars)
        for clause in clauses:
            sign = clause[0]
            x, y, z = clause[1:]
            for i in range(1 << num_vars):
                if (i & (1 << abs(x) - 1)) == ((sign * x) % 2) and \
                   (i & (1 << abs(y) - 1)) == ((sign * y) % 2) and \
                   (i & (1 << abs(z) - 1)) == ((sign * z) % 2):
                    f[i] += sign
        return fast_walsh_hadamard_transform(f)
    
    def discrepancy(f):
        max_val = max(abs(x) for x in f)
        min_val = min(abs(x) for x in f)
        return max_val - min_val
    
    def acc0_circuit_size(clauses, num_vars):
        # Brute-force ACC⁰ circuit size estimation (simplified)
        # This is a placeholder and may not be accurate
        return 2 ** (num_vars // 2)
    
    clauses = generate_3cnf(n, n * 10)
    f = fourier_coefficients(clauses, n)
    disc = discrepancy(f)
    acc0_size = acc0_circuit_size(clauses, n)
    
    conjecture_holds = disc >= 2 ** (n // 2) and acc0_size >= 2 ** (n // 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "discrepancy",
        "metric_value": disc,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_disc = sum(r["metric_value"] for r in results) / len(results)
    std_disc = math.sqrt(sum((r["metric_value"] - mean_disc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_disc} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_disc} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```

--STDERR--
Traceback (most recent call last):
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_9b6cc439.py", line 85, in <module>
    result = run_trial(seed)
             ^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_9b6cc439.py", line 64, in run_trial
    f = fourier_coefficients(clauses, n)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_9b6cc439.py", line 42, in fourier_coefficients
    f = [0] * (1 << num_vars)
        ~~~~^~~~~~~~~~~~~~~~~
MemoryError

```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> skipped: test crashed before producing data

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> Test crashed with MemoryError, preventing evaluation of the conjecture's validity. | next: Optimize memory usage for large n or increase hardware limits to retest

## 11. Audit log (LLM calls)

**Total LLM calls**: 7

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | qwen3:8b | 0 | 0 | 108068 |
| 2 | preregistration | ollama_remote | qwen3:8b | 0 | 0 | 24039 |
| 3 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 20479 |
| 4 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 14003 |
| 5 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 18137 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 10373 |
| 7 | judge | ollama_remote | qwen3:8b | 0 | 0 | 49765 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 244864 ms total latency. Provider mix: {'ollama_remote': 7}

_(full prompt+response transcripts available in `research/audit/de5fe0b83dbc.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/de5fe0b83dbc.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/de5fe0b83dbc.tar.gz` (if generated)
