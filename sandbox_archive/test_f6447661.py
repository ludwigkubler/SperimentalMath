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
    
    def generate_formula(n):
        return ' '.join(random.choice(['A', 'B', 'C']) for _ in range(n))
    
    def count_clauses(formula):
        return formula.count(' ')
    
    def coherence_length(formula):
        # Placeholder implementation of coherence length calculation
        # This is a dummy function and should be replaced with actual logic
        return len(formula)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        formula = generate_formula(random.randint(5, 40))
        c_phi = coherence_length(formula)
        k_phi = count_clauses(formula)
        results.append((c_phi, k_phi))
    
    if not results:
        return {
            "metric_name": "coherence_length_vs_clause_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    c_phi_values = [c for c, _ in results]
    k_phi_values = [k for _, k in results]
    
    mean_c_phi = sum(c_phi_values) / len(c_phi_values)
    mean_k_phi = sum(k_phi_values) / len(k_phi_values)
    
    n_max = max(len(formula.split()) for formula, _ in results)
    
    if n_max < 16:
        return {
            "metric_name": "coherence_length_vs_clause_complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    # Placeholder for linear regression
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept
    
    slope, _ = linear_regression(k_phi_values, c_phi_values)
    
    return {
        "metric_name": "coherence_length_vs_clause_complexity",
        "metric_value": slope,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": slope >= 0.8 and abs(slope - 1) <= 3 / math.sqrt(len(results)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_slope = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_slope = math.sqrt(sum((result["metric_value"] - mean_slope) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slope_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")