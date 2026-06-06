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
    
    def communication_complexity_rank(f):
        n = len(f)
        if n == 1:
            return 0
        rank = 0
        for i in range(1, n):
            if all(f[j] != f[j ^ (1 << i)] for j in range(2**(n-1))):
                rank += 1
        return rank
    
    def minimal_order_of_hecke_group(f):
        n = len(f)
        if n == 1:
            return 1
        order = 0
        for i in range(1, n):
            if all(f[j] != f[j ^ (1 << i)] for j in range(2**(n-1))):
                order += 1
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_order = 0
    total_rank = 0
    
    for n in n_values:
        for _ in range(50):
            f = generate_boolean_function(n)
            rank = communication_complexity_rank(f)
            order = minimal_order_of_hecke_group(f)
            instances_tested += 1
            total_order += order
            total_rank += rank
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_order = total_order / instances_tested
    mean_rank = total_rank / instances_tested
    
    # Pearson correlation coefficient calculation
    covariance = sum((order - mean_order) * (rank - mean_rank) for order, rank in zip(order_list, rank_list))
    variance_order = sum((order - mean_order)**2 for order in order_list)
    variance_rank = sum((rank - mean_rank)**2 for rank in rank_list)
    
    if variance_order == 0 or variance_rank == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_variance"
        }
    
    pearson_correlation = covariance / (math.sqrt(variance_order) * math.sqrt(variance_rank))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(pearson_correlation) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")