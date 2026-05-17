# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def generate_g(n, seed):
    random.seed(seed)
    g_type = random.randint(0, 3)
    if g_type == 0:  # uniform
        g = [random.choice([-1, 1]) for _ in range(2**n)]
    elif g_type == 1:  # parity
        S = random.sample(range(n), random.randint(1, n))
        g = [(-1)**sum((z >> i) & 1 for i in S) for z in range(2**n)]
    elif g_type == 2:  # k-junta threshold
        k = max(1, n // 2)
        S = random.sample(range(n), k)
        g = [(-1)**(sum((z >> i) & 1 for i in S) >= k//2) for z in range(2**n)]
    else:  # AND/OR/MAJ
        op = random.choice(['AND', 'OR', 'MAJ'])
        if op == 'AND':
            g = [(-1)**(z == (1 << n) - 1) for z in range(2**n)]
        elif op == 'OR':
            g = [(-1)**(z != 0) for z in range(2**n)]
        else:  # MAJ
            g = [(-1)**(sum((z >> i) & 1 for i in range(n)) >= n//2) for z in range(2**n)]
    return g

def spectral_norm(g):
    n = len(g)
    if n == 0:
        return 0.0
    # Walsh-Hadamard transform
    def wht(f):
        if len(f) == 1:
            return f
        half = len(f) // 2
        left = wht(f[:half])
        right = wht(f[half:])
        return [left[i] + right[i] for i in range(half)] + [left[i] - right[i] for i in range(half)]
    transformed = wht(g)
    return max(abs(x) for x in transformed) / (2**n)

def star_discrepancy(g):
    n = len(g)
    if n == 0:
        return 0.0
    # Compute c[a] = |P_g ∩ [0,a]_⊓|
    c = [0] * (2**n)
    for z in range(2**n):
        if g[z] == -1:
            a = z
            while a < 2**n:
                c[a] += 1
                a = (a + 1) | z
    # Compute D*_lat(g)
    total = sum(1 for x in g if x == -1)
    max_diff = 0.0
    for a in range(2**n):
        expected = total * (2**bin(a).count('1') - 1) / (2**n)
        diff = abs(c[a] - expected)
        if diff > max_diff:
            max_diff = diff
    return max_diff / (2**n)

def run_trial(seed):
    n_values = [6, 8, 10, 12, 14, 16, 18]
    n = random.choice(n_values)
    g = generate_g(n, seed)
    norm = spectral_norm(g)
    discrepancy = star_discrepancy(g)

    if norm == 0:
        return {
            "metric_name": "discrepancy_ratio",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

    lower_ratio = discrepancy / norm
    upper_ratio = discrepancy / (norm * math.log2(n + 1))

    conjecture_holds = (0.125 * norm <= discrepancy) and (discrepancy <= 8 * norm * math.log2(n + 1))
    counterexample = "" if conjecture_holds else f"n={n}, seed={seed}, norm={norm}, discrepancy={discrepancy}"

    return {
        "metric_name": "discrepancy_ratio",
        "metric_value": lower_ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["conjecture_holds"]]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_trials")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")