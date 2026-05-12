---
title: "Reviewer Pack — Kronecker Coefficient Gap in Symmetric Decompositions of Per..."
subtitle: "Entry b1e1fdcf3c47 · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-05-12 11:18:21 UTC"
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

# Kronecker Coefficient Gap in Symmetric Decompositions of Permanent Polynomials
**Entry ID**: `b1e1fdcf3c47`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-05-12 11:18:21 UTC

## 1. Conjecture
**Field A** (mathematical branch): Representation Theory of Symmetric Groups (Kronecker coefficients)
**Field B** (complexity object): Boolean Circuit Size for Permanent Polynomial

**Statement**:

> For a random n×n matrix M with entries ±1, the Kronecker coefficient g(λ, μ, ν) for the decomposition of Sym^2(Perm_n) ⊗ Sym^2(Perm_n) is Ω(n^2) and O(n^3), where λ, μ, ν are partitions of 2n. The ratio g(λ, μ, ν)/n^2 is strictly greater than 1 for all n ≤ 40.

**Rationale (proposer's reasoning)**:

> Kronecker coefficients encode the multiplicity of irreducible representations in tensor products, which could reflect the inherent symmetry complexity of permanent polynomials. Their growth rate may correlate with the minimal circuit size required to compute the permanent, as symmetric decompositions often require more terms than antisymmetric ones.

**Taxonomy category**: `GCT_DET_PERM` (status at proposal time: alive)

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `64f4861003016fb3`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> default: >=80% seeds must support, no counterexample

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | SAFE | 0.95 | SAFE | UNCERTAIN |
| NATURAL_PROOFS | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |
| ALGEBRIZATION | SAFE | 0.95 | SAFE | SAFE |
| KARP_LIPTON | SAFE | 0.00 | UNCERTAIN | UNCERTAIN |

## 4. Novelty audit
**Verdict**: `NOVEL` against 0 hits across arXiv + Semantic Scholar + ECCC

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=1, elapsed=0.2s

### 5.1 Generated Python source

```python
import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def sign(x):
        return 1 if x >= 0 else -1
    
    def binomial(n, k):
        if k > n:
            return 0
        result = 1
        for i in range(k):
            result *= (n - i)
            result //= (i + 1)
        return result
    
    def kronecker_coefficient(λ, μ, ν):
        if len(λ) != len(μ) or len(μ) != len(ν):
            return 0
        n = len(λ)
        coeff = Fraction(1)
        for i in range(n):
            coeff *= binomial(λ[i] + μ[i], λ[i]) * binomial(μ[i] + ν[i], μ[i])
            coeff //= (binomial(λ[i] + ν[i], λ[i]) * binomial(ν[i] + λ[i], ν[i]))
        return abs(coeff)
    
    def perm(n):
        if n == 0:
            return [[]]
        result = []
        for i in range(n):
            for p in perm(n - 1):
                if not any(p[j] == i for j in range(len(p))):
                    result.append([i] + p)
        return result
    
    def sym_power(poly, k):
        result = [poly[0]]
        for _ in range(1, k):
            new_poly = [0] * (len(result) + len(poly) - 1)
            for i in range(len(result)):
                for j in range(len(poly)):
                    new_poly[i + j] += result[i] * poly[j]
            result = new_poly
        return result
    
    def tensor_product(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                result[i * len(poly2) + j] = poly1[i] * poly2[j]
        return result
    
    def kronecker_product(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                result[i * len(poly2) + j] = poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i <= j:
                    result[i * len(poly2) + j] = poly1[i] * poly2[j]
                else:
                    result[i * len(poly2) + j] = -poly1[i] * poly2[j]
        return result
    
    def kronecker_product_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric_antisymmetric_symmetric(poly1, poly2):
        result = [0] * (len(poly1) * len(poly2))
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                if i < j:
# ... [truncated, full source in replay tarball]

```

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```

--STDERR--
Traceback (most recent call last):
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_c507cd2f.py", line 97, in <module>
    result = run_trial(seed)
             ^^^^^^^^^^^^^^^
  File "/home/ludo/Scrivania/SEC/research/pvsnp_sandbox/test_c507cd2f.py", line 81, in run_trial
    ratio = coeff / (n**2)
            ~~~~~~^~~~~~~~
OverflowError: integer division result too large for a float

```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> skipped: test crashed before producing data

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> Test crashed with overflow error during ratio calculation, preventing verification of conjecture for n ≤ 40 | next: Implement arbitrary-precision arithmetic or reformulate ratio calculation to avoid overflow

## 11. Audit log (LLM calls)

**Total LLM calls**: 7

| # | Phase | Provider | Model | Tokens in | out | Latency (ms) |
|---:|---|---|---|---:|---:|---:|
| 1 | propose | ollama_remote | qwen3:8b | 0 | 0 | 76647 |
| 2 | preregistration | ollama_remote | qwen3:8b | 0 | 0 | 24541 |
| 3 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 20873 |
| 4 | novelty | ollama_remote | qwen3:8b | 0 | 0 | 14835 |
| 5 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 13360 |
| 6 | test_gen | ollama_remote | qwen2.5-coder:7b | 0 | 0 | 84039 |
| 7 | judge | ollama_remote | qwen3:8b | 0 | 0 | 18507 |

**Totals**: 0 input tokens, 0 output tokens, ~$0.0000 cost, 252802 ms total latency. Provider mix: {'ollama_remote': 7}

_(full prompt+response transcripts available in `research/audit/b1e1fdcf3c47.jsonl`)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/b1e1fdcf3c47.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/b1e1fdcf3c47.tar.gz` (if generated)
