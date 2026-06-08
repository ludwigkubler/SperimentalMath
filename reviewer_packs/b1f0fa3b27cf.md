---
title: "Reviewer Pack — Specht Module Dimensions Bound ABP Size for Permutation Poly..."
subtitle: "Entry b1f0fa3b27cf · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-04-24 22:27:00 UTC"
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

# Specht Module Dimensions Bound ABP Size for Permutation Polynomials
**Entry ID**: `b1f0fa3b27cf`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-04-24 22:27:00 UTC

## 1. Conjecture
**Field A** (mathematical branch): Representation theory of symmetric groups
**Field B** (complexity object): Algebraic branching programs (ABPs)

**Statement**:

> For any permutation polynomial f ∈ GF(2)[x_1,…,x_n], the minimal ABP size required to compute f is at most the dimension of the Specht module S^λ corresponding to its Young diagram λ, where λ is determined by the cycle type of f's permutation action.

**Rationale (proposer's reasoning)**:

> Specht modules encode combinatorial constraints on permutation symmetries, which may translate to algebraic complexity bounds via Barrington's theorem. The Young diagram's shape reflects the function's decomposition into irreducible representations, potentially limiting the required ABP width.

**Taxonomy category**: `BARRINGTON_ALG` (status at proposal time: partially_alive)

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `3a9097c5e05cb45a`

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
**Verdict**: `NOVEL` against 7 hits across arXiv + Semantic Scholar + ECCC

**Search queries** (5):
- `Specht module ABP permutation polynomial`
- `Specht module dimension ABP permutation polynomial`
- `symmetric group representation ABP permutation polynomial`
- `Specht module GF(2) ABP permutation polynomial`
- `Specht module dimension algebraic branching program permutation polynomial bound`

**Top relevant hits considered**:
- [http://arxiv.org/abs/2502.18759v1] Some permutation polynomials via linear translators
- [http://arxiv.org/abs/2506.15133v1] A Specht Filtration of Permutation Modules Over KLR Algebras
- [http://arxiv.org/abs/1203.5751v2] Permutation resolutions for Specht modules of Hecke algebras
- [http://arxiv.org/abs/1101.2456v3] Polynomial representations and categorifications of Fock Space
- [http://arxiv.org/abs/hep-ph/0610012v1] Tevatron-for-LHC Report of the QCD Working Group
- [http://arxiv.org/abs/1511.00322v2] Five Constructions of Permutation Polynomials over $\gf(q^2)$
- [http://arxiv.org/abs/math/9902088v1] Specht Modules and Branching Rules for Ariki-Koike Algebras

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=1, elapsed=0.1s

### 5.1 Generated Python source

```python
import random
import math
import sys
import json

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(shape):
    n = len(shape)
    total = 0
    for row in range(n):
        for col in range(len(shape[row])):
            hook = shape[row][col] + (n - row) - 1 + (len(shape[row]) - col) - 1
            total += hook // gcd(hook, n * (n - row))
    return factorial(n * n) // total

def cycle_type_to_shape(cycle_type):
    shape = [0] * len(cycle_type)
    for length in cycle_type:
        shape[length - 1] += 1
    return shape

def abp_size(permutation, width):
    n = len(permutation)
    dp = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        dp[i][i] = 1
        for j in range(i - 1, -1, -1):
            for k in range(j, i):
                if permutation[k] == permutation[j]:
                    dp[i][j] = min(dp[i][j], dp[k][j + 1] + dp[i - k - 1][k])
    return dp[n][0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(10):  # Generate 10 random permutation polynomials per n
            permutation = list(range(n))
            random.shuffle(permutation)
            cycle_type = []
            i = 0
            while i < n:
                length = 1
                j = (i + 1) % n
                while permutation[j] != permutation[i]:
                    permutation[j], permutation[(j - 1) % n] = permutation[(j - 1) % n], permutation[j]
                    j = (j - 1) % n
                    length += 1
                cycle_type.append(length)
                i += length

            shape = cycle_type_to_shape(cycle_type)
            dim_specht = hook_length_formula(shape)

            abp_width = min(n, dim_specht)
            abp_size_value = abp_size(permutation, abp_width)

            if abp_size_value > dim_specht:
                conjecture_holds = False
                counterexample = f"n={n}, permutation={permutation}, dim(S^λ)={dim_specht}, ABP size={abp_size_value}"
                break

            total_metric_value += dim_specht
            instances_tested += 1

    return {
        "metric_name": "Specht Module Dimension",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {json.dumps(trial_result)}")
        results.append(trial_result)

    total_metric_value = sum(result["metric_value"] for result in results)
    instances_tested = sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```

--STDERR--
Traceback (most recent call last):
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_d1c11556.py", line 100, in <module>
    trial_result = run_trial(seed)
                   ^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_d1c11556.py", line 74, in run_trial
    dim_specht = hook_length_formula(shape)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_d1c11556.py", line 26, in hook_length_formula
    for col in range(len(shape[row])):
                     ^^^^^^^^^^^^^^^
TypeError: object of type 'int' has no len()

```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> The error indicates a metric definition bug: the code attempts to compute hook lengths on an integer 'shape' instead of a Young diagram list. This suggests the test fails to properly encode cycle types as partitions, making the Specht module dimension calculation invalid. The conjecture requires correct Young diagram representation, which is not achieved here.

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> The test crashed due to a type error in the hook length calculation, indicating the code failed to properly represent cycle types as Young diagrams. This invalidates the metric computation. | next: Fix the hook_length_formula to accept partition tuples instead of integers, then re-run tests with valid Young diagram inputs

## 11. Audit log (LLM calls)

_(no audit log file — pre-Fase-A cycle)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/b1f0fa3b27cf.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/b1f0fa3b27cf.tar.gz` (if generated)
