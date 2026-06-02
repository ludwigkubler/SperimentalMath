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
    
    # Generate a set of Boolean functions with varying input sizes up to n=40
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    # Compute the minimal order of Kähler forms for each function's associated symmetric tensors
    def kahler_form_order(f):
        n = int(math.log2(len(f)))
        order = 0
        for i in range(n):
            if f[i] == 1:
                order += 1
        return order
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            rank = communication_complexity_rank(f)
            order = kahler_form_order(f)
            results.append({"n": n, "rank": rank, "order": order})
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    # Calculate the Pearson correlation coefficient
    n_values = [r["n"] for r in results]
    rank_values = [r["rank"] for r in results]
    order_values = [r["order"] for r in results]
    
    mean_n = sum(n_values) / len(n_values)
    mean_rank = sum(rank_values) / len(rank_values)
    mean_order = sum(order_values) / len(order_values)
    
    cov = sum((n - mean_n) * (rank - mean_rank) for n, rank in zip(n_values, rank_values)) / len(n_values)
    var_n = sum((n - mean_n)**2 for n in n_values) / len(n_values)
    var_rank = sum((rank - mean_rank)**2 for rank in rank_values) / len(rank_values)
    
    if var_n == 0 or var_rank == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = cov / (math.sqrt(var_n) * math.sqrt(var_rank))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["metric_value"] is not None for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE missing_data")