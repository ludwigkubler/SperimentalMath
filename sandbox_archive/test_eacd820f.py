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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f, n):
        if len(f) != 2**n:
            raise ValueError("Function length must match the number of elements in the matrix representation")
        return [[f[i * (1 << (n - j)) + j] for j in range(n)] for i in range(2**(n-1))]
    
    def dual_vector(matrix):
        n = len(matrix)
        dual = [0] * n
        for i in range(n):
            for j in range(n):
                if matrix[i][j]:
                    dual[j] += 1 << (n - i - 1)
        return dual
    
    def minimal_order(dual):
        gcd = 0
        for x in dual:
            while x > 0:
                y = gcd % x
                gcd, x = x, y
        return gcd
    
    def communication_complexity_rank_variance(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] for j in range(n)):
                rank += 1
        return (rank - 1) / (n - 1) if n > 1 else 0
    
    def generate_random_seeds(num_seeds):
        return [random.randint(2, 10**9) for _ in range(num_seeds)]
    
    num_instances = 30
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(num_instances):
            f = generate_boolean_function(n)
            matrix = matrix_representation(f, n)
            dual = dual_vector(matrix)
            min_order = minimal_order(dual)
            rank_variance = communication_complexity_rank_variance(matrix)
            results.append((min_order, rank_variance))
    
    if not results:
        return {
            "metric_name": "minimal_order_vs_rank_variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    min_orders = [r[0] for r in results]
    rank_variances = [r[1] for r in results]
    correlation_coefficient = sum((min_orders[i] - sum(min_orders) / len(min_orders)) * (rank_variances[i] - sum(rank_variances) / len(rank_variances)) for i in range(len(results))) / (len(results) * math.sqrt(sum((x - sum(min_orders) / len(min_orders))**2 for x in min_orders) * sum((y - sum(rank_variances) / len(rank_variances))**2 for y in rank_variances)))
    
    return {
        "metric_name": "minimal_order_vs_rank_variance",
        "metric_value": correlation_coefficient,
        "instances_tested": num_instances * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = generate_random_seeds(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")