# auto-injected by SEC sandbox
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import json
import math
import random
import itertools
from collections import defaultdict

# ── helpers ────────────────────────────────────────────────────────────────────

def bits(x, n):
    return [(x >> i) & 1 for i in range(n)]

def inner_product_bits(a, b):
    return sum(ai * bi for ai, bi in zip(a, b)) % 2

# Walsh-Hadamard transform via fast butterfly
def wht(f_vals):
    """f_vals: list of 2^n values indexed by integer. Returns WHT coefficients."""
    a = list(f_vals)
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    return a

def compute_walsh_coeffs(f_vals):
    """Returns list of WHT coefficients (not normalized)."""
    return wht(f_vals)

# disc(M_f) for XOR-function = max_S |hat_f(S)| / 2^n  (using normalized convention)
# More precisely: disc = max_S |hat_f(S)| / 2^n
# But the conjecture uses disc >= c * 2^{-n/2}
# Standard: disc(M_f) = max_S |hat_f(S)| / 2^n  (the spectral norm bound for XOR functions)
# Actually for XOR functions disc(M_f) = max_S |f_hat(S)| / 2^n where f_hat is the WHT
# Let's double check: for parity f(x)=(-1)^{x·e_1}, f_hat(e_1)=2^n, all others 0
# disc(M_f) = 1 (trivially) ... that's too large.
# 
# Correct formula: For XOR communication matrix M_f(x,y)=f(x XOR y),
# disc(M_f) = max_{S} |hat_f(S)| / 2^n  where hat_f(S) = sum_x f(x)(-1)^{S·x}
# For parity: hat_f(e_1) = 2^n so disc=1. That's right since parity has disc=1/2... hmm.
# 
# Actually: disc with respect to combinatorial rectangles:
# disc(M_f) = max_{A,B} |sum_{x in A, y in B} f(x XOR y)| / 2^{2n}
# For XOR functions this equals max_S |hat_f(S)|^2 / 2^{2n} ... no.
#
# Let me be careful. The standard result is:
# disc(M_f) = max_S |hat_f(S)| / 2^n
# where hat_f(S) = (1/2^n) sum_x f(x) (-1)^{<S,x>}  (normalized)
# Then for parity: hat_f(e_1)=1, disc=1. That's wrong.
#
# OK let me use: hat_f(S) = sum_x f(x)(-1)^{<S,x>} (unnormalized, size 2^n)
# disc(M_f) = max_S |hat_f(S)| / 2^n
# For parity: |hat_f(e_1)| = 2^n, so disc=1. Hmm parity disc should be 2^{-n}.
#
# Actually disc for parity is: the matrix M_parity(x,y)=(-1)^{(x XOR y)_1}=(-1)^{x_1 XOR y_1}
# For any rectangle A x B: sum = |A_0||B_0| - |A_0||B_1| - |A_1||B_0| + |A_1||B_1|
# where A_i = {x in A : x_1=i}. Max = when |A_0|=|A|, |B_0|=|B|: sum=|A||B|.
# But normalized: disc = max |sum|/2^{2n} = |A||B|/2^{2n} <= 1/4.
# So disc(parity) = 1/4? That's also not 2^{-n}.
#
# I think the definition in the conjecture uses disc(M_f) = max_S |hat_f(S)| / 2^n
# normalized so that disc = O(1) means no discrepancy bound.
# For parity this gives disc=1, meaning it's trivially 1.
# 
# The conjecture says disc >= c * 2^{-n/2} and "equality achieved by parity-like spectra".
# For parity, disc = max_S |hat_f(S)|/2^n. If f=parity on first bit, hat_f(e_1)=2^n,
# disc=1 >> 2^{-n/2}. Equality achieved by... something with more spread.
#
# Let me re-read: "disc(M_f) = max_S |hat_f(S)| for XOR-functions" (from test_strategy).
# That would be a huge number. The "closed form" likely means something like:
# disc(M_f) = (1/2^n) * max_S |hat_f(S)|
# 
# Actually the standard result in communication complexity:
# For f: {0,1}^n -> {-1,+1} (an XOR function), 
# disc(M_f) = (1/2^n) * max_S |hat_f(S)| ... let me just check for inner product.
# Inner product mod 2: all nonzero WHT coefficients equal ±2^{n/2} (there are 2^n of them for n even).
# So max_S |hat_f(S)| / 2^n = 2^{n/2}/2^n = 2^{-n/2}.
# disc(IP_n) is known to be 2^{-n/2}. ✓
#
# For random function: expected max WHT ≈ O(sqrt(n) * 2^{n/2}), so disc ≈ sqrt(n)*2^{-n/2}.
#
# Great, so: disc(M_f) = (1/2^n) * max_S |hat_f(S)|  where hat_f(S) = sum_x f(x)(-1)^{<S,x>}

def compute_disc(f_vals, n):
    """disc(M_f) = max_S |hat_f(S)| / 2^n"""
    coeffs = compute_walsh_coeffs(f_vals)
    max_coeff = max(abs(c) for c in coeffs)
    return max_coeff / (2 ** n)

def lehmer_density(f_vals):
    """
    L(f) = #{i : (a_{i+1}-a_i) < (a_{i+1}+a_i)/(8 log2(1+i))} / #nonzero_coeffs
    where a_1 <= a_2 <= ... are magnitudes of nonzero WHT coefficients.
    """
    coeffs = compute_walsh_coeffs(f_vals)
    mags = sorted(abs(c) for c in coeffs if c != 0)
    if len(mags) <= 1:
        return 0.0
    count = 0
    total = len(mags)
    for i in range(len(mags) - 1):
        a_i = mags[i]
        a_next = mags[i + 1]
        diff = a_next - a_i
        denom = 8 * math.log2(1 + (i + 1))  # 1-indexed: i+1
        threshold = (a_next + a_i) / denom
        if diff < threshold:
            count += 1
    return count / total

# ── function families ──────────────────────────────────────────────────────────

def make_random_anf(n, degree, rng):
    """Random ANF polynomial of degree <= degree, returning f_vals in {-1,+1}^{2^n}."""
    N = 1 << n
    f_vals = []
    # Enumerate all monomials up to given degree
    monomials = []
    for d in range(1, degree + 1):
        for subset in itertools.combinations(range(n), d):
            monomials.append(subset)
    # Random subset of monomials
    chosen = [m for m in monomials if rng.random() < 0.5]
    if not chosen:
        chosen = [monomials[rng.randint(0, len(monomials)-1)]]
    for x in range(N):
        bx = bits(x, n)
        val = 0
        for mono in chosen:
            prod = 1
            for idx in mono:
                prod *= bx[idx]
            val ^= prod
        f_vals.append(1 - 2 * val)  # map {0,1} -> {+1,-1}
    return f_vals

def make_inner_product(n):
    """Inner product mod 2 function."""
    N = 1 << n
    f_vals = []
    half = n // 2
    for x in range(N):
        bx = bits(x, n)
        ip = sum(bx[i] * bx[i + half] for i in range(half)) % 2
        f_vals.append(1 - 2 * ip)
    return f_vals

def make_equality(n):
    """Equality function: f(x,y)=+1 iff x[:n//2]==x[n//2:] (treating x as concatenation)."""
    N = 1 << n
    half = n // 2
    f_vals = []
    for x in range(N):
        bx = bits(x, n)
        eq = 1 if bx[:half] == bx[half:] else -1
        f_vals.append(eq)
    return f_vals

def make_threshold(n):
    """Majority-like threshold: f(x)=+1 iff popcount(x) > n/2."""
    N = 1 << n
    f_vals = []
    for x in range(N):
        pc = bin(x).count('1')
        f_vals.append(1 if pc > n / 2 else -1)
    return f_vals

def make_clustered(n, rng):
    """
    Plant WHT coefficients at geometrically close magnitudes to maximize L(f).
    Build f_vals from inverse WHT of a planted spectrum.
    """
    N = 1 << n
    # Create a spectrum with many clustered pairs
    spectrum = [0] * N
    # Put mass on random subsets with similar magnitudes
    base = 2 ** (n // 2)
    # Cluster pairs: set coefficients at base and base+1 alternately
    indices = list(range(1, N))
    rng.shuffle(indices)
    num_active = min(N // 2, 2 ** (n - 1))
    for i in range(0, num_active - 1, 2):
        spectrum[indices[i]] = base
        spectrum[indices[i + 1]] = base + 1
    # Inverse WHT = WHT / N (since WHT is self-inverse up to scaling)
    f_raw = wht(spectrum)
    f_vals = [1 if v >= 0 else -1 for v in f_raw]
    return f_vals

# ── trial ──────────────────────────────────────────────────────────────────────

def run_trial(seed: int) -> dict:
    rng = random.Random(seed)
    c = 1.0 / 16.0
    n_values = [6, 8, 10]  # keep small for speed; n=10 means 1024-element vectors
    instances_tested = 0
    min_ratio = float('inf')
    counterexample = ""
    conjecture_holds = True

    for n in n_values:
        N = 1 << n
        families = []

        # Random ANF degree 2, 3, 4 (3 instances each)
        for deg in [2, 3, 4]:
            for _ in range(3):
                families.append(('anf_d' + str(deg), make_random_anf(n, deg, rng)))

        # Inner product (only for even n)
        if n % 2 == 0:
            families.append(('ip', make_inner_product(n)))

        # Equality
        if n % 2 == 0:
            families.append(('eq', make_equality(n)))

        # Threshold
        families.append(('threshold', make_threshold(n)))

        # Clustered (3 instances)
        for _ in range(3):
            families.append(('clustered', make_clustered(n, rng)))

        for name, f_vals in families:
            # Check it's nonconstant
            if len(set(f_vals)) < 2:
                continue

            disc = compute_disc(f_vals, n)
            L = lehmer_density(f_vals)

            # Conjecture: disc(M_f) >= c * 2^{-n/2} * (1 + L(f))^{-1}
            # Equivalently: disc(M_f) * (1 + L(f)) * 2^{n/2} >= c = 1/16
            lhs = disc * (1 + L) * (2 ** (n / 2))
            ratio = lhs  # should be >= 1/16

            instances_tested += 1
            if ratio < min_ratio:
                min_ratio = ratio

            if ratio < c:
                conjecture_holds = False
                counterexample = (
                    f"n={n} family={name} disc={disc:.6f} L={L:.4f} "
                    f"lhs={lhs:.6f} < c={c:.6f}"
                )
                # Return immediately on falsification
                return {
                    "metric_name": "min_disc_times_one_plus_L_times_2^{n/2}",
                    "metric_value": float(min_ratio),
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": counterexample,
                }

    return {
        "metric_name": "min_disc_times_one_plus_L_times_2^{n/2}",
        "metric_value": float(min_ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
    }


if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]

    results = []
    first_failing_seed = None
    falsified_example = ""

    for seed in seeds:
        result = run_trial(seed)
        row = {"seed": seed, **result}
        print("TRIAL: " + json.dumps(row))
        sys.stdout.flush()
        results.append(result)
        if not result["conjecture_holds"] and first_failing_seed is None:
            first_failing_seed = seed
            falsified_example = result["counterexample"]

    vals = [r["metric_value"] for r in results]
    mean_v = sum(vals) / len(vals)
    variance = sum((v - mean_v) ** 2 for v in vals) / len(vals)
    std_v = math.sqrt(variance)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if first_failing_seed is not None:
        print(f'RESULT: FALSIFIED counterexample="{falsified_example}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_v:.6f} std={std_v:.6f} support_fraction={support_fraction:.3f}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.3f} mean={mean_v:.6f} std={std_v:.6f}")