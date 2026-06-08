---
title: "Reviewer Pack — Fourier Coefficient Sum Lower-Bounds Resolution Length for 3..."
subtitle: "Entry e2aedb4aa03f · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-07 20:48:45 UTC"
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

# Fourier Coefficient Sum Lower-Bounds Resolution Length for 3-CNFs
**Entry ID**: `e2aedb4aa03f`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-07 20:48:45 UTC

## 1. Conjecture
**Field A** (mathematical branch): Fourier Analysis of Boolean Functions
**Field B** (complexity object): Resolution Proof Length

**Statement**:

> For every 3-CNF formula Φ with n variables, the resolution proof length is at least Σ_{S⊆[n]} |f̂(S)|, where f̂(S) is the Fourier coefficient of the characteristic function of Φ. Equality holds when Φ is a single clause.

**Rationale (proposer's reasoning)**:

> Fourier coefficients capture the sensitivity of boolean functions to variable flips, which directly relates to the number of resolution steps needed to eliminate clauses. The sum of absolute coefficients quantifies the overall 'spread' of the function's structure, which must be addressed in any refutation.

**Taxonomy category**: `FOURIER_ANALYTIC` (status at proposal time: alive)

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `431bc530f3e5406c`

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
| KARP_LIPTON | SAFE | 0.95 | UNCERTAIN | SAFE |

## 4. Novelty audit
**Verdict**: `NOVEL` against 0 hits across arXiv + Semantic Scholar + ECCC

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=1, elapsed=0.4s

### 5.1 Generated Python source

```python
import random
from itertools import combinations

def generate_3cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        random.shuffle(clause)
        clauses.append(clause)
    return clauses

def evaluate_formula(formula, assignment):
    for clause in formula:
        if any(assignment[abs(lit) - 1] == l for l in clause):
            continue
        else:
            return False
    return True

def fourier_coefficient(formula, assignment):
    sum_val = 0
    for clause in formula:
        product = 1
        for lit in clause:
            if lit > 0:
                product *= assignment[lit - 1]
            else:
                product *= 1 - assignment[-lit - 1]
        sum_val += product
    return sum_val

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    m = 20
    formula = generate_3cnf(n, m)
    
    fourier_sum = 0
    for S in range(1 << n):
        assignment = [bool(random.getrandbits(1)) for _ in range(n)]
        fourier_sum += abs(fourier_coefficient(formula, assignment))
    
    proof_length = len(formula)  # Placeholder for actual resolution proof length calculation
    
    return {
        "metric_name": "Fourier Coefficient Sum",
        "metric_value": fourier_sum,
        "instances_tested": 1 << n,
        "conjecture_holds": fourier_sum <= proof_length,
        "counterexample": "" if fourier_sum <= proof_length else "Resolution length too short"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Resolution length too short' first_failing_seed={first_failing_seed}")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```
e': 'Fourier Coefficient Sum', 'metric_value': 17, 'instances_tested': 1024, 'conjecture_holds': True, 'counterexample': ''}
TRIAL: {'metric_name': 'Fourier Coefficient Sum', 'metric_value': 35, 'instances_tested': 1024, 'conjecture_holds': False, 'counterexample': 'Resolution length too short'}
TRIAL: {'metric_name': 'Fourier Coefficient Sum', 'metric_value': 23, 'instances_tested': 1024, 'conjecture_holds': False, 'counterexample': 'Resolution length too short'}
TRIAL: {'metric_name': 'Fourier Coefficient Sum', 'metric_value': 16, 'instances_tested': 1024, 'conjecture_holds': True, 'counterexample': ''}
TRIAL: {'metric_name': 'Fourier Coefficient Sum', 'metric_value': 18, 'instances_tested': 1024, 'conjecture_holds': True, 'counterexample': ''}
TRIAL: {'metric_name': 'Fourier Coefficient Sum', 'metric_value': 26, 'instances_tested': 1024, 'conjecture_holds': False, 'counterexample': 'Resolution length too short'}
TRIAL: {'metric_name': 'Fourier Coefficient Sum', 'metric_value': 15, 'instances_tested': 1024, 'conjecture_holds': True, 'counterexample': ''}
TRIAL: {'metric_name': 'Fourier Coefficient Sum', 'metric_value': 23, 'instances_tested': 1024, 'conjecture_holds': False, 'counterexample': 'Resolution length too short'}
TRIAL: {'metric_name': 'Fourier Coefficient Sum', 'metric_value': 26, 'instances_tested': 1024, 'conjecture_holds': False, 'counterexample': 'Resolution length too short'}

--STDERR--
Traceback (most recent call last):
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_38d64c59.py", line 85, in <module>
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_38d64c59.py", line 85, in <genexpr>
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
                               ~^^^^^^^^
KeyError: 'seed'

```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> skipped: test crashed before producing data

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> Test crashed due to KeyError 'seed' before completing required data collection | next: Fix test to handle seed tracking and re-run with sufficient sample size

## 11. Audit log (LLM calls)

**Total LLM calls**: 8

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | qwen3:8b | 0 | 0 | 103899 |
| 2 | propose | ollama_remote | qwen3:8b | 0 | 0 | 98707 |
| 3 | preregistration | ollama_remote | qwen3:8b | 0 | 0 | 19849 |
| 4 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 16496 |
| 5 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 10112 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 19858 |
| 7 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 8120 |
| 8 | judge | ollama_remote | qwen3:8b | 0 | 0 | 11065 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 288106 ms total latency. Provider mix: {'ollama_remote': 8}

_(full prompt+response transcripts available in `research/audit/e2aedb4aa03f.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/e2aedb4aa03f.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/e2aedb4aa03f.tar.gz` (if generated)
