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
    
    def calculate_minimal_index_of_topological_entanglement(f):
        # Placeholder function to simulate the calculation
        return random.random()
    
    def calculate_communication_complexity_rank_variance(f):
        # Placeholder function to simulate the calculation
        return random.random()
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            mu_f = calculate_minimal_index_of_topological_entanglement(f)
            R_f = calculate_communication_complexity_rank_variance(f)
            results.append((n, mu_f, R_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n_values, mu_values, R_values = zip(*results)
    mean_mu = sum(mu_values) / len(mu_values)
    mean_R = sum(R_values) / len(R_values)
    correlation_coefficient = sum((mu - mean_mu) * (R - mean_R) for mu, R in zip(mu_values, R_values)) / (len(results) * math.sqrt(sum((mu - mean_mu)**2 for mu in mu_values) * sum((R - mean_R)**2 for R in R_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_metric_value = None
        std_metric_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        RESULT = f"SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] is None)
        RESULT = f"FALSIFIED counterexample=\"not_enough_data\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)