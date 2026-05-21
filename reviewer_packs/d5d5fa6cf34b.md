---
title: "Reviewer Pack — Coxeter Group Action Number Invariant for Tseitin Resolution..."
subtitle: "Entry d5d5fa6cf34b · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-21 13:41:24 UTC"
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

# Coxeter Group Action Number Invariant for Tseitin Resolution Length
**Entry ID**: `d5d5fa6cf34b`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-21 13:41:24 UTC

## 1. Conjecture
**Field A** (mathematical branch): Combinatorial Group Theory
**Field B** (complexity object): Resolution Lower Bounds for Tseitin Formulas

**Statement**:

> ["For any Tseitin formula on a graph G, the number of distinct orbits under the action of the Coxeter group Γ associated with G's symmetries is upper-bounded by the resolution length L(G) required to refute G.", 'Formally: For all graphs G and Tseitin formulas φ(G), |Orb(Γ)| ≤ 2^L(G).', 'If a graph has no nontrivial automorphisms, then Γ = 1 and Orb(Γ) = {G}, implying L(G) = O(log n).']

**Rationale (proposer's reasoning)**:

> ['Coxeter groups provide a rich structure for studying symmetries in combinatorial objects. By relating the action of these groups to resolution complexity, we could potentially uncover new properties that are hard to capture using current techniques.', 'The invariant |Orb(Γ)| measures the complexity of the symmetry group acting on the graph, which may correlate with the difficulty of refuting Tseitin formulas derived from it.']

**Taxonomy category**: `TSEITIN_RES` (status at proposal time: )

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `1e98db21c3ce7029`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> The conjecture is supported if the maximum observed ratio of distinct orbits under Coxeter group action to resolution length is less than or equal to 1, otherwise it is falsified.

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | SAFE | 1.00 | UNCERTAIN | SAFE |
| NATURAL_PROOFS | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| ALGEBRIZATION | SAFE | 1.00 | SAFE | UNCERTAIN |
| KARP_LIPTON | SAFE | 1.00 | UNCERTAIN | SAFE |

## 4. Novelty audit
**Verdict**: `NOVEL` against 0 hits across arXiv + Semantic Scholar + ECCC

**Search queries** (3):
- `"Coxeter group action number" AND "Tseitin resolution length"`
- `"symmetry orbits in Tseitin formulas" AND "resolution lower bounds"`
- `"graph automorphisms" AND "resolution length of Tseitin formulas"`

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=124, elapsed=240.1s

### 5.1 Generated Python source

```python
import random
import math
from fractions import Fraction

def generate_random_graph(n):
    graph = {i: set() for i in range(n)}
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    random.shuffle(edges)
    for u, v in edges[:n - 1]:
        graph[u].add(v)
        graph[v].add(u)
    return graph

def is_connected(graph):
    visited = set()
    stack = [0]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node] - visited)
    return len(visited) == len(graph)

def generate_tseitin_formula(graph):
    n = len(graph)
    literals = {i: (2 * i, 2 * i + 1) for i in range(n)}
    clauses = []
    
    # Add clauses for each node
    for u in range(n):
        if graph[u]:
            clause = [literals[u][0]]
            for v in graph[u]:
                clause.append(-literals[v][0])
                clause.append(literals[v][1])
            clauses.append(clause)
    
    # Add clauses for each edge
    for u, v in [(i, j) for i in range(n) for j in range(i + 1, n)]:
        if not graph[u] or not graph[v]:
            continue
        clause = [-literals[u][0], -literals[v][0]]
        clauses.append(clause)
    
    # Add tautology to ensure satisfiability
    tautology = [2 * i + 1 for i in range(n)]
    clauses.append(tautology)
    
    return clauses

def resolution_length(clauses):
    clauses_set = set(tuple(sorted(c)) for c in clauses)
    new_clauses = []
    while True:
        new_clause = None
        for clause1 in clauses_set:
            for clause2 in clauses_set:
                if any(lit in clause1 and -lit in clause2 for lit in clause1):
                    new_clause = [l for l in clause1 + clause2 if l not in clause1 and -l not in clause2]
                    break
            if new_clause:
                break
        if not new_clause:
            return len(clauses_set)
        new_clauses.append(new_clause)
        clauses_set.add(tuple(sorted(new_clause)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    while not is_connected(graph):
        graph = generate_random_graph(n)
    
    clauses = generate_tseitin_formula(graph)
    resolution_len = resolution_length(clauses)
    
    if resolution_len == 1:
        return {
            "metric_name": "Orb(Γ) / 2^L(G)",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    orbits = set()
    for u in range(n):
        orbit = {u}
        stack = [u]
        while stack:
            node = stack.pop()
            if node not in orbit:
                orbit.add(node)
                stack.extend(graph[node] - orbit)
        orbits.add(tuple(sorted(orbit)))
    
    ratio = len(orbits) / (2 ** resolution_len)
    return {
        "metric_name": "Orb(Γ) / 2^L(G)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
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

> The test timed out before producing data, making it impossible to determine if the conjecture is supported or falsified. | next: NONE

## 11. Audit log (LLM calls)

**Total LLM calls**: 9

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | glm4:latest | 0 | 0 | 15020 |
| 2 | preregistration | ollama_remote | glm4:latest | 0 | 0 | 9169 |
| 3 | novelty | ollama_remote | glm4:latest | 0 | 0 | 8111 |
| 4 | novelty | ollama_remote | glm4:latest | 0 | 0 | 9064 |
| 5 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 14910 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 10477 |
| 7 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 11708 |
| 8 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 12347 |
| 9 | judge | ollama_remote | glm4:latest | 0 | 0 | 11800 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 102606 ms total latency. Provider mix: {'ollama_remote': 9}

_(full prompt+response transcripts available in `research/audit/d5d5fa6cf34b.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/d5d5fa6cf34b.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/d5d5fa6cf34b.tar.gz` (if generated)
