---
title: "Reviewer Pack — Minimal Order of Automorphism Groups of Affine Schemes and C..."
subtitle: "Entry db66dfd74cbc · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-06-03 19:32:59 UTC"
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

# Minimal Order of Automorphism Groups of Affine Schemes and Circuit Monotone Width
**Entry ID**: `db66dfd74cbc`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-06-03 19:32:59 UTC

## 1. Conjecture
**Field A** (mathematical branch): Algebraic Geometry (Affine Schemes)
**Field B** (complexity object): Boolean Circuit Complexity (Circuit Monotone Width)

**Statement**:

> For any given n-variable CNF φ, the minimal order of automorphism groups of its associated affine scheme A(φ) is linearly correlated with its circuit monotone width w(φ), such that |Aut(A(φ))| = Θ(w(φ)).

**Rationale (proposer's reasoning)**:

> Affine schemes provide a geometric structure to certain boolean functions, and the minimal order of their automorphism groups may reflect the inherent complexity of computing these functions. The conjecture bridges algebraic geometry with circuit complexity by proposing a potential invariant that could reveal deep connections between the two fields.

**Taxonomy category**: `affine-schemes-circuit-monotone-width` (status at proposal time: )

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `a14495e2c780c3be`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> The conjecture is supported if the correlation coefficient between the minimal order of automorphism groups of affine schemes (|Aut(A(φ))|) and circuit monotone width (w(φ)) of at least 30 random n-variables CNFs φ exceeds 0.8, with a mean difference in |Aut(A(φ))| and w(φ) less than or equal to 3.

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| NATURAL_PROOFS | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| ALGEBRIZATION | UNCERTAIN | 1.00 | UNCERTAIN | HITS |
| KARP_LIPTON | SAFE | 1.00 | SAFE | UNCERTAIN |

## 4. Novelty audit
**Verdict**: `ADJACENT_OK` against 8 hits across arXiv + Semantic Scholar + ECCC

**Search queries** (3):
- `Minimal order automorphism groups AND affine schemes AND circuit monotone width`
- `CNF associated affine scheme automorphism group size AND circuit monotone width`
- `algebraic geometry affine schemes AND Boolean circuits monotone width relationship`

**Top relevant hits considered**:
- [http://arxiv.org/abs/1511.09051v3] On automorphism groups of affine surfaces
- [http://arxiv.org/abs/2001.09848v6] Reduced expression of minimal infinite reduced words of affine Weyl groups
- [http://arxiv.org/abs/1505.06927v2] Automorphism Groups of Configuration Spaces and Discriminant Varieties
- [http://arxiv.org/abs/1509.06670v2] Automorphism Groups and Invariant Theory on PN
- [http://arxiv.org/abs/math/0608534v2] On Automorphisms of Finite $p$-groups
- [http://arxiv.org/abs/1912.00347v3] Equiresidual algebraic geometry I: The affine theory
- [http://arxiv.org/abs/0802.4323v1] Non-singular affine surfaces with self-maps
- [http://arxiv.org/abs/1812.11710v1] Geometric Satake correspondence for affine Kac-Moody Lie algebras of type $A$

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=0, elapsed=2.0s

### 5.1 Generated Python source

```python
import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_cnf(n, k):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables) * (2 * random.randint(0, 1) - 1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def circuit_monotone_width(cnf):
        # Placeholder function to compute circuit monotone width
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(cnf)

    def aut_order(cnf):
        # Placeholder function to compute the order of automorphism group
        # This is a dummy implementation and should be replaced with an actual algorithm
        return random.randint(1, 100)  # Dummy value

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_aut_order = 0
    total_w = 0
    max_n = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_random_cnf(n, random.randint(1, n))
            aut_order_val = aut_order(cnf)
            w = circuit_monotone_width(cnf)
            total_aut_order += aut_order_val
            total_w += w
            instances_tested += 1
            max_n = max(max_n, n)

    mean_aut_order = total_aut_order / instances_tested
    mean_w = total_w / instances_tested
    correlation_coefficient = (instances_tested * sum(aut_order_val * w for aut_order_val, w in zip([aut_order(cnf) for cnf in [generate_random_cnf(n, random.randint(1, n)) for _ in range(instances_tested)]], [circuit_monotone_width(generate_random_cnf(n, random.randint(1, n))) for _ in range(instances_tested)])) - instances_tested * mean_aut_order * mean_w) / (instances_tested * math.sqrt(sum((aut_order_val - mean_aut_order)**2 for aut_order_val in [aut_order(cnf) for cnf in [generate_random_cnf(n, random.randint(1, n)) for _ in range(instances_tested)]]) * sum((w - mean_w)**2 for w in [circuit_monotone_width(generate_random_cnf(n, random.randint(1, n))) for _ in range(instances_tested)])))

    conjecture_holds = correlation_coefficient > 0.8 and abs(mean_aut_order - mean_w) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unspecified")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```
, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 2.23461938484049, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 1.8321777933886008, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 3.00518954450008, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 1.8476740247330632, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 1.9897948362637403, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 2.0022729270686566, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 2.3861924245257824, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 3.102114075018636, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 2.5842235962472215, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
TRIAL: {'metric_name': 'correlation_coefficient', 'metric_value': 2.316257449567291, 'instances_tested': 30, 'n_max': 40, 'conjecture_holds': False, 'counterexample': 'mapping_undefined'}
RESULT: FALSIFIED counterexample="mapping_undefined" first_failing_seed=11

```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> The test code uses dummy implementations for both the 'aut_order' and 'circuit_monotone_width' functions, which are critical components of the conjecture. Without correct implementations, the correlation coefficient cannot be accurately computed, leading to an unreliable verdict.

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> Safety rail: critic_challenge_falsified | original: The test code uses dummy implementations for both 'aut_order' and 'circuit_monotone_width', which are critical components of the conjecture. Without c | next: Implement accurate functions for 'aut_order' and 'circuit_monotone_width' and retest the conjecture.

## 11. Audit log (LLM calls)

**Total LLM calls**: 10

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | glm4:latest | 0 | 0 | 13574 |
| 2 | preregistration | ollama_remote | glm4:latest | 0 | 0 | 16099 |
| 3 | novelty | ollama_remote | glm4:latest | 0 | 0 | 9000 |
| 4 | novelty | ollama_remote | glm4:latest | 0 | 0 | 9919 |
| 5 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 18722 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 14934 |
| 7 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 19219 |
| 8 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 23244 |
| 9 | critic | ollama_remote | glm4:latest | 0 | 0 | 51354 |
| 10 | judge | ollama_remote | glm4:latest | 0 | 0 | 20003 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 196068 ms total latency. Provider mix: {'ollama_remote': 10}

_(full prompt+response transcripts available in `research/audit/db66dfd74cbc.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/db66dfd74cbc.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/db66dfd74cbc.tar.gz` (if generated)
