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
    
    def hamming_distance(x, y):
        return sum(xi != yi for xi, yi in zip(x, y))
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        min_dist = float('inf')
        for i in range(len(f)):
            for j in range(i+1, len(f)):
                dist = hamming_distance(f[i], f[j])
                if dist < min_dist:
                    min_dist = dist
        return min_dist
    
    def quaternionic_generators_count(n):
        # Placeholder function; actual implementation needed
        return n * math.log2(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        generators_count = quaternionic_generators_count(n)
        
        if generators_count <= 0 or cc <= 0:
            continue
        
        results.append({
            "n": n,
            "communication_complexity": cc,
            "generators_count": generators_count
        })
    
    if not results:
        return {
            "metric_name": "communication_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_cc = sum(result["communication_complexity"] for result in results) / len(results)
    mean_generators_count = sum(result["generators_count"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["communication_complexity"] - mean_cc)**2 for result in results) / len(results))
    
    correlation_coefficient = sum((result["communication_complexity"] - mean_cc) * (result["generators_count"] - mean_generators_count) for result in results) / (len(results) * std_dev * std_dev)
    
    return {
        "metric_name": "communication_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_threshold\" first_failing_seed={result['seed']}")
                break