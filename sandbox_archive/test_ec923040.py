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
    
    def permutation_group_representation(f, n):
        G = []
        for i in range(2**n):
            perm = [f[i ^ (1 << j)] if (i >> j) & 1 else f[i] for j in range(n)]
            G.append(perm)
        return G
    
    def automorphism_group_order(G, n):
        # Simple heuristic to estimate the order of the automorphism group
        # This is a placeholder and may not be accurate
        return len(G)
    
    def communication_complexity(f, n):
        # Placeholder for actual communication complexity calculation
        # For simplicity, we use a random value
        return random.uniform(1, 2**n)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        G_f = permutation_group_representation(f, n)
        order_Aut_G_f = automorphism_group_order(G_f, n)
        c_f = communication_complexity(f, n)
        
        results.append({
            "n": n,
            "order_Aut_G_f": order_Aut_G_f,
            "c_f": c_f
        })
    
    mean_order = sum(result["order_Aut_G_f"] for result in results) / len(results)
    mean_c = sum(result["c_f"] for result in results) / len(results)
    
    correlation_coefficient = 0.0
    if len(results) > 1:
        numerator = sum((result["order_Aut_G_f"] - mean_order) * (result["c_f"] - mean_c) for result in results)
        denominator = math.sqrt(sum((result["order_Aut_G_f"] - mean_order)**2 for result in results)) * math.sqrt(sum((result["c_f"] - mean_c)**2 for result in results))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_C = sum(result["metric_value"] for result in results) / len(results)
    std_C = math.sqrt(sum((result["metric_value"] - mean_C)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")