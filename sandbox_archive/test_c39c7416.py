# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_random_g(n, seed):
    random.seed(seed)
    g = [random.choice([-1, 1]) for _ in range(2**n)]
    return g

def generate_parity_g(n, seed):
    random.seed(seed)
    S = random.sample(range(n), random.randint(1, n))
    g = [1] * (2**n)
    for i in range(2**n):
        z = [int(b) for b in bin(i)[2:].zfill(n)]
        if sum(z[j] for j in S) % 2 == 1:
            g[i] = -1
    return g

def generate_junta_g(n, seed):
    random.seed(seed)
    k = math.ceil(n / 2)
    S = random.sample(range(n), k)
    g = [1] * (2**n)
    for i in range(2**n):
        z = [int(b) for b in bin(i)[2:].zfill(n)]
        if sum(z[j] for j in S) >= k / 2:
            g[i] = -1
    return g

def generate_and_g(n):
    g = [1] * (2**n)
    for i in range(2**n):
        z = [int(b) for b in bin(i)[2:].zfill(n)]
        if all(z[j] == 1 for j in range(n)):
            g[i] = -1
    return g

def generate_or_g(n):
    g = [1] * (2**n)
    for i in range(2**n):
        z = [int(b) for b in bin(i)[2:].zfill(n)]
        if any(z[j] == 1 for j in range(n)):
            g[i] = -1
    return g

def generate_maj_g(n):
    g = [1] * (2**n)
    for i in range(2**n):
        z = [int(b) for b in bin(i)[2:].zfill(n)]
        if sum(z[j] for j in range(n)) >= n / 2:
            g[i] = -1
    return g

def walsh_hadamard_transform(g, n):
    gh = [0.0] * (2**n)
    for S in range(2**n):
        for z in range(2**n):
            dot_product = sum((int(b) for b in bin(S & z)[2:].zfill(n)))
            gh[S] += g[z] * ((-1) ** dot_product)
    return gh

def spectral_norm(gh, n):
    return max(abs(x) for x in gh) / (2**n)

def star_discrepancy(g, n):
    c = [0] * (2**n)
    for a in range(2**n):
        for z in range(2**n):
            if all((z & (1 << i)) <= (a & (1 << i)) for i in range(n)):
                if g[z] == -1:
                    c[a] += 1
    P_g = sum(1 for x in g if x == -1)
    discrepancy = 0.0
    for a in range(2**n):
        popcount = bin(a).count('1')
        term = abs(c[a] / (2**n) - (P_g / (2**n)) * (2**popcount / (2**n)))
        if term > discrepancy:
            discrepancy = term
    return discrepancy

def run_trial(seed):
    n_values = [6, 8, 10, 12, 14, 16, 18]
    n = random.choice(n_values)
    random.seed(seed)
    g_type = random.choice(['random', 'parity', 'junta', 'and', 'or', 'maj'])
    if g_type == 'random':
        g = generate_random_g(n, seed)
    elif g_type == 'parity':
        g = generate_parity_g(n, seed)
    elif g_type == 'junta':
        g = generate_junta_g(n, seed)
    elif g_type == 'and':
        g = generate_and_g(n)
    elif g_type == 'or':
        g = generate_or_g(n)
    elif g_type == 'maj':
        g = generate_maj_g(n)

    gh = walsh_hadamard_transform(g, n)
    spectral_norm_val = spectral_norm(gh, n)
    discrepancy = star_discrepancy(g, n)

    lower_bound = 0.125 * spectral_norm_val
    upper_bound = 8 * spectral_norm_val * math.log2(n + 1)

    conjecture_holds = (lower_bound <= discrepancy <= upper_bound)
    counterexample = ""
    if not conjecture_holds:
        if discrepancy < lower_bound:
            counterexample = f"Lower bound violated: D*_lat={discrepancy} < {lower_bound}"
        else:
            counterexample = f"Upper bound violated: D*_lat={discrepancy} > {upper_bound}"

    return {
        "metric_name": "star_discrepancy",
        "metric_value": discrepancy,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
        "spectral_norm": spectral_norm_val,
        "n": n,
        "g_type": g_type
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    metric_values = [trial["metric_value"] for trial in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in results if trial["conjecture_holds"]) / len(results)

    if all(trial["conjecture_holds"] for trial in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in results):
        first_failing_seed = next(trial["seed"] for trial in results if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in results if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")