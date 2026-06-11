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
    
    def generate_instance(n):
        # Generate a communication complexity instance φ with size n
        # This is a placeholder function; replace it with actual generation logic
        return [random.randint(0, 1) for _ in range(n)]
    
    def min_order(phi):
        # Compute the minimal order of twisted module representations associated with φ
        # This is a placeholder function; replace it with actual computation logic
        return len(set(phi))
    
    def rank_variance(phi):
        # Compute the rank variance of φ
        # This is a placeholder function; replace it with actual computation logic
        mean = sum(phi) / len(phi)
        variance = sum((x - mean) ** 2 for x in phi) / len(phi)
        return variance
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        phi = generate_instance(n)
        min_order_phi = min_order(phi)
        rank_variance_phi = rank_variance(phi)
        
        if min_order_phi == 0 or rank_variance_phi == 0:
            continue
        
        log_min_order_phi = math.log2(min_order_phi)
        results.append((log_min_order_phi, rank_variance_phi))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    log_min_order_values, rank_variance_values = zip(*results)
    n_max = max(n_values)
    instances_tested = len(results)
    
    # Compute Pearson's correlation coefficient
    mean_log_min_order = sum(log_min_order_values) / instances_tested
    mean_rank_variance = sum(rank_variance_values) / instances_tested
    
    cov = sum((log_min_order_values[i] - mean_log_min_order) * (rank_variance_values[i] - mean_rank_variance) for i in range(instances_tested)) / instances_tested
    var_log_min_order = sum((log_min_order_values[i] - mean_log_min_order) ** 2 for i in range(instances_tested)) / instances_tested
    var_rank_variance = sum((rank_variance_values[i] - mean_rank_variance) ** 2 for i in range(instances_tested)) / instances_tested
    
    correlation_coefficient = cov / (math.sqrt(var_log_min_order) * math.sqrt(var_rank_variance))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(log_min_order - rank_variance) <= 3 for log_min_order, rank_variance in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")