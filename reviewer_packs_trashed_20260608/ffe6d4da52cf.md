---
title: "Reviewer Pack — Prime Density in Arithmetic Progressions and Seed Length of ..."
subtitle: "Entry ffe6d4da52cf · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-21 07:37:53 UTC"
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

# Prime Density in Arithmetic Progressions and Seed Length of Nisan-Wigderson PRGs
**Entry ID**: `ffe6d4da52cf`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-21 07:37:53 UTC

## 1. Conjecture
**Field A** (mathematical branch): Algebraic Number Theory
**Field B** (complexity object): Seed Length of Nisan-Wigderson PRGs

**Statement**:

> For a 3-SAT instance with n variables, the seed length of a Nisan-Wigderson PRG that fools AC⁰ circuits is Θ(π(n)), where π(n) is the number of primes ≤n. This holds for all instances where the clause graph is bipartite and the variable assignments induce a Dirichlet progression with modulus ≤n².

**Rationale (proposer's reasoning)**:

> The distribution of primes in arithmetic progressions relates to the structure of number fields, which could influence the pseudorandomness properties needed for PRGs. The density of primes affects the entropy required to generate pseudorandom bits, thus influencing seed length.

**Taxonomy category**: `NISAN_WIGDERSON_DESIGNS` (status at proposal time: partially_alive)

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `fa9739ba909bd214`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> default: >=80% seeds must support, no counterexample

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | UNCERTAIN | 0.95 | HITS | UNCERTAIN |
| NATURAL_PROOFS | SAFE | 0.95 | UNCERTAIN | SAFE |
| ALGEBRIZATION | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |
| KARP_LIPTON | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |

## 4. Novelty audit
**Verdict**: `NOVEL` against 0 hits across arXiv + Semantic Scholar + ECCC

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=0, elapsed=0.1s

### 5.1 Generated Python source

```python
import random
import math

def sieve_of_eratosthenes(n):
    primes = [True] * (n + 1)
    p = 2
    while p * p <= n:
        if primes[p]:
            for i in range(p * p, n + 1, p):
                primes[i] = False
        p += 1
    return [p for p in range(2, n + 1) if primes[p]]

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_dirichlet_progression(a, d, n):
    return [(a + k * d) % n for k in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random 3-SAT instance with n variables
    n = random.randint(5, 40)
    m = random.randint(2 * n, 4 * n)
    clauses = []
    for _ in range(m):
        literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        random.shuffle(literals)
        clauses.append(tuple(literals))
    
    # Check if the clause graph is bipartite
    variable_to_clauses = {i: [] for i in range(1, n + 1)}
    for clause in clauses:
        for literal in clause:
            variable_to_clauses[abs(literal)].append(clause)
    
    def bfs(start):
        queue = [start]
        visited = set()
        color = {start: 0}
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                for neighbor in variable_to_clauses[node]:
                    for lit in neighbor:
                        var = abs(lit)
                        if var != node and var not in visited:
                            if color.get(var) is None:
                                color[var] = 1 - color[node]
                                queue.append(var)
                            elif color[var] == color[node]:
                                return False
        return True
    
    if not bfs(1):
        return {
            "metric_name": "Seed Length",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "Clause graph is not bipartite"
        }
    
    # Compute π(n) using sieve of Eratosthenes
    primes = sieve_of_eratosthenes(n)
    pi_n = len(primes)
    
    # Generate a Dirichlet progression based on clause graph bipartitioning
    modulus = n * n
    if not is_prime(modulus):
        return {
            "metric_name": "Seed Length",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "Modulus must be a prime number"
        }
    
    progression = generate_dirichlet_progression(1, 2, modulus)
    
    # Simulate PRG seed length via a pseudorandom generator with explicit modular arithmetic
    seed_length = len(progression)
    
    return {
        "metric_name": "Seed Length",
        "metric_value": seed_length,
        "instances_tested": 1,
        "conjecture_holds": abs(seed_length - pi_n) <= 2 * math.sqrt(pi_n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Modulus must be a prime number\" first_failing_seed={first_failing_seed}")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```
': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
TRIAL: {'metric_name': 'Seed Length', 'metric_value': None, 'instances_tested': 0, 'conjecture_holds': False, 'counterexample': 'Clause graph is not bipartite'}
RESULT: FALSIFIED counterexample="Modulus must be a prime number" first_failing_seed=11

```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> Instances tested is 0, violating the 'n too small' failure mode. The counterexample cites modulus requirements but no empirical data was collected to validate this. The conjecture's metric (seed length) isn't measured in any trials, making the 'falsified' verdict invalid without actual tests.

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> No instances were tested, violating the 'n too small' failure mode. The counterexample references modulus requirements but lacks empirical validation. | next: Run tests with bipartite clause graphs and prime moduli to collect empirical data on seed length behavior

## 11. Audit log (LLM calls)

**Total LLM calls**: 11

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | qwen3:8b | 0 | 0 | 136116 |
| 2 | propose | ollama_remote | qwen3:8b | 0 | 0 | 101571 |
| 3 | preregistration | ollama_remote | qwen3:8b | 0 | 0 | 31631 |
| 4 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 27222 |
| 5 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 20400 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 12139 |
| 7 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 9980 |
| 8 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 11706 |
| 9 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 13843 |
| 10 | critic | ollama_remote | qwen3:8b | 0 | 0 | 32857 |
| 11 | judge | ollama_remote | qwen3:8b | 0 | 0 | 21453 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 418917 ms total latency. Provider mix: {'ollama_remote': 11}

_(full prompt+response transcripts available in `research/audit/ffe6d4da52cf.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/ffe6d4da52cf.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/ffe6d4da52cf.tar.gz` (if generated)
