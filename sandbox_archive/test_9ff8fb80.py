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
    
    def calculate_invariant_generators(f):
        # Placeholder function to simulate invariant generator calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        invariant_counts = []
        
        while instances_tested < 30:
            f = generate_boolean_function(n)
            invariant_count = calculate_invariant_generators(f)
            invariant_counts.append(invariant_count)
            instances_tested += 1
        
        metric_value = sum(invariant_counts) / len(invariant_counts)
        n_max = max(n_values)
        
        conjecture_holds = False
        counterexample = ""
        
        if instances_tested >= 30:
            expected_mean = math.sqrt(n) * math.log(n)
            correlation_coefficient = calculate_correlation(invariant_counts, [math.sqrt(x) * math.log(x) for x in n_values])
            
            if correlation_coefficient >= 0.8:
                conjecture_holds = True
            elif correlation_coefficient < 0.5:
                counterexample = "correlation_coefficient_too_low"
        
        results.append({
            "metric_name": "invariant_generator_count",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0]
    }

def calculate_correlation(x, y):
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
    std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / len(x))
    std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / len(y))
    return cov / (std_x * std_y)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")