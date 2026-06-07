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
    
    def generate_random_group(n):
        # Generate a random group of order n using a simple method
        elements = [i for i in range(1, n+1)]
        relations = []
        for _ in range(n-1):
            a, b = random.sample(elements, 2)
            if a < b:
                relations.append((a, b))
            else:
                relations.append((b, a))
        return elements, relations
    
    def adjoint_representation(group, n):
        # Generate the adjoint representation for a given group action on an n-bit input space
        adj_rep = []
        for g in group:
            rep = [[0]*n for _ in range(n)]
            for i in range(n):
                rep[i][g-1] = 1
            adj_rep.append(rep)
        return adj_rep
    
    def communication_complexity_rank(variance):
        # Calculate the communication complexity rank based on variance
        return math.sqrt(variance)
    
    def min_order_of_local_units(adj_rep):
        # Calculate the minimal order of local units in the adjoint representation
        orders = [sum(row) for row in adj_rep]
        return max(orders)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_min_order = 0
    total_variance = 0
    instances_tested = 0
    
    for n in n_values:
        group, relations = generate_random_group(n)
        adj_rep = adjoint_representation(group, n)
        variance = sum([sum(row) for row in adj_rep]) / (n * n)
        min_order = min_order_of_local_units(adj_rep)
        
        total_min_order += min_order
        total_variance += variance
        instances_tested += 1
    
    mean_min_order = total_min_order / len(n_values)
    mean_variance = total_variance / len(n_values)
    
    if mean_variance == 0:
        conjecture_holds = False
        counterexample = "variance_is_zero"
    else:
        ratio = mean_min_order / mean_variance
        conjecture_holds = 0.4 <= ratio <= 1.2
        counterexample = ""
    
    return {
        "metric_name": "Ratio of Min Order to Variance",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if 0.4 <= result["metric_value"] <= 1.2) / len(results)
    
    if all(0.4 <= result["metric_value"] <= 1.2 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(result["metric_value"] < 0.4 or result["metric_value"] > 1.2 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.4 or result["metric_value"] > 1.2)
        print(f"RESULT: FALSIFIED counterexample=\"ratio_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")