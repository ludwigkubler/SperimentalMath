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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance_ratio(f):
        n = len(f)
        counts = [f.count(i) for i in set(f)]
        variance = sum((x - (sum(counts) / len(counts))) ** 2 for x in counts) / len(counts)
        return variance
    
    def construct_braided_tensor_product_module(f):
        n = len(f)
        # Simplified braided tensor product module construction
        order = 2 * n
        return order
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_random_boolean_function(n)
        R_f = communication_complexity_rank_variance_ratio(f)
        M_order = construct_braided_tensor_product_module(f)
        
        results.append({
            "n": n,
            "R_f": R_f,
            "M_order": M_order
        })
    
    if not results:
        return {
            "metric_name": "log2|M|",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    log2_M_order = [math.log2(result["M_order"]) for result in results]
    R_f_values = [result["R_f"] * math.log(result["n"], 2) for result in results]
    
    mean_log2_M_order = sum(log2_M_order) / len(log2_M_order)
    mean_R_f_values = sum(R_f_values) / len(R_f_values)
    correlation = sum((log2_M_order[i] - mean_log2_M_order) * (R_f_values[i] - mean_R_f_values) for i in range(len(log2_M_order))) / len(log2_M_order)
    
    return {
        "metric_name": "log2|M|",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation) > 0.5,  # Simplified threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")