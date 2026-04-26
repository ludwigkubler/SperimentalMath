# auto-injected by SEC sandbox
import random
import math
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

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