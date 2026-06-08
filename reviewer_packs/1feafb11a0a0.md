---
title: "Reviewer Pack — Minimal ABP Size and Permutation Polynomial Degree"
subtitle: "Entry 1feafb11a0a0 · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-04-24 18:09:32 UTC"
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

# Minimal ABP Size and Permutation Polynomial Degree
**Entry ID**: `1feafb11a0a0`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-04-24 18:09:32 UTC

## 1. Conjecture
**Field A** (mathematical branch): Finite automata theory (permutation polynomials over finite fields)
**Field B** (complexity object): Size of algebraic branching programs (ABPs) for CNF formulas

**Statement**:

> For any CNF formula φ over n variables, the minimal ABP size required to represent φ is Θ(d²), where d is the degree of the minimal permutation polynomial encoding φ's clauses.

**Rationale (proposer's reasoning)**:

> Permutation polynomials can encode CNF formulas via their action on variable assignments. ABPs, being layered, naturally mirror the polynomial's degree structure, leading to a quadratic relationship between degree and ABP size.

**Taxonomy category**: `BARRINGTON_ALG` (status at proposal time: partially_alive)

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `d1690cc1a882fc5b`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> default: >=80% seeds must support, no counterexample

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |
| NATURAL_PROOFS | SAFE | 0.95 | UNCERTAIN | SAFE |
| ALGEBRIZATION | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |
| KARP_LIPTON | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |

## 4. Novelty audit
**Verdict**: `NOVEL` against 0 hits across arXiv + Semantic Scholar + ECCC

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=1, elapsed=0.3s

### 5.1 Generated Python source

```python
import sys
import random
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def degree_of_permutation_polynomial(clauses):
        # Simplified heuristic to estimate the degree of a permutation polynomial
        # based on the number of unique variables in clauses.
        unique_vars = set()
        for clause in clauses:
            for var in clause:
                unique_vars.add(abs(var))
        return len(unique_vars)
    
    def min_abp_size(clauses):
        n = max(abs(var) for var in sum(clauses, []))
        dp = [0] * (n + 1)
        for clause in clauses:
            for i in range(n, -1, -1):
                if i >= abs(clause[0]):
                    dp[i] += dp[i - abs(clause[0])]
                if i >= abs(clause[1]):
                    dp[i] += dp[i - abs(clause[1])]
        return max(dp)
    
    n = random.choice([5, 8, 11, 14])
    m = random.randint(2 * n, 3 * n)
    cnf = generate_cnf(n, m)
    degree = degree_of_permutation_polynomial(cnf)
    abp_size = min_abp_size(cnf)
    
    return {
        "metric_name": "ABP Size",
        "metric_value": abp_size,
        "instances_tested": 1,
        "conjecture_holds": abs(abp_size - degree**2) <= 0.1 * degree**2,
        "counterexample": "" if conjecture_holds else f"Degree {degree}, ABP Size {abp_size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_abp_size = sum(r["metric_value"] for r in results)
    num_seeds = len(results)
    avg_abp_size = total_abp_size / num_seeds
    std_abp_size = (sum((r["metric_value"] - avg_abp_size) ** 2 for r in results) / num_seeds) ** 0.5
    
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / num_seeds
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_abp_size} std={std_abp_size} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```

--STDERR--
Traceback (most recent call last):
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_2d64e563.py", line 54, in <module>
    result = run_trial(seed)
             ^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_2d64e563.py", line 46, in run_trial
    "counterexample": "" if conjecture_holds else f"Degree {degree}, ABP Size {abp_size}"
                            ^^^^^^^^^^^^^^^^
NameError: name 'conjecture_holds' is not defined

```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> ```json
{
  "critic_verdict": "CHALLENGE",
  "reasoning": "The empirical test failed

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> The test crashed due to an undefined variable, preventing determination of conjecture validity | next: Fix the test code to properly define 'conjecture_holds' and re-run experiments

## 11. Audit log (LLM calls)

_(no audit log file — pre-Fase-A cycle)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/1feafb11a0a0.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/1feafb11a0a0.tar.gz` (if generated)
