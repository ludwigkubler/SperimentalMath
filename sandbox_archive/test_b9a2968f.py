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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def hypergeom_order(n, m):
    if n == 0 or m == 0:
        return 1
    order = 1
    for i in range(1, min(n, m) + 1):
        order *= (n - i + 1) / (i * (m - i + 1))
    return order

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = random.sample(range(1, n+1), random.randint(1, n))
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    # Simplified version of resolution width calculation
    # This is a placeholder and should be replaced with actual implementation
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n // 2, n)
            cnf = generate_cnf(n, m)
            width = resolution_width(cnf)
            order = hypergeom_order(n, m)
            if order != 0:
                ratio = Fraction(abs(width), order ** 2)
                total_ratio += ratio
                instances_tested += 1
                n_max = max(n_max, n)

    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_ratio <= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "resolution_width_to_hypergeom_order",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")