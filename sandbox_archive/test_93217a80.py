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

def xor(a, b):
    return a ^ b

def hamming_distance(x, y):
    return bin(x ^ y).count('1')

def compute_dt(f, n):
    if n == 0:
        return 0
    dt = float('inf')
    for i in range(n):
        f0 = [f(x) for x in range(2**n) if (x >> i) & 1 == 0]
        f1 = [f(x) for x in range(2**n) if (x >> i) & 1 == 1]
        if f0 == f1:
            dt = min(dt, compute_dt(lambda x: f(x | (1 << i)), n - 1))
        else:
            dt = min(dt, 1 + max(compute_dt(lambda x: f(x | (1 << i)), n - 1),
                                 compute_dt(lambda x: f(x & ~(1 << i)), n - 1)))
    return dt

def compute_delta_bar(M, d):
    max_delta = 0
    n = len(M)
    for a, b, c, d in itertools.combinations(range(n), 4):
        S1 = hamming_distance(M[a], M[b]) + hamming_distance(M[c], M[d])
        S2 = hamming_distance(M[a], M[c]) + hamming_distance(M[b], M[d])
        S3 = hamming_distance(M[a], M[d]) + hamming_distance(M[b], M[c])
        S_sorted = sorted([S1, S2, S3], reverse=True)
        delta = (S_sorted[0] - S_sorted[1]) / 2
        if delta > max_delta:
            max_delta = delta
    diam = max(hamming_distance(M[i], M[j]) for i, j in itertools.combinations(range(n), 2))
    if diam == 0:
        return 0
    return max_delta / diam

def run_trial(seed):
    random.seed(seed)
    n_values = [3, 4, 5]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        # Generate a random Boolean function
        f = [random.randint(0, 1) for _ in range(2**n)]
        # Ensure the function is non-constant
        if len(set(f)) == 1:
            continue
        # Compute the decision tree depth
        dt = compute_dt(lambda x: f[x], n)
        # Build the lifted matrix M
        M = [[f[xor(x, y)] for y in range(2**n)] for x in range(2**n)]
        # Compute delta_bar
        delta_bar = compute_delta_bar(M, n)
        # Check the conjecture
        if delta_bar > 1 - dt / (n + 1):
            conjecture_holds = False
            counterexample = f"delta_bar={delta_bar} > 1 - dt/(n+1)={1 - dt/(n+1)} for n={n}, dt={dt}"
            break
        metric_values.append(delta_bar)
        instances_tested += 1

    if not metric_values:
        return {
            "metric_name": "delta_bar",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances tested"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "delta_bar",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_all = True
    counterexample = ""
    first_failing_seed = None

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]
            first_failing_seed = seed
            break

    if not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={first_failing_seed}')
    else:
        mean_metric = sum(metric_values) / len(metric_values)
        std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction=1.0')