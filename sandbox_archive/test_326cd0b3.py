# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_boolean_function(n):
    return {i: random.randint(0, 1) for i in range(2**n)}

def evaluate_quadratic_form(f, x_k):
    n = int(math.log2(len(x_k)))
    Q = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            Q[i][j] = f[(i << (n - 1)) | (j << (n - 2))]
            if i != j:
                Q[j][i] = Q[i][j]
    return sum(Q[i][j] * x_k[i] * x_k[j] for i in range(n) for j in range(i, n))

def minimal_quadratic_defect(f):
    n = int(math.log2(len(f)))
    min_defect = float('inf')
    for k in range(1, len(f)):
        for x_k in combinations(range(2**n), k):
            defect = abs(evaluate_quadratic_form(f, x_k) - 1) / len(x_k)
            if defect < min_defect:
                min_defect = defect
    return min_defect

def communication_complexity(f):
    n = int(math.log2(len(f)))
    max_comm_cost = float('-inf')
    for k in range(1, len(f)):
        for x_k in combinations(range(2**n), k):
            comm_cost = sum(abs(f[i] - f[j]) for i, j in combinations(x_k, 2))
            if comm_cost > max_comm_cost:
                max_comm_cost = comm_cost
    return max_comm_cost

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        cc = communication_complexity(f)
        min_defect = minimal_quadratic_defect(f)
        
        if min_defect == float('inf'):
            return {
                "metric_name": "minimal_quadratic_defect",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append({
            "n": n,
            "cc": cc,
            "min_defect": min_defect
        })
    
    mean_cc = sum(result["cc"] for result in results) / len(results)
    mean_min_defect = sum(result["min_defect"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["cc"] - mean_cc)**2 + (result["min_defect"] - mean_min_defect)**2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if abs(result["cc"] - result["min_defect"]) <= 0.1 * max(result["cc"], result["min_defect"])) / len(results)
    
    return {
        "metric_name": "minimal_quadratic_defect",
        "metric_value": mean_min_defect,
        "instances_tested": sum(1 for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")