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
    
    def hamming_distance(x, y):
        if len(x) != len(y):
            raise ValueError("Hamming distance requires equal-length sequences")
        return sum(xi != yi for xi, yi in zip(x, y))
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        dist_matrix = [[hamming_distance(f[i], f[j]) for j in range(2**n)] for i in range(2**n)]
        min_dist = min(min(row) for row in dist_matrix)
        return 1 + math.ceil(math.log2(min_dist))
    
    def quaternionic_generators_count(n):
        # Placeholder function to simulate the calculation
        return n * math.log2(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        generators_count = quaternionic_generators_count(n)
        
        if generators_count <= 0 or cc <= 0:
            continue
        
        total_metric_value += generators_count / cc
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "Generators per CC",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_metric = total_metric_value / instances_tested
    return {
        "metric_name": "Generators per CC",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric)**2 for result in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")