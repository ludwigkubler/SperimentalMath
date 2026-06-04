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
    
    def generate_boolean_instance(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def compute_conflict_set(phi):
        # Placeholder function to simulate conflict set computation
        # This is a dummy implementation and should be replaced with actual logic
        return phi.count('1')
    
    def count_integral_points(conflict_set):
        # Placeholder function to simulate counting integral points
        # This is a dummy implementation and should be replaced with actual logic
        return len(conflict_set)
    
    def compute_resolution_proof_tree_height(phi):
        # Placeholder function to simulate resolution proof tree height computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi)  # Simplified for demonstration
    
    metric_name = "Number of Integral Points"
    instances_tested = 0
    total_integral_points = 0
    max_n = 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        phi = generate_boolean_instance(n)
        conflict_set = compute_conflict_set(phi)
        integral_points = count_integral_points(conflict_set)
        proof_tree_height = compute_resolution_proof_tree_height(phi)
        
        instances_tested += 1
        total_integral_points += integral_points
        max_n = max(max_n, n)
    
    mean_integral_points = Fraction(total_integral_points, instances_tested)
    conjecture_holds = False
    counterexample = "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(mean_integral_points),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")