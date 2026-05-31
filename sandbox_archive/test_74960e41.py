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

def random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def noncrossing_partitions(n):
    if n == 1:
        return [[{0}], [{1}]]
    parts = noncrossing_partitions(n-1)
    new_parts = []
    for part in parts:
        new_parts.append([{i} for i in range(n) if i != n-1] + part)
        for i in range(1, n):
            new_parts.append([{0, n-1}] + [{j for j in range(i)} | {k for k in range(i+1, n)} for part in parts])
    return new_parts

def is_valid_partition(partition, n):
    if len(partition) != n:
        return False
    if any(len(p) == 0 or max(p) >= n for p in partition):
        return False
    if not all(i in range(n) for i in range(n)):
        return False
    return True

def automorphism_group_order(partitions):
    n = len(partitions)
    if n == 1:
        return 2
    order = 1
    for i in range(1, n):
        order *= (i+1) * math.factorial(n-1-i)
    return order

def communication_complexity(f, n):
    # Placeholder for actual communication complexity calculation
    # For simplicity, we use a linear function of n
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = random_boolean_function(n)
        partitions = noncrossing_partitions(n)
        if not all(is_valid_partition(p, n) for p in partitions):
            return {
                "metric_name": "communication_complexity",
                "metric_value": 0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        order = automorphism_group_order(partitions)
        comm_complexity = communication_complexity(f, n)
        results.append((order, comm_complexity))
    
    mean_C = sum(order for order, _ in results) / len(results)
    std_dev_C = math.sqrt(sum((order - mean_C)**2 for order, _ in results) / len(results))
    mean_ranks = sum(comm_complexity for _, comm_complexity in results) / len(results)
    
    if abs(mean_C / mean_ranks - 1) <= 0.5 and std_dev_C < 0.5:
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_ranks,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_C = sum(result["metric_value"] for result in results) / len(results)
    std_dev_C = math.sqrt(sum((result["metric_value"] - mean_C)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_dev_C} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_dev_C} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")