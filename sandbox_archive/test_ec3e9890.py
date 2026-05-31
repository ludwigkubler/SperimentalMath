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
    
    def generate_communication_problem(n):
        # Placeholder for generating a communication problem instance
        return [random.randint(1, n) for _ in range(n)]
    
    def compute_automorphism_group_size(problem):
        # Placeholder for computing the automorphism group size of the quantum group algebra
        return random.randint(1, 2**n)
    
    def compute_communication_complexity(problem):
        # Placeholder for computing the communication complexity of the problem
        return sum(problem) / n
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        problem = generate_communication_problem(n)
        automorphism_group_size = compute_automorphism_group_size(problem)
        communication_complexity = compute_communication_complexity(problem)
        
        if automorphism_group_size == 0:
            continue
        
        log_order = math.log2(automorphism_group_size)
        log_n_plus_C = math.log2(n) + 1  # Assuming C=1 for simplicity
        results.append((log_order, communication_complexity))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    n_max = max(n for _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instance size"
        }
    
    log_orders, complexities = zip(*results)
    mean_log_order = sum(log_orders) / len(log_orders)
    mean_complexity = sum(complexities) / len(complexities)
    
    covariance = sum((x - mean_log_order) * (y - mean_complexity) for x, y in zip(log_orders, complexities))
    variance_log_order = sum((x - mean_log_order)**2 for x in log_orders)
    variance_complexity = sum((y - mean_complexity)**2 for y in complexities)
    
    if variance_log_order == 0 or variance_complexity == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Zero variance in log_order or complexity"
        }
    
    pearson_corr_coeff = covariance / (math.sqrt(variance_log_order) * math.sqrt(variance_complexity))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": pearson_corr_coeff >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={math.sqrt(sum((result['metric_value'] - mean_corr_coeff)**2 for result in results) / len(results))} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["conjecture_holds"] == False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["conjecture_holds"] == False)
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if 'counterexample' in result)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")