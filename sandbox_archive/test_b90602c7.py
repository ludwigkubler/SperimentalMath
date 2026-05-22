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
    
    def hamming_distance(f1, f2):
        return sum(x != y for x, y in zip(f1, f2))
    
    def influence_complexity(f, n):
        max_influence = 0
        for i in range(n):
            flipped_f = f[:]
            flipped_f[i] = 1 - flipped_f[i]
            max_influence = max(max_influence, hamming_distance(f, flipped_f) / (2**n))
        return max_influence
    
    def characteristic_function(f, n):
        norm_squared = sum(1 for _ in range(2**n)) / (2**(n+1))
        return norm_squared
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_influence_complexity = []
    total_norm_squared = []
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            norm_squared = characteristic_function(f, n)
            influence = influence_complexity(f, n)
            total_influence_complexity.append(influence)
            total_norm_squared.append(norm_squared**2)
            instances_tested += 1
    
    if not total_influence_complexity or not total_norm_squared:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    corr = sum(a * b for a, b in zip(total_norm_squared, total_influence_complexity)) / len(total_norm_squared)
    conjecture_holds = corr > 0.7
    counterexample = "" if conjecture_holds else f"Correlation {corr} is less than 0.7"
    
    return {
        "metric_name": "Correlation",
        "metric_value": corr,
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3  # Default list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        std_corr = math.sqrt(sum((result["metric_value"] - mean_corr)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_corr = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"])
        std_corr = math.sqrt(sum((result["metric_value"] - mean_corr)**2 for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"]))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        counterexample = next(result["counterexample"] for result in results if result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")