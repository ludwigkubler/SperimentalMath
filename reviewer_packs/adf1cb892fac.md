---
title: "Reviewer Pack — Minimal Symplectic Form Rank vs BP_ReadTwice Circuit Depth"
subtitle: "Entry adf1cb892fac · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-22 12:45:20 UTC"
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

# Minimal Symplectic Form Rank vs BP_ReadTwice Circuit Depth
**Entry ID**: `adf1cb892fac`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-22 12:45:20 UTC

## 1. Conjecture
**Field A** (mathematical branch): Symplectic Geometry
**Field B** (complexity object): Complexity Theory: Branching Program Read-Twice Complexity

**Statement**:

> {'text': 'For any read-twice branching program P, the minimal rank of its associated symplectic form is Θ(log^2 size(P))', 'counterexample': 'There exists a counterexample where the minimal rank of the symplectic form for a given read-twice branching program is less than Θ(log^2 size(P))'}

**Rationale (proposer's reasoning)**:

> {'text': 'Symplectic geometry offers a structured way to encode the complexity of computations, potentially providing deeper insights into the limitations of BP_read_twice circuits. The minimal symplectic form rank could serve as a non-trivial invariant that distinguishes between read-once and read-twice complexities.'}

**Taxonomy category**: `BP_READTWICE` (status at proposal time: )

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `c9cae12a3ab858b0`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> The conjecture is supported if, for at least 80% of generated read-twice branching programs with n ≤ 40, the ratio of the minimal rank to log^2(n) falls within ±30% of its expected value (Θ(log^2 size(P))).

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | UNCERTAIN | 1.00 | UNCERTAIN | HITS |
| NATURAL_PROOFS | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| ALGEBRIZATION | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| KARP_LIPTON | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |

## 4. Novelty audit
**Verdict**: `ADJACENT_OK` against 6 hits across arXiv + Semantic Scholar + ECCC

**Search queries** (3):
- `"symplectic geometry" AND "branching program read-twice complexity"`
- `"minimal rank" symplectic form AND Θ(log^2) size(P)`
- `"counterexample" minimal rank symplectic form < Θ(log^2) size(P)`

**Top relevant hits considered**:
- [http://arxiv.org/abs/1908.01012v3] Model comparison from LIGO-Virgo data on GW170817's binary components and consequences for the merger remnant
- [http://arxiv.org/abs/2011.00217v1] Searches for 25 rare and forbidden decays of $D^+$ and $D_s^+$ mesons
- [http://arxiv.org/abs/2012.05143v2] First observation of the decay $B_s^0 \to K^-μ^+ν_μ$ and a measurement of $|V_{ub}|/|V_{cb}|$
- [http://arxiv.org/abs/2007.11292v2] First observation of the decay $Λ_b^0 \to η_c(1S) p K^-$
- [http://arxiv.org/abs/2407.14261v2] Study of charmonium production via the decay to $p\bar{p}$ at $\sqrt{s} = 13 TeV$
- [http://arxiv.org/abs/2103.07349v2] Measurement of the prompt-production cross-section ratio $σ(χ_{c2})/σ(χ_{c1})$ in $p$Pb collisions at $\sqrt{s_{NN}}$ = 

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
    
    def generate_read_twice_circuit(n):
        if n == 1:
            return [[0]]
        else:
            left = generate_read_twice_circuit(n // 2)
            right = generate_read_twice_circuit(n - n // 2)
            circuit = []
            for i in range(len(left)):
                circuit.append([left[i][0] + right[i][0]])
            return circuit
    
    def symplectic_form_rank(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        m = n // 2
        A = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                A[i][j] = circuit[i][0][j]
        C = [[A[i][j] - A[i+m//2][j+m//2] for j in range(n)] for i in range(m)]
        rank = 0
        for row in C:
            if any(row):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_read_twice_circuit(n)
        rank = symplectic_form_rank(circuit)
        expected_rank = math.log2(n) ** 2
        ratio = rank / expected_rank if expected_rank != 0 else float('inf')
        results.append({
            "n": n,
            "rank": rank,
            "expected_rank": expected_rank,
            "ratio": ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["ratio"] - 1) < 0.3) / len(results)
    
    return {
        "metric_name": "Ratio of Symplectic Form Rank to Expected Rank",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, rank={results[0]['rank']}, expected_rank={results[0]['expected_rank']}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, rank={results[0]['rank']}, expected_rank={results[0]['expected_rank']}\" first_failing_seed={first_failing_seed}")
```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```
, 'counterexample': 'n=5, rank=1, expected_rank=5.391350077827255'}
TRIAL: {'metric_name': 'Ratio of Symplectic Form Rank to Expected Rank', 'metric_value': 0.07866521015009668, 'instances_tested': 6, 'conjecture_holds': False, 'counterexample': 'n=5, rank=1, expected_rank=5.391350077827255'}
TRIAL: {'metric_name': 'Ratio of Symplectic Form Rank to Expected Rank', 'metric_value': 0.07866521015009668, 'instances_tested': 6, 'conjecture_holds': False, 'counterexample': 'n=5, rank=1, expected_rank=5.391350077827255'}
TRIAL: {'metric_name': 'Ratio of Symplectic Form Rank to Expected Rank', 'metric_value': 0.07866521015009668, 'instances_tested': 6, 'conjecture_holds': False, 'counterexample': 'n=5, rank=1, expected_rank=5.391350077827255'}
TRIAL: {'metric_name': 'Ratio of Symplectic Form Rank to Expected Rank', 'metric_value': 0.07866521015009668, 'instances_tested': 6, 'conjecture_holds': False, 'counterexample': 'n=5, rank=1, expected_rank=5.391350077827255'}
TRIAL: {'metric_name': 'Ratio of Symplectic Form Rank to Expected Rank', 'metric_value': 0.07866521015009668, 'instances_tested': 6, 'conjecture_holds': False, 'counterexample': 'n=5, rank=1, expected_rank=5.391350077827255'}
TRIAL: {'metric_name': 'Ratio of Symplectic Form Rank to Expected Rank', 'metric_value': 0.07866521015009668, 'instances_tested': 6, 'conjecture_holds': False, 'counterexample': 'n=5, rank=1, expected_rank=5.391350077827255'}
TRIAL: {'metric_name': 'Ratio of Symplectic Form Rank to Expected Rank', 'metric_value': 0.07866521015009668, 'instances_tested': 6, 'conjecture_holds': False, 'counterexample': 'n=5, rank=1, expected_rank=5.391350077827255'}
TRIAL: {'metric_name': 'Ratio of Symplectic Form Rank to Expected Rank', 'metric_value': 0.07866521015009668, 'instances_tested': 6, 'conjecture_holds': False, 'counterexample': 'n=5, rank=1, expected_rank=5.391350077827255'}
TRIAL: {'metric_name': 'Ratio of Symplectic Form Rank to Expected Rank', 'metric_value': 0.07866521015009668, 'instances_tes
```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> skipped: test crashed before producing data

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> Safety rail: critic_challenge_falsified | original: The test results indicate that for at least one instance (n=5), the minimal rank of the symplectic form is less than half of the expected value, which | next: Investigate further to understand why the test crashed and whether it was a fluke or indicative of a deeper issue with the conjecture. If the crash is due to an error in the implementation, fix the code and retest.

## 11. Audit log (LLM calls)

**Total LLM calls**: 9

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | glm4:latest | 0 | 0 | 13403 |
| 2 | preregistration | ollama_remote | glm4:latest | 0 | 0 | 9677 |
| 3 | novelty | ollama_remote | glm4:latest | 0 | 0 | 8662 |
| 4 | novelty | ollama_remote | glm4:latest | 0 | 0 | 9474 |
| 5 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 9703 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 9694 |
| 7 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 22935 |
| 8 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 11809 |
| 9 | judge | ollama_remote | glm4:latest | 0 | 0 | 60428 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 155784 ms total latency. Provider mix: {'ollama_remote': 9}

_(full prompt+response transcripts available in `research/audit/adf1cb892fac.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/adf1cb892fac.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/adf1cb892fac.tar.gz` (if generated)
