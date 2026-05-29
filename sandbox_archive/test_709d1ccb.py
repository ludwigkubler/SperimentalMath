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
    
    # Generate a random Boolean function with n variables
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the minimal order of permutation representation under W_n
    def min_order(permutation):
        n = int(math.log2(len(permutation)))
        if n <= 0:
            return float('inf')
        cycle_lengths = []
        visited = [False] * len(permutation)
        for i in range(len(permutation)):
            if not visited[i]:
                cycle_length = 1
                j = permutation[i]
                while j != i:
                    visited[j] = True
                    j = permutation[j]
                    cycle_length += 1
                cycle_lengths.append(cycle_length)
        return math.prod([math.factorial(cl) for cl in cycle_lengths])
    
    # Calculate the tree-like resolution width
    def tree_like_resolution_width(boolean_function):
        n = int(math.log2(len(boolean_function)))
        if n <= 0:
            return float('inf')
        clauses = [boolean_function[i:i+n] for i in range(0, len(boolean_function), n)]
        width = 0
        for clause in clauses:
            width = max(width, sum(clause))
        return width
    
    # Main trial logic
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        boolean_function = generate_boolean_function(n)
        order = min_order(boolean_function)
        width = tree_like_resolution_width(boolean_function)
        results.append((order, width))
    
    # Compute correlation coefficient
    n = len(results)
    if n < 2:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": float('nan'),
            "instances_tested": n,
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    x_mean = sum(order for order, _ in results) / n
    y_mean = sum(width for _, width in results) / n
    x_var = sum((order - x_mean)**2 for order, _ in results) / n
    y_var = sum((width - y_mean)**2 for _, width in results) / n
    
    if x_var == 0 or y_var == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": float('nan'),
            "instances_tested": n,
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    cov = sum((order - x_mean) * (width - y_mean) for order, width in results) / n
    correlation_coefficient = cov / math.sqrt(x_var * y_var)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")