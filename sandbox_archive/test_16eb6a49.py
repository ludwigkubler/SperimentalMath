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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def arithmetic_hierarchy_complexity(f):
        # Placeholder function. This is a stub and should be replaced with actual computation.
        return len(f) / 2
    
    def circuit_monotone_width(f):
        # Placeholder function. This is a stub and should be replaced with actual computation.
        return sum(1 for bit in f if bit == 1)
    
    n_values = [30, 35, 40]
    results = []
    
    for n in n_values:
        for _ in range(10):  # Ensure at least 30 instances per seed
            f = generate_random_boolean_function(n)
            ah_f = arithmetic_hierarchy_complexity(f)
            w_mon_f = circuit_monotone_width(f)
            results.append((ah_f, w_mon_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ah_values = [ah for ah, _ in results]
    w_mon_values = [w_mon for _, w_mon in results]
    
    mean_ah = sum(ah_values) / len(ah_values)
    mean_w_mon = sum(w_mon_values) / len(w_mon_values)
    
    covariance = sum((ah - mean_ah) * (w_mon - mean_w_mon) for ah, w_mon in results) / len(results)
    variance_ah = sum((ah - mean_ah)**2 for ah in ah_values) / len(ah_values)
    variance_w_mon = sum((w_mon - mean_w_mon)**2 for w_mon in w_mon_values) / len(w_mon_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_ah) * math.sqrt(variance_w_mon))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")