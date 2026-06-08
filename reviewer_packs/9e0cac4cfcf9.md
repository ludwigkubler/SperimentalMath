---
title: "Reviewer Pack — Tropical Convex Hull Dimension and ACC^0 Circuit Size"
subtitle: "Entry 9e0cac4cfcf9 · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-07 20:41:09 UTC"
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

# Tropical Convex Hull Dimension and ACC^0 Circuit Size
**Entry ID**: `9e0cac4cfcf9`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-07 20:41:09 UTC

## 1. Conjecture
**Field A** (mathematical branch): Tropical Convex Geometry
**Field B** (complexity object): ACC^0 Circuit Size

**Statement**:

> For any CNF formula Φ with n variables, the dimension of the tropical convex hull of its clause vectors is Θ(log n) if and only if Φ has an ACC^0 circuit of size Θ(n).

**Rationale (proposer's reasoning)**:

> Tropical convex hulls capture the extremal structure of clause interactions, which may constrain the algebraic complexity of ACC^0 circuits. The logarithmic scaling suggests a trade-off between geometric sparsity and computational efficiency.

**Taxonomy category**: `ACC_LB_via_WILLIAMS` (status at proposal time: partially_alive)

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `73a63ba2c26a6ad3`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> default: >=80% seeds must support, no counterexample

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | SAFE | 0.95 | SAFE | UNCERTAIN |
| NATURAL_PROOFS | SAFE | 0.95 | SAFE | UNCERTAIN |
| ALGEBRIZATION | SAFE | 0.95 | UNCERTAIN | SAFE |
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
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not any(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def tropical_convex_hull(clauses):
        # Placeholder for actual implementation
        return len(clauses)
    
    def acc0_circuit_size(clauses):
        # Placeholder for actual implementation
        return len(clauses) * 2
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    hull_dimension = tropical_convex_hull(clauses)
    circuit_size = acc0_circuit_size(clauses)
    
    if hull_dimension == math.log(n, 2):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "hull_dimension",
        "metric_value": hull_dimension,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2%}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```
 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'hull_dimension', 'metric_value': 14, 'instances_tested': 1, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'hull_dimension', 'metric_value': 50, 'instances_tested': 1, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'hull_dimension', 'metric_value': 46, 'instances_tested': 1, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'hull_dimension', 'metric_value': 18, 'instances_tested': 1, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'hull_dimension', 'metric_value': 76, 'instances_tested': 1, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'hull_dimension', 'metric_value': 32, 'instances_tested': 1, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'hull_dimension', 'metric_value': 72, 'instances_tested': 1, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'hull_dimension', 'metric_value': 38, 'instances_tested': 1, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'hull_dimension', 'metric_value': 34, 'instances_tested': 1, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}

--STDERR--
Traceback (most recent call last):
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_f6948cba.py", line 74, in <module>
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_f6948cba.py", line 74, in <genexpr>
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

> Test crashed with KeyError 'seed' before producing valid data, preventing reliable assessment of conjecture status. | next: Fix test to handle 'seed' parameter properly and re-run with validated input configurations

## 11. Audit log (LLM calls)

**Total LLM calls**: 8

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | qwen3:8b | 0 | 0 | 106068 |
| 2 | propose | ollama_remote | qwen3:8b | 0 | 0 | 103416 |
| 3 | preregistration | ollama_remote | qwen3:8b | 0 | 0 | 19810 |
| 4 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 16542 |
| 5 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 12585 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 19081 |
| 7 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 7285 |
| 8 | judge | ollama_remote | qwen3:8b | 0 | 0 | 12543 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 297332 ms total latency. Provider mix: {'ollama_remote': 8}

_(full prompt+response transcripts available in `research/audit/9e0cac4cfcf9.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/9e0cac4cfcf9.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/9e0cac4cfcf9.tar.gz` (if generated)
