# auto-injected by SEC sandbox
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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_pdf(x):
    return (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * x**2)

def gaussian_cdf_inv(p):
    a = -0.3275911
    b = 0.2308467
    c = 0.9345453
    d = 0.0798480
    e = 0.0020342
    t = 1 - p
    return math.sqrt(-math.log(t)) * (-a + b*t + c*t**2 + d*t**3 + e*t**4)

def gaussian_cdf(x):
    if x < 0:
        return 0.5 - 0.5 * math.erf(-x / math.sqrt(2))
    else:
        return 0.5 + 0.5 * math.erf(x / math.sqrt(2))

def gaussian_sample():
    u1 = random.random()
    u2 = random.random()
    z0 = gaussian_cdf_inv(u1)
    z1 = -math.log(u2) ** 0.5
    return z0 + (z1 if random.random() < 0.5 else -z1)

def min_plus_convolution(f, n):
    g = [float('inf')] * n
    for i in range(n):
        for j in range(n):
            k = (i + j) % n
            g[k] = min(g[k], f[i] + f[j])
    return g

def maslov_dequantized_tft(h, n, beta=5):
    exp_h = [math.exp(-beta * h[j]) for j in range(n)]
    sum_exp_h = sum(exp_h)
    tft = [-1 / beta * math.log(sum_exp_h * math.exp(-2 * math.pi * 1j * k / n)) for k in range(n)]
    return tft

def mfc(h, n):
    return min(abs(tft[k]) for k in range(1, n))

def delta(f, g, n):
    return abs(mfc(g, n) - 2 * mfc(f, n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 12, 16, 20, 24, 28, 32, 36, 40]:
        f = [gaussian_sample() for _ in range(n)]
        g = min_plus_convolution(f, n)
        h_values = [f, g]
        for h in h_values:
            tft_h = maslov_dequantized_tft(h, n)
            mfc_h = mfc(h, n)
            results.append((n, delta(f, g, n)))
    metric_value = sum(val for _, val in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for n, _ in results)
    conjecture_holds = all(val <= 4 * math.sqrt(math.log(n)) for n, val in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Delta",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")