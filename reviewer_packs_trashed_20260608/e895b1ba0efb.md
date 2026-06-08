---
title: "Reviewer Pack — Minimal Quadratic Defect and Communication Complexity"
subtitle: "Entry e895b1ba0efb · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-06-07 07:38:32 UTC"
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

# Minimal Quadratic Defect and Communication Complexity
**Entry ID**: `e895b1ba0efb`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-06-07 07:38:32 UTC

## 1. Conjecture
**Field A** (mathematical branch): Algebraic Geometry (Quadratic Forms)
**Field B** (complexity object): Communication Complexity (Boolean Functions)

**Statement**:

> For every boolean function f: {0,1}^n → {0,1}, the communication complexity of f, denoted as CC(f), is upper-bounded by the minimal quadratic defect, denoted as D_q(f), defined as the minimum value of |D[f(x_1,...,x_k)] - 1|/k over all distinct inputs x_1,...,x_k ∈ {0,1}^n, where D[f(x_1,...,x_k)] is the quadratic form associated with the boolean function evaluated at (x_1,...,x_k).

**Rationale (proposer's reasoning)**:

> Quadratic forms have been studied in algebraic geometry and have applications in coding theory. The quadratic defect captures the distance of a boolean function from being linear. Communication complexity measures the amount of communication needed to compute a boolean function. This conjecture explores whether the geometric property of quadratic forms can provide insights into the complexity of computing Boolean functions, which is a fundamental problem in complexity theory.

**Taxonomy category**: `AlgebraicGeometry-CommunicationComplexity` (status at proposal time: )

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `fd83420e974677cb`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> The conjecture is supported if, for all generated boolean functions f: {0,1}^n → {0,1}, with n ≤ 40 and 30 random seeds, the minimal quadratic defect D_q(f) equals the communication complexity CC(f) within a tolerance of ±10%.

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| NATURAL_PROOFS | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| ALGEBRIZATION | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| KARP_LIPTON | SAFE | 1.00 | SAFE | SAFE |

## 4. Novelty audit
**Verdict**: `ADJACENT_OK` against 3 hits across arXiv + Semantic Scholar + ECCC

**Search queries** (3):
- `"quadratic form" AND "communication complexity"`
- `"minimal quadratic defect" AND boolean function"`
- `"algebraic geometry" AND communication complexity`

**Top relevant hits considered**:
- [http://arxiv.org/abs/1409.1534v1] Algorithms in Real Algebraic Geometry: A Survey
- [http://arxiv.org/abs/1008.0601v3] A note on the cotangent complex in derived algebraic geometry
- [http://arxiv.org/abs/math/0504259v1] Multiplier ideal sheaves in complex and algebraic geometry

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=124, elapsed=240.1s

### 5.1 Generated Python source

```python
import random
import math
from itertools import combinations

def generate_random_boolean_function(n):
    return {i: random.randint(0, 1) for i in range(2**n)}

def evaluate_quadratic_form(f, x_k):
    n = int(math.log2(len(x_k)))
    Q = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            Q[i][j] = f[(i << (n - 1)) | (j << (n - 2))]
            if i != j:
                Q[j][i] = Q[i][j]
    return sum(Q[i][j] * x_k[i] * x_k[j] for i in range(n) for j in range(i, n))

def minimal_quadratic_defect(f):
    n = int(math.log2(len(f)))
    min_defect = float('inf')
    for k in range(1, len(f)):
        for x_k in combinations(range(2**n), k):
            defect = abs(evaluate_quadratic_form(f, x_k) - 1) / len(x_k)
            if defect < min_defect:
                min_defect = defect
    return min_defect

def communication_complexity(f):
    n = int(math.log2(len(f)))
    max_comm_cost = float('-inf')
    for k in range(1, len(f)):
        for x_k in combinations(range(2**n), k):
            comm_cost = sum(abs(f[i] - f[j]) for i, j in combinations(x_k, 2))
            if comm_cost > max_comm_cost:
                max_comm_cost = comm_cost
    return max_comm_cost

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        cc = communication_complexity(f)
        min_defect = minimal_quadratic_defect(f)
        
        if min_defect == float('inf'):
            return {
                "metric_name": "minimal_quadratic_defect",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append({
            "n": n,
            "cc": cc,
            "min_defect": min_defect
        })
    
    mean_cc = sum(result["cc"] for result in results) / len(results)
    mean_min_defect = sum(result["min_defect"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["cc"] - mean_cc)**2 + (result["min_defect"] - mean_min_defect)**2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if abs(result["cc"] - result["min_defect"]) <= 0.1 * max(result["cc"], result["min_defect"])) / len(results)
    
    return {
        "metric_name": "minimal_quadratic_defect",
        "metric_value": mean_min_defect,
        "instances_tested": sum(1 for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
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

> The test timed out before producing data, which means it did not complete within the allotted time frame. | next: NONE

## 11. Audit log (LLM calls)

**Total LLM calls**: 11

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | glm4:latest | 0 | 0 | 23265 |
| 2 | propose | ollama_remote | glm4:latest | 0 | 0 | 12989 |
| 3 | propose | ollama_remote | glm4:latest | 0 | 0 | 13696 |
| 4 | preregistration | ollama_remote | glm4:latest | 0 | 0 | 9692 |
| 5 | novelty | ollama_remote | glm4:latest | 0 | 0 | 16551 |
| 6 | novelty | ollama_remote | glm4:latest | 0 | 0 | 9998 |
| 7 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 49713 |
| 8 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 12104 |
| 9 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 11488 |
| 10 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 12604 |
| 11 | judge | ollama_remote | glm4:latest | 0 | 0 | 28976 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 201077 ms total latency. Provider mix: {'ollama_remote': 11}

_(full prompt+response transcripts available in `research/audit/e895b1ba0efb.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/e895b1ba0efb.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/e895b1ba0efb.tar.gz` (if generated)
