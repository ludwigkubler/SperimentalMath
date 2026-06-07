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
    
    def matrix_representation(f, n):
        return [[f[i * (1 << (n - j)) + j] for j in range(n)] for i in range(2**(n-1))]
    
    def dual_vector(matrix):
        m = len(matrix)
        n = len(matrix[0])
        dual = [0] * n
        for i in range(m):
            for j in range(n):
                dual[j] += matrix[i][j]
        return dual
    
    def minimal_order(dual):
        gcd = 1
        for x in dual:
            while x % gcd == 0 and gcd != 1:
                gcd -= 1
            if gcd == 1:
                break
        return gcd
    
    def communication_complexity_rank_variance(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = sum(1 for i in range(m) if any(matrix[i][j] != 0 for j in range(n)))
        variance = (rank - n / m) ** 2
        return variance
    
    def euclidean_algorithm(a, b):
        while b:
            a, b = b, a % b
        return a
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        matrix = matrix_representation(f, n)
        dual = dual_vector(matrix)
        order = minimal_order(dual)
        variance = communication_complexity_rank_variance(matrix)
        results.append((order, variance))
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in results) / len(results)
    mean_x = sum(x for x, _ in results) / len(results)
    mean_y = sum(y for _, y in results) / len(results)
    std_dev_x = math.sqrt(sum((x - mean_x) ** 2 for x, _ in results) / len(results))
    std_dev_y = math.sqrt(sum((y - mean_y) ** 2 for _, y in results) / len(results))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": 0.5 < correlation_coefficient < 0.7,
        "counterexample": "" if 0.5 < correlation_coefficient < 0.7 else "correlation_out_of_range"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_out_of_range' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")