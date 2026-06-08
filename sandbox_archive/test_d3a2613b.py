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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause.count(i) == 0 for i in [-1, 1]):
                clauses.append(clause)
        return clauses
    
    def ehrhart_polynomial_degree(clauses):
        # This is a placeholder function. Replace with actual Ehrhart polynomial degree calculation.
        return len(clauses)
    
    def clause_depth(clauses):
        max_depth = 0
        for clause in clauses:
            depth = sum(abs(x) for x in clause)
            if depth > max_depth:
                max_depth = depth
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_cnf(n)
        degree = ehrhart_polynomial_degree(clauses)
        depth = clause_depth(clauses)
        results.append({
            "n": n,
            "degree": degree,
            "depth": depth
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    
    if n_max < 16:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    expected_depths = [math.log(n, 2)**2 * result["degree"] for result in results]
    actual_depths = [result["depth"] for result in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    correlation = pearson_correlation(expected_depths, actual_depths)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample = "first_failing_seed" if first_failing_seed else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    elif all(result["metric_value"] is not None for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE metric_values_missing")