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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_circuit(n, d):
        if (n * d) % 2 != 0:
            return None
        circuit = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(d):
                k = random.randint(0, n - 1)
                while circuit[i][k] is not None or k == i:
                    k = random.randint(0, n - 1)
                circuit[i][k] = (i, k)
        return circuit
    
    def compute_monotone_width(circuit):
        n = len(circuit)
        width = [0] * n
        for i in range(n):
            for j in range(n):
                if circuit[i][j] is not None:
                    a, b = circuit[i][j]
                    width[a] += 1
                    width[b] += 1
        return max(width)
    
    def compute_automorphism_group(circuit):
        n = len(circuit)
        generators = []
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i][j] is not None:
                    a, b = circuit[i][j]
                    if (a, b) == (i, j):
                        generators.append((i, j))
        return len(generators)
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    G_values = []
    sqrt_wm_values = []
    
    for n in n_values:
        circuit = generate_d_regular_circuit(n, 2)
        if circuit is None:
            continue
        wm = compute_monotone_width(circuit)
        G = compute_automorphism_group(circuit)
        G_values.append(G)
        sqrt_wm_values.append(math.sqrt(wm))
    
    if len(G_values) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(G_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    r = pearson_correlation(G_values, sqrt_wm_values)
    p_value = 2 * (1 - math.erf(abs(r) / math.sqrt(2 * len(G_values) - 2)))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": r,
        "instances_tested": len(G_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(r) >= 0.7 and p_value > 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation too low' first_failing_seed={first_failing_seed}")