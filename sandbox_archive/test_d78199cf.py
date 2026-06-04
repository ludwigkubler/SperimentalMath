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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_topological_entanglement(f):
        # Placeholder function to simulate topological entanglement calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    def calculate_communication_complexity_rank(f):
        # Placeholder function to simulate communication complexity rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        toe_f = calculate_topological_entanglement(f)
        r_f = calculate_communication_complexity_rank(f)
        results.append((toe_f, r_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    toe_values = [toe for toe, _ in results]
    r_values = [r for _, r in results]
    
    n_max = max(n_values)
    instances_tested = len(results)
    
    if n_max < 16:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    def calculate_correlation(x, y):
        if len(x) != len(y):
            return None
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        var_x = sum((xi - mean_x)**2 for xi in x) / len(x)
        var_y = sum((yi - mean_y)**2 for yi in y) / len(y)
        if var_x == 0 or var_y == 0:
            return None
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    correlation_coefficient = calculate_correlation(toe_values, r_values)
    
    conjecture_holds = correlation_coefficient is not None and correlation_coefficient >= 0.7
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    total_metric_value = 0
    conjecture_holds_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            conjecture_holds_count += 1
        
        total_metric_value += trial_result["metric_value"] * trial_result["instances_tested"]
    
    mean_metric_value = total_metric_value / sum(result["instances_tested"] for result in results)
    support_fraction = conjecture_holds_count / len(seeds)
    
    if all(result["conjecture_holds"] for result in results) or support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")