# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

def walsh_hadamard_transform(g):
    n = len(g)
    N = 1 << n
    f = [0] * N
    for S in range(N):
        for z in range(N):
            parity = 1
            for i in range(n):
                if (S >> i) & 1:
                    parity *= g[z] if (z >> i) & 1 else -g[z]
            f[S] += parity
    return [x / N for x in f]

def spectral_norm(g):
    f = walsh_hadamard_transform(g)
    return max(abs(x) for x in f)

def popcount(x):
    return bin(x).count('1')

def compute_c(g):
    n = len(g)
    N = 1 << n
    c = [0] * N
    for a in range(N):
        for z in range(N):
            if all((z >> i) & 1 <= (a >> i) & 1 for i in range(n)):
                if g[z] == -1:
                    c[a] += 1
    return c

def star_discrepancy(g):
    n = len(g)
    N = 1 << n
    c = compute_c(g)
    P_g = sum(1 for x in g if x == -1)
    max_diff = 0.0
    for a in range(N):
        term1 = c[a] / N
        term2 = (P_g / N) * (2 ** popcount(a) / N)
        diff = abs(term1 - term2)
        if diff > max_diff:
            max_diff = diff
    return max_diff

def generate_random_g(n, seed):
    random.seed(seed)
    g = [random.choice([-1, 1]) for _ in range(1 << n)]
    return g

def generate_parity_g(n, seed):
    random.seed(seed)
    S = random.randint(1, (1 << n) - 1)
    g = [1] * (1 << n)
    for z in range(1 << n):
        parity = 1
        for i in range(n):
            if (S >> i) & 1:
                parity *= -1 if (z >> i) & 1 else 1
        g[z] = parity
    return g

def generate_junta_g(n, seed):
    random.seed(seed)
    k = n // 2
    S = random.sample(range(n), k)
    g = [1] * (1 << n)
    for z in range(1 << n):
        count = sum((z >> i) & 1 for i in S)
        g[z] = -1 if count > k // 2 else 1
    return g

def generate_and_g(n):
    g = [1] * (1 << n)
    for z in range(1 << n):
        if z == (1 << n) - 1:
            g[z] = -1
    return g

def generate_or_g(n):
    g = [1] * (1 << n)
    for z in range(1 << n):
        if z != 0:
            g[z] = -1
    return g

def generate_maj_g(n):
    g = [1] * (1 << n)
    for z in range(1 << n):
        count = popcount(z)
        if count > n // 2:
            g[z] = -1
    return g

def run_trial(seed):
    n_values = [6, 8, 10, 12, 14, 16, 18]
    results = []
    for n in n_values:
        for g_type in range(5):
            if g_type == 0:
                g = generate_random_g(n, seed)
            elif g_type == 1:
                g = generate_parity_g(n, seed)
            elif g_type == 2:
                g = generate_junta_g(n, seed)
            elif g_type == 3:
                g = generate_and_g(n)
            else:
                g = generate_or_g(n)

            norm = spectral_norm(g)
            discrepancy = star_discrepancy(g)

            lower_ratio = discrepancy / norm if norm != 0 else 0
            upper_ratio = discrepancy / (norm * math.log2(n + 1)) if norm != 0 else 0

            conjecture_holds = (lower_ratio >= 0.125) and (upper_ratio <= 8)

            counterexample = ""
            if not conjecture_holds:
                if lower_ratio < 0.125:
                    counterexample = f"Lower ratio {lower_ratio} < 0.125"
                elif upper_ratio > 8:
                    counterexample = f"Upper ratio {upper_ratio} > 8"

            results.append({
                "n": n,
                "g_type": g_type,
                "metric_name": "discrepancy",
                "metric_value": discrepancy,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample,
                "lower_ratio": lower_ratio,
                "upper_ratio": upper_ratio
            })

    overall_conjecture_holds = all(r["conjecture_holds"] for r in results)
    min_lower_ratio = min(r["lower_ratio"] for r in results)
    max_upper_ratio = max(r["upper_ratio"] for r in results)

    return {
        "seed": seed,
        "metric_name": "discrepancy",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": overall_conjecture_holds,
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), ""),
        "min_lower_ratio": min_lower_ratio,
        "max_upper_ratio": max_upper_ratio
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {json.dumps(trial)}")
        trials.append(trial)

    metric_values = [t["metric_value"] for t in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)

    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not t["conjecture_holds"] for t in trials):
        first_failing_seed = next(t["seed"] for t in trials if not t["conjecture_holds"])
        counterexample = next(t["counterexample"] for t in trials if not t["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")