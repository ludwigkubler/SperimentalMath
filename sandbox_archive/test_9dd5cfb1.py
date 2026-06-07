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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def box_counting_dimension(data, min_size=1, max_size=None):
        if max_size is None:
            max_size = len(data) // 2
        dimensions = []
        for size in range(min_size, max_size + 1):
            count = sum(1 for x in data if abs(x) >= size)
            dimensions.append((size, math.log(count)))
        slope, _ = linear_regression(dimensions)
        return -slope
    
    def linear_regression(points):
        n = len(points)
        x_sum = sum(point[0] for point in points)
        y_sum = sum(point[1] for point in points)
        xy_sum = sum(x * y for x, y in points)
        xx_sum = sum(x ** 2 for x, _ in points)
        slope = (n * xy_sum - x_sum * y_sum) / (n * xx_sum - x_sum ** 2)
        intercept = (y_sum - slope * x_sum) / n
        return slope, intercept
    
    def dpll(clauses):
        def solve(model):
            if not clauses:
                return True
            literal = next(l for l in range(1, max(abs(c) for c in sum(clauses, [])) + 1) if l not in model and -l not in model)
            for value in [True, False]:
                new_model = model.copy()
                new_model[literal] = value
                if solve(new_model):
                    return True
                new_model[-literal] = not value
                if solve(new_model):
                    return True
            return False
        
        return solve({})
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        fractal_dimension = box_counting_dimension(cnf)
        resolution_width = dpll(cnf)
        
        if fractal_dimension is None or resolution_width is None:
            return {
                "metric_name": "correlation",
                "metric_value": 0.0,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((fractal_dimension, resolution_width))
    
    correlation_coefficient = linear_regression(results)[0]
    mean_absolute_difference = sum(abs(d - w) for d, w in results) / len(results)
    max_value = max(max(d, w) for d, w in results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_absolute_difference / max_value <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")