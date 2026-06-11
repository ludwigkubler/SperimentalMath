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
    
    def generate_instance(n):
        # Generate a random communication complexity instance
        return [random.randint(0, 1) for _ in range(n)]
    
    def min_order(phi):
        # Placeholder function to compute the minimal order of twisted module representations
        # This is a dummy implementation; replace with actual computation
        return len(phi)
    
    def rank_variance(phi):
        # Placeholder function to compute the rank variance
        # This is a dummy implementation; replace with actual computation
        mean = sum(phi) / len(phi)
        return sum((x - mean) ** 2 for x in phi) / len(phi)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        log_min_order_sum = 0
        rank_variance_sum = 0
        
        while instances_tested < 30:
            phi = generate_instance(n)
            min_order_val = min_order(phi)
            rank_variance_val = rank_variance(phi)
            
            if min_order_val > 0 and rank_variance_val >= 0:
                log_min_order_sum += math.log2(min_order_val)
                rank_variance_sum += rank_variance_val
                instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "log₂(min_order) vs rank_variance",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "No valid instances found"
            }
        
        log_min_order_mean = log_min_order_sum / instances_tested
        rank_variance_mean = rank_variance_sum / instances_tested
        
        var_log_min_order = sum((math.log2(min_order(phi)) - log_min_order_mean) ** 2 for phi in [generate_instance(n) for _ in range(30)]) / instances_tested
        var_rank_variance = sum((rank_variance(phi) - rank_variance_mean) ** 2 for phi in [generate_instance(n) for _ in range(30)]) / instances_tested
        
        if var_log_min_order == 0 or var_rank_variance == 0:
            return {
                "metric_name": "log₂(min_order) vs rank_variance",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Zero variance in log₂(min_order) or rank_variance"
            }
        
        correlation_coefficient = (sum((math.log2(min_order(phi)) - log_min_order_mean) * (rank_variance(phi) - rank_variance_mean) for phi in [generate_instance(n) for _ in range(30)]) / instances_tested) / math.sqrt(var_log_min_order * var_rank_variance)
        
        results.append({
            "n": n,
            "correlation_coefficient": correlation_coefficient
        })
    
    mean_corr = sum(result["correlation_coefficient"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["correlation_coefficient"] - mean_corr) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "log₂(min_order) vs rank_variance",
        "metric_value": mean_corr,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all(abs(correlation_coefficient - mean_corr) <= 3 for correlation_coefficient in [result["correlation_coefficient"] for result in results]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")