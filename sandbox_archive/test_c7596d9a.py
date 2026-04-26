# auto-injected by SEC sandbox
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

import sys
import json
import math
import cmath
import random


# ── Tropical helpers ────────────────────────────────────────────────────────

def tropical_convolution(f, n):
    """g[x] = min_{y in Z_n} (f[y] + f[(x-y) mod n])  (min-plus self-convolution)"""
    g = [0.0] * n
    for x in range(n):
        mv = f[0] + f[x % n]
        for y in range(1, n):
            v = f[y] + f[(x - y) % n]
            if v < mv:
                mv = v
        g[x] = mv
    return g


def tropical_fourier_transform(f, beta, n):
    """
    Maslov-dequantized TFT:
        F_beta[f](k) = -(1/beta) * log( sum_x exp(-beta*f[x]) * exp(-2*pi*i*k*x/n) )

    Returns list of |F_beta[f](k)| for k = 0 … n-1.

    FIX vs attempt #1: we NEVER pass a complex value to math.exp.
    Instead we split exp(-beta*f[x]) * e^{i*angle} into:
        real weight  w = math.exp(-beta * f[x])            (always real)
        rotation     e^{i*angle} = cos(angle) + i*sin(angle)
    then assemble the complex sum explicitly before calling cmath.log.
    """
    mags = []
    for k in range(n):
        re_s = 0.0
        im_s = 0.0
        for x in range(n):
            w = math.exp(-beta * f[x])               # real weight – math.exp is safe
            angle = -2.0 * math.pi * k * x / n       # real angle
            re_s += w * math.cos(angle)
            im_s += w * math.sin(angle)
        s = complex(re_s, im_s)
        if abs(s) < 1e-290:                          # degenerate: DFT sum ≈ 0
            mags.append(float('inf'))
        else:
            log_s = cmath.log(s)                     # cmath handles complex arg
            coeff = -(1.0 / beta) * log_s            # complex Fourier coefficient
            mags.append(abs(coeff))                  # magnitude
    return mags


def min_fourier_coeff(mags):
    """MinimalFourierCoefficient = min_k |F_beta[f](k)|."""
    finite = [v for v in mags if math.isfinite(v)]
    return min(finite) if finite else float('inf')


def discrepancy(f):
    """DiscrepancyMeasure = max(f) - min(f)."""
    return max(f) - min(f)


# ── Core trial ───────────────────────────────────────────────────────────────

def run_trial(seed: int) -> dict:
    rng = random.Random(seed)
    ns = [8, 16, 32, 64]
    betas = [5, 10, 20]
    num_polys = 15       # polynomials per n-cell (fast enough in pure Python)
    C = 5.0              # constant in error bound |MinFC(g) - 2*MinFC(f)| ≤ C/n

    total_tests = 0
    total_passes = 0
    all_scaled_errors = []   # collect error_i * n for mean check
    counterexample = ""

    for n in ns:
        for _ in range(num_polys):
            # Random tropical polynomial: integer coefficients in [-10, 10]
            f = [float(rng.randint(-10, 10)) for _ in range(n)]
            g = tropical_convolution(f, n)

            disc_f = discrepancy(f)
            disc_g = discrepancy(g)
            # (ii) Disc(g) ≤ 2·Disc(f)  (provable: min(g)=2·min(f), max(g)≤2·max(f))
            check_ii = (disc_g <= 2.0 * disc_f + 1e-6)

            for beta in betas:
                Ff = tropical_fourier_transform(f, beta, n)
                Fg = tropical_fourier_transform(g, beta, n)

                mf = min_fourier_coeff(Ff)
                mg = min_fourier_coeff(Fg)

                # Skip degenerate instances where a DFT bucket collapses to 0
                if not (math.isfinite(mf) and math.isfinite(mg)):
                    continue

                error_i = abs(mg - 2.0 * mf)
                check_i = (error_i <= C / n)
                all_scaled_errors.append(error_i * n)

                total_tests += 1
                if check_i and check_ii:
                    total_passes += 1
                elif not counterexample:
                    parts = []
                    if not check_i:
                        parts.append(
                            f"|MinFC(g)-2*MinFC(f)|={error_i:.5f} > C/n={C/n:.5f}"
                        )
                    if not check_ii:
                        parts.append(
                            f"disc_g={disc_g:.2f} > 2*disc_f={2*disc_f:.2f}"
                        )
                    counterexample = f"n={n},beta={beta}: {'; '.join(parts)}"

    support_fraction = total_passes / total_tests if total_tests > 0 else 0.0
    mean_scaled = (
        sum(all_scaled_errors) / len(all_scaled_errors)
        if all_scaled_errors else float('inf')
    )
    # Acceptance: ≥95% pass AND mean scaled error ≤ 5
    conjecture_holds = (support_fraction >= 0.95 and mean_scaled <= 5.0)

    return {
        "metric_name": "support_fraction",
        "metric_value": support_fraction,
        "instances_tested": total_tests,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample if not conjecture_holds else "",
    }


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    seeds = (
        [int(s) for s in sys.argv[1:]]
        if len(sys.argv) > 1
        else [11, 23, 37, 53, 71]
    )

    results = []
    first_failing_seed = None
    first_counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        row = {"seed": seed, **result}
        print(f"TRIAL: {json.dumps(row)}", flush=True)
        results.append(result)
        if not result["conjecture_holds"] and first_failing_seed is None:
            first_failing_seed = seed
            first_counterexample = result["counterexample"]

    metric_values = [r["metric_value"] for r in results]
    mean_val = sum(metric_values) / len(metric_values)
    variance = (
        sum((v - mean_val) ** 2 for v in metric_values) / max(len(metric_values) - 1, 1)
    )
    std_val = math.sqrt(variance)
    support_frac = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_frac >= 0.8:
        print(
            f"RESULT: SUPPORTED mean={mean_val:.6f} std={std_val:.6f}"
            f" support_fraction={support_frac:.3f}"
        )
    elif first_counterexample:
        print(
            f'RESULT: FALSIFIED counterexample="{first_counterexample}"'
            f" first_failing_seed={first_failing_seed}"
        )
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_frac:.3f}")