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
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank = sum(f[i] != f[j] for i in range(len(f)) for j in range(i+1, len(f))) / (len(f) * (len(f) - 1) / 2)
        return rank
    
    def non_arithmetic_L_function(rank_variance):
        # This is a placeholder function. Replace with actual implementation.
        return abs(rank_variance)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank_variance = communication_complexity_rank_variance(f)
        L_order = non_arithmetic_L_function(rank_variance)
        
        if L_order <= 0 or rank_variance <= 0:
            continue
        
        results.append({
            "n": n,
            "L_order": L_order,
            "rank_variance": rank_variance
        })
    
    if not results:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    n_max = max(result["n"] for result in results)
    L_orders = [result["L_order"] for result in results]
    rank_variances = [result["rank_variance"] for result in results]
    
    mean_L_order = sum(L_orders) / len(L_orders)
    std_L_order = math.sqrt(sum((x - mean_L_order) ** 2 for x in L_orders) / len(L_orders))
    
    correlation_coefficient = sum((L_orders[i] - mean_L_order) * (rank_variances[i] - mean(rank_variances)) for i in range(len(L_orders))) / (len(L_orders) * std_L_order * math.sqrt(sum((x - mean(rank_variances)) ** 2 for x in rank_variances)))
    
    return {
        "metric_name": "minimal_order",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient - n) < 2 * n / 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_instances")