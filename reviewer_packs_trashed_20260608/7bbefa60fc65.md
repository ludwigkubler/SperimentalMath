---
title: "Reviewer Pack — Tropical Convolution Subadditivity of MinimalFourierCoeffici..."
subtitle: "Entry 7bbefa60fc65 · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-04-26 13:51:25 UTC"
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

# Tropical Convolution Subadditivity of MinimalFourierCoefficient and its Discrepancy Bound
**Entry ID**: `7bbefa60fc65`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-04-26 13:51:25 UTC

## 1. Conjecture
**Field A** (mathematical branch): TROPICAL_FOURIER_ANALYSIS within tropical algebra and Fourier-analytic combinatorics (max-plus harmonic analysis on finite abelian groups)
**Field B** (complexity object): Communication complexity lower bounds via the discrepancy method (specifically, the unbounded-error and randomized communication complexity of XOR-functions defined by tropical polynomials over Z_n)

**Statement**:

> Let f, g: Z_n -> R be tropical polynomials with TropicalFourierTransform coefficients f_hat(k) = min_x (f(x) - (k*x mod n)/n) and analogously g_hat. Define MinimalFourierCoefficient mu(f) = min_k f_hat(k). Then for the tropical (min-plus) convolution h = f *_trop g defined by h(z) = min_{x+y=z mod n} (f(x)+g(y)), the following holds: (i) mu(h) >= mu(f) + mu(g) (subadditivity inheriting from Axiom A1's preservation of semiring structure), and (ii) DiscrepancyMeasure(h) <= 2 * max(|mu(f)|, |mu(g)|) + |mu(f) + mu(g)|, which strictly refines Axiom A3 by replacing the maximum absolute Fourier coefficient with a quantity controlled by MinimalFourierCoefficient on each factor.

**Rationale (proposer's reasoning)**:

> This sub-conjecture jointly tests Axiom A1 (tropical convolution preserves semiring structure, so the Legendre-style tropical Fourier transform should be additive on factors) and Axiom A3 (discrepancy is controlled by Fourier coefficients). Under the standard analogy between classical convolution-becomes-multiplication and tropical convolution-becomes-tropical-multiplication (i.e., addition in min-plus), the minimum over Fourier dual variables should compose additively. Because the target invariant MinimalFourierCoefficient is exactly mu(f), establishing subadditivity gives a *constructive* lower bound on mu(h) without computing the convolution's full transform, and ties directly into the discrepancy method's role in proving communication complexity lower bounds.

**Taxonomy category**: `FOURIER_ANALYTIC` (status at proposal time: )

**Framework membership**: framework `fw_28b4bfb95f`, role: elaboration

## 2. Pre-registration (Popper-style)
**Hash (SHA-256 prefix)**: `2d39f830518d19fd`

This hash commits to the conjecture statement, acceptance criterion, and seed list **before** the empirical test runs. Tampering with the test or its data after this hash was computed would be detectable.

**Acceptance criterion**:

> Across 600 trials (200 pairs × n∈{8,16,32}, fixed seeds 0–199), inequality (i) mu(h) >= mu(f)+mu(g) - 1e-9 must hold for every trial, and inequality (ii) Discrepancy(h) <= 2*max(|mu(f)|,|mu(g)|)+|mu(f)+mu(g)| must hold for every trial. Refinement vs A3 must occur in >=50% of trials.

## 3. Barrier filter (F1)
**Final**: `PASS`

| Barrier | Verdict | Confidence | LLM₁ | LLM₂ |
|---|---|---:|---|---|
| RELATIVIZATION | SAFE | 0.95 | SAFE | SAFE |
| NATURAL_PROOFS | SAFE | 0.95 | SAFE | SAFE |
| ALGEBRIZATION | SAFE | 0.95 | SAFE | SAFE |
| KARP_LIPTON | SAFE | 0.99 | SAFE | SAFE |

## 4. Novelty audit
**Verdict**: `NOVEL` against 13 hits across arXiv + Semantic Scholar + ECCC

**Search queries** (5):
- `tropical Fourier transform min-plus convolution finite abelian group`
- `max-plus harmonic analysis discrepancy communication complexity XOR function`
- `tropical polynomial Fourier coefficient subadditivity Z_n cyclic group`
- `unbounded-error randomized communication complexity discrepancy method tropical semiring`
- `min-plus convolution Fourier coefficient lower bound XOR function discrepancy`

**Top relevant hits considered**:
- [http://arxiv.org/abs/1912.07071v3] Fourier transforms on the basic affine space of a quasi-split group
- [http://arxiv.org/abs/1010.5964v1] Quadratic discrete Fourier transform and mutually unbiased bases
- [http://arxiv.org/abs/1207.2443v2] Tropical Teichmuller and Siegel spaces
- [http://arxiv.org/abs/0909.3392v2] On the communication complexity of XOR functions
- [http://arxiv.org/abs/0808.1762v2] Communication Complexities of XOR functions
- [http://arxiv.org/abs/2310.20606v2] One-Way Communication Complexity of Partial XOR Functions
- [http://arxiv.org/abs/2005.06373v2] Counting Schur Rings over Cyclic Groups of Semi-prime Order
- [http://arxiv.org/abs/hep-ph/0610012v1] Tevatron-for-LHC Report of the QCD Working Group

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=0, elapsed=0.5s

### 5.1 Generated Python source

```python
"""
Empirical test: Tropical Convolution Subadditivity of MinimalFourierCoefficient
and its Discrepancy Bound.

Definitions (all arithmetic in Z_n = {0, ..., n-1}):
  f_hat(k) = min_x (f[x] - (k*x % n) / n)    [tropical Fourier coefficient]
  mu(f)    = min_k f_hat(k)                    [MinimalFourierCoefficient]
  h(z)     = min_{x+y = z mod n} (f[x]+g[y])  [tropical / min-plus convolution]
  Disc(h)  = max_z h(z) - min_z h(z)           [DiscrepancyMeasure]

Conjecture:
  (i)  mu(h) >= mu(f) + mu(g)
  (ii) Disc(h) <= 2*max(|mu(f)|, |mu(g)|) + |mu(f)+mu(g)|
  Refinement: RHS of (ii) < max_k |h_hat(k)|  in >=50% of trials

Stdlib only: sys, json, math, random.
"""

import sys
import json
import math
import random


# ---------------------------------------------------------------------------
# Core primitives  (O(n^2), pure Python)
# ---------------------------------------------------------------------------

def trop_fourier(f, n):
    """f_hat[k] = min_x (f[x] - (k*x % n) / n),  for k in range(n)."""
    result = []
    for k in range(n):
        best = None
        for x in range(n):
            v = f[x] - (k * x % n) / n
            if best is None or v < best:
                best = v
        result.append(best)
    return result


def mu_min(f_hat):
    """MinimalFourierCoefficient = min_k f_hat(k)."""
    return min(f_hat)


def minplus_conv(f, g, n):
    """h[z] = min_{x+y = z mod n} (f[x] + g[y])."""
    h = [None] * n
    for z in range(n):
        best = None
        for x in range(n):
            v = f[x] + g[(z - x) % n]
            if best is None or v < best:
                best = v
        h[z] = best
    return h


def disc(h):
    """DiscrepancyMeasure = max(h) - min(h)."""
    return max(h) - min(h)


def bound_ii_rhs(mu_f, mu_g):
    """RHS of (ii): 2*max(|mu_f|, |mu_g|) + |mu_f + mu_g|."""
    return 2.0 * max(abs(mu_f), abs(mu_g)) + abs(mu_f + mu_g)


def axiom_a3_bound(h_hat):
    """Axiom-A3 bound = max_k |h_hat(k)|."""
    return max(abs(v) for v in h_hat)


# ---------------------------------------------------------------------------
# Trial runner
# ---------------------------------------------------------------------------

def run_trial(seed):
    # type: (int) -> dict
    """
    Draw 200 (f, g) pairs for each n in {8, 16, 32} -> 600 instances total.

    Returns required dict:
      metric_name, metric_value (mean slack of ineq i), instances_tested,
      conjecture_holds, counterexample
    plus extras: violations_i, violations_ii, refinement_fraction.
    """
    rng         = random.Random(seed)
    N_VALUES    = [8, 16, 32]
    PAIRS_PER_N = 200
    TOL         = 1e-9

    total      = 0
    viol_i     = 0
    viol_ii    = 0
    refine_hit = 0
    slack_sum  = 0.0
    first_ce   = ""

    for n in N_VALUES:
        for _p in range(PAIRS_PER_N):
            # Sample tropical polynomials with coefficients uniform in [-5, 5]
            f = [rng.uniform(-5.0, 5.0) for _i in range(n)]
            g = [rng.uniform(-5.0, 5.0) for _i in range(n)]

            fh   = trop_fourier(f, n)
            gh   = trop_fourier(g, n)
            mu_f = mu_min(fh)
            mu_g = mu_min(gh)

            h    = minplus_conv(f, g, n)
            hh   = trop_fourier(h, n)
            mu_h = mu_min(hh)
            dh   = disc(h)

            # ---- inequality (i): mu(h) >= mu(f) + mu(g) ----
            slack = mu_h - (mu_f + mu_g)
            slack_sum += slack
            if slack < -TOL:
                viol_i += 1
                if not first_ce:
                    first_ce = (
                        "ineq_i n=%d seed=%d mu_h=%.6f "
                        "sum_mu=%.6f slack=%.3e"
                        % (n, seed, mu_h, mu_f + mu_g, slack)
                    )

            # ---- inequality (ii): Disc(h) <= bound_ii_rhs ----
            b2 = bound_ii_rhs(mu_f, mu_g)
            if dh > b2 + TOL:
                viol_ii += 1
                if not first_ce:
                    first_ce = (
                        "ineq_ii n=%d seed=%d Disc_h=%.6f "
                        "bound=%.6f mu_f=%.4f mu_g=%.4f"
                        % (n, seed, dh, b2, mu_f, mu_g)
                    )

            # ---- refinement: bound_ii < Axiom-A3 bound ----
            if b2 < axiom_a3_bound(hh):
                refine_hit += 1

            total += 1

    mean_slack  = slack_sum / total if total else 0.0
    refine_frac = refine_hit / total if total else 0.0
    holds       = (viol_i == 0) and (viol_ii == 0)

    return {
        "metric_name":         "mean_slack_ineq_i",
        "metric_value":        mean_slack,
        "instances_tested":    total,
        "conjecture_holds":    holds,
        "counterexample":      first_ce if not holds else "",
        "violations_i":        viol_i,
        "violations_ii":       viol_ii,
        "refinement_fraction": refine_frac,
    }


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------

def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((v - m) ** 2 for v in xs) / len(xs))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]

    results            = []
    first_failing_seed = None
    first_ce_global    = ""

    for seed in seeds:
        trial = run_trial(seed)
        row   = {"seed": seed}
        row.update(trial)
        print("TRIAL: " + json.dumps(row))
        sys.stdout.flush()
        results.append(trial)
        if not trial["conjecture_holds"] and first_failing_seed is None:
            first_failing_seed = seed
            first_ce_global    = trial["counterexample"]

    metric_vals   = [r["metric_value"]        for r in results]
    refine_vals   = [r["refinement_fraction"] for r in results]
    support_frac  = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    mean_val      = _mean(metric_vals)
    std_val       = _std(metric_vals)
    mean_refine   = _mean(refine_vals)
    total_viol_i  = sum(r["violations_i"]  for r in results)
    total_viol_ii = sum(r["violations_ii"] for r in results)

    print(
        "\nSummary: seeds=%s support_fraction=%.3f mean_slack_i=%.6f "
        "std=%.6f violations_i=%d violations_ii=%d "
        "mean_refinement_fraction=%.3f"
        % (str(seeds), support_frac, mean_val, std_val,
           total_viol_i, total_viol_ii, mean_refine)
    )

    if first_failing_seed is not None:
        print(
            'RESULT: FALSIFIED counterexample="%s" first_failing_seed=%d'
            % (first_ce_global, first_failing_seed)
        )
    elif support_frac >= 0.8 and mean_refine >= 0.50:
        print(
            "RESULT: SUPPORTED mean=%.6f std=%.6f support_fraction=%.3f"
            % (mean_val, std_val, support_frac)
        )
    elif support_frac >= 0.8:
        print(
            "RESULT: INCONCLUSIVE inequalities_hold=True "
            "but refinement_fraction=%.3f < 0.50 "
            "(A3-refinement clause not satisfied)" % mean_refine
        )
    else:
        print(
            "RESULT: INCONCLUSIVE support_fraction=%.3f "
            "violations_i=%d violations_ii=%d"
            % (support_frac, total_viol_i, total_viol_ii)
        )
```

## 6. Per-seed results

| Seed | Metric value | Holds? | Counterexample |
|---:|---:|:-:|---|
| 11 | 0.8203247853146347 | ✓ |  |
| 23 | 0.8110094059267055 | ✓ |  |
| 37 | 0.7914336582481677 | ✓ |  |
| 53 | 0.8293467548319479 | ✓ |  |
| 71 | 0.8305321982334402 | ✓ |  |

**Aggregate statistics**:

| Statistic | Value |
|---|---|
| `n_seeds` | 5 |
| `metric_mean` | 0.8165293605109791 |
| `metric_std` | 0.0160859758918841 |
| `metric_ci95_half` | 0.014387734231470262 |
| `metric_min` | 0.7914336582481677 |
| `metric_max` | 0.8305321982334402 |
| `support_fraction` | 1.0 |

## 7. Test stdout (last 2KB)

```
TRIAL: {"seed": 11, "metric_name": "mean_slack_ineq_i", "metric_value": 0.8203247853146347, "instances_tested": 600, "conjecture_holds": true, "counterexample": "", "violations_i": 0, "violations_ii": 0, "refinement_fraction": 0.0}
TRIAL: {"seed": 23, "metric_name": "mean_slack_ineq_i", "metric_value": 0.8110094059267055, "instances_tested": 600, "conjecture_holds": true, "counterexample": "", "violations_i": 0, "violations_ii": 0, "refinement_fraction": 0.0}
TRIAL: {"seed": 37, "metric_name": "mean_slack_ineq_i", "metric_value": 0.7914336582481677, "instances_tested": 600, "conjecture_holds": true, "counterexample": "", "violations_i": 0, "violations_ii": 0, "refinement_fraction": 0.0}
TRIAL: {"seed": 53, "metric_name": "mean_slack_ineq_i", "metric_value": 0.8293467548319479, "instances_tested": 600, "conjecture_holds": true, "counterexample": "", "violations_i": 0, "violations_ii": 0, "refinement_fraction": 0.0}
TRIAL: {"seed": 71, "metric_name": "mean_slack_ineq_i", "metric_value": 0.8305321982334402, "instances_tested": 600, "conjecture_holds": true, "counterexample": "", "violations_i": 0, "violations_ii": 0, "refinement_fraction": 0.0}

Summary: seeds=[11, 23, 37, 53, 71] support_fraction=1.000 mean_slack_i=0.816529 std=0.014388 violations_i=0 violations_ii=0 mean_refinement_fraction=0.000
RESULT: INCONCLUSIVE inequalities_hold=True but refinement_fraction=0.000 < 0.50 (A3-refinement clause not satisfied)

```

## 8. Critic adversarial review
**Critic verdict**: `CHALLENGE`

**Critic reasoning**:

> The result line itself says 'INCONCLUSIVE' because refinement_fraction=0.000 across all 5 seeds — the discrepancy bound (ii) never strictly refines A3, so the central novelty claim is empirically falsified, not supported. Furthermore, part (i) is mathematically trivial: mu(h) = min_k (f_hat(k)+g_hat(k)) >= min_k f_hat(k) + min_k g_hat(k) = mu(f)+mu(g) follows directly from min-plus distributivity, so 0 violations on (i) is a tautology, not evidence. The 'mean_slack_ineq_i' metric (~0.82) measure

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> The test's RESULT line explicitly states INCONCLUSIVE because refinement_fraction=0.000 across all 5 seeds, failing the pre-registered >=0.50 refinement clause; while inequalities (i) and (ii) held in every trial, (i) is a trivial consequence of min-plus distributivity and (ii) never strictly refines A3, so the novelty claim is unsupported. | next: Tighten clause (ii) to a non-trivial bound (e.g., Discrepancy(h) <= |mu(f)+mu(g)| + epsilon-correction term derived from coefficient spread) and re-t

## 11. Audit log (LLM calls)

_(no audit log file — pre-Fase-A cycle)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/7bbefa60fc65.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/7bbefa60fc65.tar.gz` (if generated)
