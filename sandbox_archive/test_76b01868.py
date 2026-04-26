# auto-injected by SEC sandbox to prevent common NameError crashes
import random
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
try:
    from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
except ImportError:
    pass
# end SEC prelude

"""
Empirical test of the Tropical Parseval Lower Bound on Discrepancy conjecture.

Conjecture: For every TropicalPolynomial f on {0,...,N-1} with
  F[k] = max_n (f[n] + theta(n,k)),  theta(n,k) = -2*pi*n*k/N
  Disc(f) = max_n f[n] - mean_n f[n]
  the double bound holds:  min_k F[k] <= Disc(f) <= max_k |F[k]|
with lower-bound saturation in >=95% of tropical autoconvolutions f*f
and <10% of generic random samples.

NOTE on expected outcome:
  theta(n,k) = -2*pi*n*k/N <= 0 for all n,k >= 0.
  Therefore F[k] >= f[0] (the n=0 term always contributes theta=0).
  So  min_k F[k] >= f[0].
  Disc(f) = max(f) - mean(f) can easily be < f[0] when mean(f) > 0
  and f[0] is large — giving a clear lower-bound violation.
  The upper bound  Disc(f) <= max|F[k]|  may also fail when Disc
  is large but all F[k] collapse near f[0].
"""

import sys
import json
import math
import random

TWO_PI = 2.0 * math.pi


# ---------------------------------------------------------------------------
# Core tropical operations — pure Python, stdlib only
# ---------------------------------------------------------------------------

def tropical_fourier_transform(f, N):
    """
    F[k] = max_n ( f[n] + theta(n,k) ),   theta(n,k) = -2*pi*n*k/N.
    Returns list of length N.
    """
    scale = TWO_PI / N
    F = []
    for k in range(N):
        best = -math.inf
        sk = scale * k              # precompute scale*k once per k
        for n in range(N):
            val = f[n] - sk * n
            if val > best:
                best = val
        F.append(best)
    return F


def tropical_discrepancy(f):
    """Disc(f) = max_n f[n] - mean_n f[n].  Always >= 0."""
    N = len(f)
    return max(f) - sum(f) / N


def tropical_convolution(f, g, N):
    """
    (f ★ g)[m] = max_{ a+b ≡ m (mod N) } ( f[a] + g[b] ).
    Max-plus cyclic convolution.
    """
    result = [-math.inf] * N
    for a in range(N):
        fa = f[a]
        for b in range(N):
            m = (a + b) % N
            val = fa + g[b]
            if val > result[m]:
                result[m] = val
    return result


# ---------------------------------------------------------------------------
# Single trial
# ---------------------------------------------------------------------------

def run_trial(seed: int) -> dict:
    """
    One independent replication using the given seed.

    Tests the double bound
        min_k F[k]  <=  Disc(f)  <=  max_k |F[k]|
    across N in {8, 16, 32, 64} for:
      - n_random   generic random tropical polynomials per N
      - n_autoconv tropical autoconvolutions f★f per N

    Also records whether the lower bound is *tight* (|Disc - min_F| <= 1e-6)
    for autoconvolutions vs. generic samples (acceptance-criterion check).
    """
    rng = random.Random(seed)

    N_values   = [8, 16, 32, 64]
    n_random   = 200    # generic random polys per N
    n_autoconv = 100    # autoconvolutions f★f per N
    tol        = 1e-6

    total_tested     = 0
    total_violations = 0
    lower_violations = 0
    upper_violations = 0
    first_counterexample = ""

    autoconv_tight = 0
    autoconv_total = 0
    generic_tight  = 0
    generic_total  = 0

    for N in N_values:

        # ---- generic random polynomials ----------------------------------
        for _ in range(n_random):
            f = [rng.uniform(-5.0, 5.0) for _ in range(N)]
            F    = tropical_fourier_transform(f, N)
            disc = tropical_discrepancy(f)
            min_F     = min(F)
            max_abs_F = max(abs(v) for v in F)

            total_tested  += 1
            generic_total += 1

            lower_ok = (min_F <= disc      + tol)
            upper_ok = (disc  <= max_abs_F + tol)

            if not lower_ok:
                lower_violations += 1
                total_violations += 1
                if first_counterexample == "":
                    mean_f = sum(f) / N
                    first_counterexample = (
                        f"random poly N={N} seed={seed}: "
                        f"lower bound VIOLATED — "
                        f"min_F={min_F:.6f} > Disc={disc:.6f}  "
                        f"[f[0]={f[0]:.4f}, max_f={max(f):.4f}, "
                        f"mean_f={mean_f:.4f}; "
                        f"note: min_F>=f[0] since theta(0,k)=0 always]"
                    )
            elif not upper_ok:
                upper_violations += 1
                total_violations += 1
                if first_counterexample == "":
                    first_counterexample = (
                        f"random poly N={N} seed={seed}: "
                        f"upper bound VIOLATED — "
                        f"Disc={disc:.6f} > max|F|={max_abs_F:.6f}"
                    )

            if abs(disc - min_F) <= tol:
                generic_tight += 1

        # ---- tropical autoconvolutions f★f -------------------------------
        for _ in range(n_autoconv):
            f = [rng.uniform(-5.0, 5.0) for _ in range(N)]
            g = tropical_convolution(f, f, N)   # g = f ★ f
            F    = tropical_fourier_transform(g, N)
            disc = tropical_discrepancy(g)
            min_F     = min(F)
            max_abs_F = max(abs(v) for v in F)

            total_tested   += 1
            autoconv_total += 1

            lower_ok = (min_F <= disc      + tol)
            upper_ok = (disc  <= max_abs_F + tol)

            if not lower_ok:
                lower_violations += 1
                total_violations += 1
                if first_counterexample == "":
                    mean_g = sum(g) / N
                    first_counterexample = (
                        f"autoconv N={N} seed={seed}: "
                        f"lower bound VIOLATED — "
                        f"min_F={min_F:.6f} > Disc={disc:.6f}  "
                        f"[g[0]={g[0]:.4f}, max_g={max(g):.4f}, "
                        f"mean_g={mean_g:.4f}]"
                    )
            elif not upper_ok:
                upper_violations += 1
                total_violations += 1
                if first_counterexample == "":
                    first_counterexample = (
                        f"autoconv N={N} seed={seed}: "
                        f"upper bound VIOLATED — "
                        f"Disc={disc:.6f} > max|F|={max_abs_F:.6f}"
                    )

            if abs(disc - min_F) <= tol:
                autoconv_tight += 1

    violation_rate      = total_violations / total_tested
    autoconv_tight_frac = autoconv_tight  / max(1, autoconv_total)
    generic_tight_frac  = generic_tight   / max(1, generic_total)

    return {
        "metric_name"         : "bound_violation_rate",
        "metric_value"        : violation_rate,
        "instances_tested"    : total_tested,
        "conjecture_holds"    : (total_violations == 0),
        "counterexample"      : first_counterexample,
        # secondary diagnostics (extra keys allowed by spec)
        "lower_violations"    : lower_violations,
        "upper_violations"    : upper_violations,
        "autoconv_tight_frac" : autoconv_tight_frac,
        "generic_tight_frac"  : generic_tight_frac,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]

    results            = []
    first_failing_seed = None
    first_ce           = ""

    for seed in seeds:
        trial = run_trial(seed)
        row   = {"seed": seed, **trial}
        print(f"TRIAL: {json.dumps(row)}")
        sys.stdout.flush()
        results.append(trial)
        if not trial["conjecture_holds"] and first_failing_seed is None:
            first_failing_seed = seed
            first_ce           = trial["counterexample"]

    # ---- aggregate statistics -------------------------------------------
    metric_values    = [r["metric_value"] for r in results]
    mean_mv          = sum(metric_values) / len(metric_values)
    var_mv           = sum((x - mean_mv) ** 2 for x in metric_values) / len(metric_values)
    std_mv           = math.sqrt(var_mv)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    avg_lower_viol = sum(r["lower_violations"]    for r in results) / len(results)
    avg_upper_viol = sum(r["upper_violations"]    for r in results) / len(results)
    avg_ac_tight   = sum(r["autoconv_tight_frac"] for r in results) / len(results)
    avg_gen_tight  = sum(r["generic_tight_frac"]  for r in results) / len(results)

    print(
        f"SUMMARY: "
        f"lower_viol_avg={avg_lower_viol:.1f}  "
        f"upper_viol_avg={avg_upper_viol:.1f}  "
        f"autoconv_tight_frac={avg_ac_tight:.4f}  "
        f"generic_tight_frac={avg_gen_tight:.4f}"
    )

    # ---- verdict --------------------------------------------------------
    if first_failing_seed is not None:
        print(
            f'RESULT: FALSIFIED counterexample="{first_ce}" '
            f"first_failing_seed={first_failing_seed}"
        )
    elif support_fraction >= 0.8:
        print(
            f"RESULT: SUPPORTED mean={mean_mv:.6f} std={std_mv:.6f} "
            f"support_fraction={support_fraction:.3f}"
        )
    else:
        print(
            f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.3f} "
            f"mean={mean_mv:.6f} std={std_mv:.6f}"
        )