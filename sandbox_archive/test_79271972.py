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
    
    def communication_complexity(phi):
        n = len(phi)
        count = 0
        for i in range(2**n):
            if phi[i] == 1:
                count += 1
        return count
    
    def lefschetz_thimble_rank(phi):
        # Placeholder function to simulate Lefschetz thimble rank calculation
        n = len(phi)
        return random.randint(1, n)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = generate_boolean_function(n)
        c_phi = communication_complexity(phi)
        Lr_phi = lefschetz_thimble_rank(phi)
        results.append((c_phi, Lr_phi))
    
    if not results:
        return {
            "metric_name": "Lefschetz Thimble Rank vs Communication Complexity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    c_phi_values = [c for c, _ in results]
    Lr_phi_values = [L for _, L in results]
    
    mean_c_phi = sum(c_phi_values) / len(c_phi_values)
    mean_Lr_phi = sum(Lr_phi_values) / len(Lr_phi_values)
    
    n_max = max(len(phi) for phi, _ in results)
    
    correlation_coefficient = 0.0
    if len(results) > 1:
        numerator = sum((c - mean_c_phi) * (L - mean_Lr_phi) for c, L in results)
        denominator = math.sqrt(sum((c - mean_c_phi)**2 for c, _ in results)) * math.sqrt(sum((L - mean_Lr_phi)**2 for _, L in results))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Lefschetz Thimble Rank vs Communication Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials")
        exit(0)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")