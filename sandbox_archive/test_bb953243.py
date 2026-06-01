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
    
    def generate_cnf(m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, m) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(2, 5))]
            cnf.append(clause)
        return cnf
    
    def compute_mri(cnf):
        # Placeholder for computing the minimal local ring index
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    def compute_frege_depth(cnf):
        # Placeholder for computing the Frege proof depth
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(10, 50)
    
    mri_values = []
    frege_depths = []
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        m = random.randint(5, 40)
        cnf = generate_cnf(m)
        mri = compute_mri(cnf)
        frege_depth = compute_frege_depth(cnf)
        mri_values.append(mri)
        frege_depths.append(frege_depth)
    
    if not mri_values or not frege_depths:
        return {
            "metric_name": "mri_vs_frege",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    n_max = max(len(cnf) for cnf in frege_depths)
    if n_max < 16:
        return {
            "metric_name": "mri_vs_frege",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_too_small"
        }
    
    correlation = compute_correlation(mri_values, frege_depths)
    return {
        "metric_name": "mri_vs_frege",
        "metric_value": correlation,
        "instances_tested": len(mri_values),
        "n_max": n_max,
        "conjecture_holds": abs(correlation) > 0.1,  # Threshold for significance
        "counterexample": ""
    }

def compute_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    var_x = sum((xi - mean_x) ** 2 for xi in x) / n
    var_y = sum((yi - mean_y) ** 2 for yi in y) / n
    
    if var_x == 0 or var_y == 0:
        return 0
    
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"])) / sum(1 for r in results if r["conjecture_holds"])
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")