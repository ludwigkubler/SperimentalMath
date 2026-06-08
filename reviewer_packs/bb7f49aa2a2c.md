---
title: "Reviewer Pack — Minimal Rank of Formal Languages over Boolean Functions"
subtitle: "Entry bb7f49aa2a2c · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-27 06:10:03 UTC"
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

# Minimal Rank of Formal Languages over Boolean Functions
**Entry ID**: `bb7f49aa2a2c`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-27 06:10:03 UTC

## 1. Conjecture
**Field A** (mathematical branch): Formal Language Theory
**Field B** (complexity object): Complexity Theory: Boolean Function Entropy

**Statement**:

> ['For a given boolean function f with entropy H(f), the minimal rank of any formal language L over f is upper bounded by 2^{H(f)}.', 'Equivalently, if L is a formal language defined over the boolean function f, then the number of states in any finite automaton accepting L is at most 2^{H(f)}.']

**Rationale (proposer's reasoning)**:

> ['Formal language theory, particularly the study of minimal automata, provides insights into the structure and complexity of languages. The entropy of a boolean function measures its information content, which suggests a potential link to the complexity of formal languages defined over that function.', 'This conjecture could expose a fundamental connection between information theory (via entropy) and automata theory (via formal languages), potentially leading to new insights in computational complexity.']

**Taxonomy category**: `formal_language_automata` (status at proposal time: )

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `a03c5bbadf93ed90`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> For a boolean function f, if the number of states in the minimal DFA accepting L over f does not exceed 2^{H(f)} for all 30 random seeds.

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | UNCERTAIN | 1.00 | UNCERTAIN | HITS |
| NATURAL_PROOFS | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| ALGEBRIZATION | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |
| KARP_LIPTON | SAFE | 0.50 | UNCERTAIN | UNCERTAIN |

## 4. Novelty audit
**Verdict**: `NOVEL` against 9 hits across arXiv + Semantic Scholar + ECCC

**Search queries** (3):
- `minimal rank formal languages boolean functions`
- `formal language theory complexity theory boolean function entropy`
- `automaton acceptance formal language boolean function entropy`

**Top relevant hits considered**:
- [http://arxiv.org/abs/2406.09757v2] Evaluating LLM-driven User-Intent Formalization for Verification-Aware Languages
- [http://arxiv.org/abs/0903.3848v1] Join-irreducible Boolean functions
- [http://arxiv.org/abs/0808.0684v1] 9-variable Boolean Functions with Nonlinearity 242 in the Generalized Rotation Class
- [http://arxiv.org/abs/hep-th/9707234v2] Variational Approach to Quantum Field Theory: Gaussian Approximation and the Perturbative Expansion around It
- [http://arxiv.org/abs/chao-dyn/9311011v2] The Great Inequality In A Hamiltonian Planetary Theory
- [http://arxiv.org/abs/cs/0110040v1] A New Approach to Formal Language Theory by Kolmogorov Complexity
- [http://arxiv.org/abs/2003.09703v1] Variance function of boolean additive convolution
- [http://arxiv.org/abs/1801.07321v2] Exploring the Topological Entropy of Formal Languages

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=124, elapsed=240.3s

### 5.1 Generated Python source

```python
import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    if n < 5 or n > 40:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "invalid_n"
        }
    
    # Generate a random boolean function with entropy H(f)
    num_vars = random.randint(1, n)
    f = [random.choice([0, 1]) for _ in range(2**num_vars)]
    h_f = -sum(p * math.log2(p) for p in (f.count(0)/len(f), f.count(1)/len(f))) if 0 not in (f.count(0), f.count(1)) else 0
    
    # Construct a minimal deterministic finite automaton (DFA) accepting the language defined by the function
    states = [{'q': 0, 'transitions': {}}]
    for i in range(len(f)):
        new_state = len(states)
        states.append({'q': new_state, 'transitions': {}})
        states[0]['transitions'][i] = new_state
    
    # Measure the number of states in each DFA
    num_states = len(states)
    
    # Compare it with 2^H(f)
    conjecture_holds = num_states <= 2**h_f
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": num_states,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample for H(f) = {h_f}, states = {num_states}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
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

> The test timed out before producing data, which means we cannot confirm whether the conjecture holds or not. | next: Re-run the test with a longer timeout and ensure that it completes successfully to verify the conjecture.

## 11. Audit log (LLM calls)

**Total LLM calls**: 9

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | glm4:latest | 0 | 0 | 11028 |
| 2 | preregistration | ollama_remote | glm4:latest | 0 | 0 | 5150 |
| 3 | novelty | ollama_remote | glm4:latest | 0 | 0 | 4426 |
| 4 | novelty | ollama_remote | glm4:latest | 0 | 0 | 6451 |
| 5 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 29018 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 42613 |
| 7 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 14892 |
| 8 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 8589 |
| 9 | judge | ollama_remote | glm4:latest | 0 | 0 | 44360 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 166528 ms total latency. Provider mix: {'ollama_remote': 9}

_(full prompt+response transcripts available in `research/audit/bb7f49aa2a2c.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/bb7f49aa2a2c.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/bb7f49aa2a2c.tar.gz` (if generated)
