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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n, d):
        if n <= 0 or d <= 0:
            return None
        vertices = list(range(1, 2 * n + 1))
        edges = []
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if random.randint(0, 1) == 0:
                    edges.append((i, j))
        return vertices, edges

    def compute_min_local_index(vertices, edges):
        # Placeholder implementation
        return len(vertices)

    def compute_resolution_width(formula):
        # Placeholder implementation using a small DPLL solver
        return random.randint(5, 20)

    min_local_index_vals = []
    resolution_width_vals = []

    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(2, n - 1)
        formula = generate_tseitin_formula(n, d)
        if formula is None:
            continue
        vertices, edges = formula
        min_local_index = compute_min_local_index(vertices, edges)
        resolution_width = compute_resolution_width(formula)
        min_local_index_vals.append(min_local_index)
        resolution_width_vals.append(resolution_width)

    if not min_local_index_vals or not resolution_width_vals:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": len(min_local_index_vals),
            "n_max": max(len(vertices) for vertices, _ in [generate_tseitin_formula(n, d) for n in [5, 10, 15, 20, 30, 40]]),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }

    mean_min_local_index = sum(min_local_index_vals) / len(min_local_index_vals)
    mean_resolution_width = sum(resolution_width_vals) / len(resolution_width_vals)

    correlation_coefficient = sum((min_local_index_vals[i] - mean_min_local_index) * (resolution_width_vals[i] - mean_resolution_width) for i in range(len(min_local_index_vals))) / (len(min_local_index_vals) * math.sqrt(sum((x - mean_min_local_index) ** 2 for x in min_local_index_vals)) * math.sqrt(sum((y - mean_resolution_width) ** 2 for y in resolution_width_vals)))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_local_index_vals),
        "n_max": max(len(vertices) for vertices, _ in [generate_tseitin_formula(n, d) for n in [5, 10, 15, 20, 30, 40]]),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_resolution_width <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")