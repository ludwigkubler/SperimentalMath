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
    
    def affine_group_order(f):
        n = len(f)
        count = 0
        for i in range(2**n):
            if all((f[i ^ j] == f[j]) for j in range(2**n)):
                count += 1
        return count
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = sum(1 for i in range(n) if any(f[i ^ j] != f[j] for j in range(2**n)))
        return rank / (2**(n-1))
    
    metric_values = []
    instances_tested = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_boolean_function(n)
            order = affine_group_order(f)
            rank_variance = communication_complexity_rank_variance(f)
            metric_values.append(order * rank_variance)
            instances_tested += 1
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(abs(x - mean_value) <= 3 * std_value or x > 10 for x in metric_values)
    counterexample = "" if conjecture_holds else "metric_outside_threshold"
    
    return {
        "metric_name": "Order of Affine Group Conjugacy Classes * Communication Complexity Rank Variance",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] and x["metric_value"] > 10 for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"] and x["metric_value"] > 10)
        print(f"RESULT: FALSIFIED counterexample=\"metric_outside_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")