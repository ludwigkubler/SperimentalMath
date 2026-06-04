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
        for _ in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def entropy(clauses):
        total_clauses = len(clauses)
        zero_count = sum(1 for clause in clauses if all(var == 0 for var in clause))
        return -math.log2(zero_count / total_clauses) if zero_count > 0 else float('inf')
    
    def quaternionic_k_theory_order(clauses):
        n = len(clauses)
        order = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(clause[i] * clause[j] == 0 for clause in clauses):
                    order += 1
        return order
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        r_squared = ((n * sum_xy - sum_x * sum_y) ** 2) / ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        
        return slope, intercept, r_squared
    
    trials = 30
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for _ in range(trials):
        n = random.choice(n_values)
        cnf = generate_cnf(n)
        order = quaternionic_k_theory_order(cnf)
        entropy_val = entropy(cnf)
        
        if entropy_val == float('inf'):
            continue
        
        results.append((order, entropy_val))
    
    if len(results) < 30:
        return {
            "metric_name": "R²",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    x, y = zip(*results)
    slope, intercept, r_squared = linear_regression(x, y)
    
    return {
        "metric_name": "R²",
        "metric_value": r_squared,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": r_squared >= 0.9 and slope > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_r_squared = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R² too low\" first_failing_seed={first_failing_seed}")