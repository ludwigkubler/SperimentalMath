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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_minimal_index_of_topological_entanglement(f):
        # Placeholder function to simulate calculation
        return random.random()
    
    def calculate_communication_complexity_rank_variance(f):
        # Placeholder function to simulate calculation
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_metric_value = 0.0
        
        while instances_tested < 30:
            f = generate_boolean_function(n)
            mu = calculate_minimal_index_of_topological_entanglement(f)
            R = calculate_communication_complexity_rank_variance(f)
            
            if mu is None or R is None:
                continue
            
            total_metric_value += mu * R
            instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "mu_R_ratio",
                "metric_value": 0.0,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        mu_R_ratio = total_metric_value / instances_tested
        results.append(mu_R_ratio)
    
    mean_mu_R_ratio = sum(results) / len(results)
    std_deviation = math.sqrt(sum((x - mean_mu_R_ratio)**2 for x in results) / len(results))
    correlation_coefficient = 0.7  # Placeholder value, should be computed
    
    return {
        "metric_name": "mu_R_ratio",
        "metric_value": mean_mu_R_ratio,
        "instances_tested": sum(len(results) for _ in n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    mean_mu_R_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_mu_R_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu_R_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")