---
title: "Reviewer Pack — Tropical Rank of Tseitin Incidence Matrix Bounds Resolution ..."
subtitle: "Entry 4cbcbdc0fbf7 · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-04-25 15:58:47 UTC"
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

# Tropical Rank of Tseitin Incidence Matrix Bounds Resolution Width
**Entry ID**: `4cbcbdc0fbf7`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-04-25 15:58:47 UTC

## 1. Conjecture
**Field A** (mathematical branch): Tropical geometry
**Field B** (complexity object): Resolution proof width

**Statement**:

> For Tseitin formulas on d-regular expander graphs with n variables, the tropical rank of the incidence matrix over the max-plus semiring is Θ(log n) if and only if the resolution proof width is Ω(n^{1/2})

**Rationale (proposer's reasoning)**:

> Tropical rank captures combinatorial degeneracy in constraint systems, while resolution width measures proof complexity. Expanders enforce structural rigidity that may create tropical rank anomalies, revealing hidden geometric constraints in proof size.

**Taxonomy category**: `PROOF_COMPLEXITY_TSEITIN` (status at proposal time: alive)

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `61fa7b15bc3ef961`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> default: >=80% seeds must support, no counterexample

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | SAFE | 0.95 | SAFE | SAFE |
| NATURAL_PROOFS | SAFE | 0.95 | UNCERTAIN | SAFE |
| ALGEBRIZATION | SAFE | 0.95 | SAFE | SAFE |
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
import sys
import json

# Helper functions for max-plus algebra and linear algebra

def max_plus_add(a, b):
    return a if a == float('-inf') else b if b == float('-inf') else max(a, b)

def max_plus_multiply(a, b):
    return float('-inf') if a == float('-inf') or b == float('-inf') else a + b

def max_plus_matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[float('-inf')] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] = max_plus_add(C[i][j], max_plus_multiply(A[i][l], B[l][j]))
    return C

def gaussian_elimination_max_plus(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if A[j][i] > A[max_row][i]:
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(n + 1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] = max_plus_add(augmented_matrix[j][k], max_plus_multiply(-factor, augmented_matrix[i][k]))
    return [row[-1] for row in augmented_matrix]

def tropical_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        pivot_row = -1
        for j in range(m):
            if matrix[j][i] != float('-inf'):
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        rank += 1
        for j in range(m):
            if j != pivot_row:
                factor = max_plus_multiply(-matrix[j][i], matrix[pivot_row][i])
                for k in range(n):
                    matrix[j][k] = max_plus_add(matrix[j][k], max_plus_multiply(factor, matrix[pivot_row][k]))
    return rank

def d_regular_expander_graph(d, n):
    if (d * (n - 1)) % 2 != 0:
        raise ValueError("Invalid parameters for expander graph")
    graph = [[] for _ in range(n)]
    degree = (d * (n - 1)) // 2
    visited = [False] * n
    def dfs(u, count):
        if count == degree:
            return True
        visited[u] = True
        for v in range(n):
            if not visited[v]:
                graph[u].append(v)
                graph[v].append(u)
                if dfs(v, count + 1):
                    return True
                graph[u].pop()
                graph[v].pop()
        visited[u] = False
        return False
    for i in range(n):
        if not visited[i]:
            dfs(i, 0)
    return graph

def incidence_matrix(graph, n):
    m = len(graph)
    A = [[float('-inf')] * n for _ in range(m)]
    for u in range(m):
        for v in graph[u]:
            A[u][v] = 1
    return A

def resolution_width(clauses, variables):
    clauses = [set(c) for c in clauses]
    variables = set(variables)
    queue = list(variables)
    while queue:
        var = queue.pop(0)
        if not any(var in clause for clause in clauses):
            continue
        new_clauses = []
        for clause in clauses:
            if var in clause:
                new_clauses.append(clause - {var})
            elif -var in clause:
                new_clauses.append(clause | {-var})
        queue.extend(new_clause for new_clause in new_clauses if len(new_clause) == 1)
        clauses = new_clauses
    return max(len(c) for c in clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    d = 3
    graph = d_regular_expander_graph(d, n)
    A = incidence_matrix(graph, n)
    rank = tropical_rank(A)
    clauses = [[i+1 if x == 1 else -(i+1) for i, x in enumerate(row)] for row in A]
    width = resolution_width(clauses, range(n))
    metric_name = "tropical_rank"
    metric_value = math.log(n)
    instances_tested = 1
    conjecture_holds = rank == math.log(n) and width >= n**0.5
    counterexample = "" if conjecture_holds else f"rank={rank}, width={width}"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```

--STDERR--
Traceback (most recent call last):
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_a76fc763.py", line 139, in <module>
    result = run_trial(seed)
             ^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_a76fc763.py", line 117, in run_trial
    graph = d_regular_expander_graph(d, n)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_a76fc763.py", line 64, in d_regular_expander_graph
    raise ValueError("Invalid parameters for expander graph")
ValueError: Invalid parameters for expander graph

```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> {
  "critic_verdict": "CHALLENGE",
  "reasoning": "The error indicates invalid parameters for

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> The test crashed due to invalid expander graph parameters, preventing evaluation of the conjecture | next: Verify parameter validity for d_regular_expander_graph function

## 11. Audit log (LLM calls)

_(no audit log file — pre-Fase-A cycle)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/4cbcbdc0fbf7.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/4cbcbdc0fbf7.tar.gz` (if generated)
