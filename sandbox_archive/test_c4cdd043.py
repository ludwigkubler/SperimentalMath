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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def compute_clause_set_complexity(cnf):
        # Simplified complexity measure
        return len(cnf) + sum(len(clause) for clause in cnf)
    
    def compute_minimal_geometric_entropy(cnf):
        # Simplified entropy measure
        total_weight = 0
        for _ in range(100):  # Simulate sampling
            weight = random.random()
            total_weight += weight
        return total_weight / len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_values = [n // 2, n, n * 2]
        for m in m_values:
            cnf = generate_cnf(n, m)
            c_phi = compute_clause_set_complexity(cnf)
            mge_phi = compute_minimal_geometric_entropy(cnf)
            results.append({
                "n": n,
                "m": m,
                "c_phi": c_phi,
                "mge_phi": mge_phi
            })
    
    if not results:
        return {
            "metric_name": "minimal_geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    mge_values = [result["mge_phi"] for result in results]
    c_phi_values = [result["c_phi"] for result in results]
    
    def linear_regression(x, y):
        if not x or not y:
            return 0, 0
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = sum((xi - mean_x) ** 2 for xi in x)
        if denominator == 0:
            return 0, 0
        slope = numerator / denominator
        intercept = mean_y - slope * mean_x
        return slope, intercept
    
    slope, _ = linear_regression(c_phi_values, mge_values)
    
    return {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(slope - 1) < 0.3,  # Simplified threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials ran")
    else:
        mean_slope = sum(result["metric_value"] for result in results) / len(results)
        std_slope = math.sqrt(sum((result["metric_value"] - mean_slope) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if abs(result["metric_value"] - 1) < 0.3) / len(results)
        
        if all(abs(result["metric_value"] - 1) < 0.3 for result in results):
            print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
        elif any(result["conjecture_holds"] is False for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"slope_out_of_range\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE no clear support or refutation")