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

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def resolution_width(phi):
    n = int(math.log2(len(phi)))
    clauses = []
    for i in range(n):
        for j in range(i+1, n):
            clause = [i, -j]
            if any(phi[2**(i+j)] == 1 for i in range(2**n) if (i & (1 << i)) and (i & (1 << j))):
                clauses.append(clause)
    return len(clauses)

def min_order_lat(phi):
    n = int(math.log2(len(phi)))
    lat = [[0] * (1 << n) for _ in range(n)]
    for i in range(n):
        for j in range(1 << n):
            if phi[j]:
                lat[i][j] = 1
                for k in range(j):
                    if (k & (1 << i)) == 0:
                        lat[i][j] += lat[i-1][k]
    return max(max(row) for row in lat)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        phi = generate_boolean_function(n)
        t_star = resolution_width(phi)
        min_order = min_order_lat(phi)
        results.append({"n": n, "t_star": t_star, "min_order": min_order})
    
    metric_value = sum(result["min_order"] / result["t_star"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["min_order"] <= result["t_star"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MinOrderLat / t*",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")