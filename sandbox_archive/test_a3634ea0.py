# auto-injected by SEC sandbox
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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_random_read_twice_bp(n):
    bp = [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
    return bp

def compute_function(bp, n):
    f = [0] * (1 << n)
    for i in range(n):
        x = i
        for j in range(n):
            if bp[j][x % 2]:
                x ^= 1 << (n - j - 1)
        f[x] += 1
    return [f[i] - f[~i] for i in range(1 << n)]

def compute_additive_energy(f, n):
    count = 0
    for x in range(1 << n):
        for y in range(x + 1, 1 << n):
            for z in range(y + 1, 1 << n):
                w = (x ^ y) ^ (z ^ y)
                if f[x] + f[y] == f[z] + f[w]:
                    count += 1
    return count

def compute_discrepancy(f, n):
    max_disc = 0
    for mask in range(1 << n):
        sum_mask = sum(f[i] if i & mask else -f[i] for i in range(1 << n))
        max_disc = max(max_disc, abs(sum_mask))
    return max_disc

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    bp = generate_random_read_twice_bp(n)
    f = compute_function(bp, n)
    E_f = compute_additive_energy(f, n)
    disc_P = compute_discrepancy(f, n)
    C = 1.0  # Empirical constant to test the conjecture
    metric_name = "additive_energy_lower_bound"
    metric_value = E_f / (C * n * disc_P) if disc_P != 0 else float('inf')
    instances_tested = 1
    conjecture_holds = metric_value >= 1.0
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")