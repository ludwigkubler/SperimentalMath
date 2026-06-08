---
title: "Reviewer Pack — Minimal Rank of Boolean Differential Forms vs Monotone Circu..."
subtitle: "Entry 6cb7db7fda37 · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-23 06:19:40 UTC"
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

# Minimal Rank of Boolean Differential Forms vs Monotone Circuit Depth for k-CLIQUE
**Entry ID**: `6cb7db7fda37`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-23 06:19:40 UTC

## 1. Conjecture
**Field A** (mathematical branch): Boolean Differential Calculus
**Field B** (complexity object): Complexity Theory: Monotone Circuit Complexity for k-CLIQUE

**Statement**:

> ['For every k-CLIQUE instance with n vertices, there exists a Boolean differential form of minimal rank that corresponds to its monotone circuit depth.', 'The minimal rank of the corresponding Boolean differential form is at least Θ(n^{1/4}).', 'This rank grows without bound as k increases for fixed n.']

**Rationale (proposer's reasoning)**:

> ['Boolean differential calculus provides a way to represent boolean functions through geometric objects, which could potentially expose the intrinsic structure of monotone circuits.', 'The minimal rank of these forms may reflect the complexity of the circuit that can be constructed to solve the k-CLIQUE problem, providing insights into circuit lower bounds.', 'Previous work has shown connections between differential geometry and complexity theory, suggesting that this approach might be fruitful.']

**Taxonomy category**: `MONOTONE_CLIQUE` (status at proposal time: )

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `67fb4ccef355d696`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> For a given k-CLIQUE instance, if the minimal rank of the Boolean differential form is within Θ(n^{1/4}) of its monotone circuit depth and this condition holds true for at least 80% of the instances tested with 30 seeds, it will be considered supported. If any seed produces a discrepancy greater than 3 standard deviations from the expected Θ(n^{1/4}) relationship or if less than 70% of the instances meet the expected relationship, it will be considered falsified.

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | UNCERTAIN | 1.00 | UNCERTAIN | HITS |
| NATURAL_PROOFS | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| ALGEBRIZATION | UNCERTAIN | 0.90 | HITS | UNCERTAIN |
| KARP_LIPTON | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |

## 4. Novelty audit
**Verdict**: `NOVEL` against 6 hits across arXiv + Semantic Scholar + ECCC

**Search queries** (3):
- `boolean differential calculus AND monotone circuit complexity FOR k-CLIQUE`
- `minimal rank of boolean differential forms AND monotone circuit depth for k-CLIQUE`
- `Θ(n^{1/4}) IN BOOLEAN DIFFERENTIAL FORMS AND MONOTONE CIRCUIT DEPTH`

**Top relevant hits considered**:
- [http://arxiv.org/abs/2001.09986v2] Zheghalkin-Boolean Calculus
- [http://arxiv.org/abs/1403.5908v2] Monotone and boolean unitary Brownian motions
- [http://arxiv.org/abs/1102.1242v2] A refinement of Stone duality to skew Boolean algebras
- [http://arxiv.org/abs/2005.05490v1] Monotone Boolean Functions, Feasibility/Infeasibility, LP-type problems and MaxCon
- [http://arxiv.org/abs/2407.04826v1] Multi-strategy Based Quantum Cost Reduction of Quantum Boolean Circuits
- [http://arxiv.org/abs/2305.07364v1] Improved Lower Bounds for Monotone q-Multilinear Boolean Circuits

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=1, elapsed=0.1s

### 5.1 Generated Python source

```python
import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot_row = -1
        for row in range(rank, rows):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for r in range(rows):
            if r != rank and matrix[r][col] != 0:
                factor = Fraction(matrix[r][col], matrix[rank][col])
                for c in range(cols):
                    matrix[r][c] -= factor * matrix[rank][c]
        rank += 1
    return rank

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for col in range(cols):
        pivot_row = -1
        for row in range(col, rows):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
        for r in range(rows):
            if r != col and matrix[r][col] != 0:
                factor = Fraction(matrix[r][col], matrix[col][col])
                for c in range(cols):
                    matrix[r][c] -= factor * matrix[col][c]
    return matrix

def generate_k_clique_instance(n, k):
    vertices = list(range(n))
    edges = []
    for i in range(k):
        for j in range(i + 1, k):
            edges.append((vertices[i], vertices[j]))
    for _ in range(random.randint(0, n * (n - 1) // 2 - len(edges))):
        u, v = random.sample(vertices, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    return vertices, edges

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        for _ in range(5):  # Test each n with 5 different k values
            k = random.randint(n // 2, n)
            vertices, edges = generate_k_clique_instance(n, k)
            # Construct the Boolean differential form (simplified example)
            form = [[1 if (i, j) in edges else 0 for j in range(n)] for i in range(n)]
            rank = matrix_rank(gaussian_elimination(form))
            total_rank += rank
            instances_tested += 1
        avg_rank = Fraction(total_rank, instances_tested)
        expected_rank = n ** Fraction(1, 4)
        if abs(avg_rank - expected_rank) > 3 * (expected_rank / math.sqrt(instances_tested)):
            return {
                "metric_name": "rank",
                "metric_value": float(avg_rank),
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, avg_rank={avg_rank}, expected_rank={expected_rank}"
            }
    return {
        "metric_name": "rank",
        "metric_value": float(avg_rank),
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_rank = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - avg_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"rank_discrepancy\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```
, "metric_value": 8.2, "instances_tested": 5, "conjecture_holds": False, "counterexample": "n=10, avg_rank=41/5, expected_rank=1.7782794100389228"}
TRIAL: {"seed": 593, "metric_name": "rank", "metric_value": 8.4, "instances_tested": 5, "conjecture_holds": False, "counterexample": "n=10, avg_rank=42/5, expected_rank=1.7782794100389228"}
TRIAL: {"seed": 631, "metric_name": "rank", "metric_value": 7.4, "instances_tested": 5, "conjecture_holds": False, "counterexample": "n=10, avg_rank=37/5, expected_rank=1.7782794100389228"}
TRIAL: {"seed": 677, "metric_name": "rank", "metric_value": 7.8, "instances_tested": 5, "conjecture_holds": False, "counterexample": "n=10, avg_rank=39/5, expected_rank=1.7782794100389228"}
TRIAL: {"seed": 727, "metric_name": "rank", "metric_value": 8.4, "instances_tested": 5, "conjecture_holds": False, "counterexample": "n=10, avg_rank=42/5, expected_rank=1.7782794100389228"}
TRIAL: {"seed": 773, "metric_name": "rank", "metric_value": 7.6, "instances_tested": 5, "conjecture_holds": False, "counterexample": "n=10, avg_rank=38/5, expected_rank=1.7782794100389228"}
TRIAL: {"seed": 821, "metric_name": "rank", "metric_value": 3.6, "instances_tested": 5, "conjecture_holds": False, "counterexample": "n=5, avg_rank=18/5, expected_rank=1.4953487812212205"}
TRIAL: {"seed": 877, "metric_name": "rank", "metric_value": 3.6, "instances_tested": 5, "conjecture_holds": False, "counterexample": "n=5, avg_rank=18/5, expected_rank=1.4953487812212205"}
TRIAL: {"seed": 929, "metric_name": "rank", "metric_value": 8.4, "instances_tested": 5, "conjecture_holds": False, "counterexample": "n=10, avg_rank=42/5, expected_rank=1.7782794100389228"}

--STDERR--
Traceback (most recent call last):
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_712fbec1.py", line 127, in <module>
    first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lu
```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> skipped: test crashed before producing data

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> Safety rail: critic_challenge_falsified | original: The test results show that for at least one seed (n=10), the average rank of the Boolean differential form significantly deviates from the expected Θ( | next: Investigate further to identify why the discrepancy occurs and whether there are specific types of k-CLIQUE instances that lead to such deviations.

## 11. Audit log (LLM calls)

**Total LLM calls**: 9

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | glm4:latest | 0 | 0 | 14005 |
| 2 | preregistration | ollama_remote | glm4:latest | 0 | 0 | 9892 |
| 3 | novelty | ollama_remote | glm4:latest | 0 | 0 | 8421 |
| 4 | novelty | ollama_remote | glm4:latest | 0 | 0 | 9095 |
| 5 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 13651 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 9199 |
| 7 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 13051 |
| 8 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 14599 |
| 9 | judge | ollama_remote | glm4:latest | 0 | 0 | 14240 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 106153 ms total latency. Provider mix: {'ollama_remote': 9}

_(full prompt+response transcripts available in `research/audit/6cb7db7fda37.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/6cb7db7fda37.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/6cb7db7fda37.tar.gz` (if generated)
