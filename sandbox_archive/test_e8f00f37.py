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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    for i in range(n):
        if all(matrix[i][j] == 0 for j in range(m)):
            continue
        pivot = matrix[i]
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], pivot[i])
            for k in range(m):
                matrix[j][k] -= factor * pivot[k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_communication_instance(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A, B
    
    def compute_hodge_bundle_rank(A, B):
        n = len(A)
        H = [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
        return matrix_rank(H)
    
    def compute_matrix_rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[i][j] == 0 for j in range(m)):
                continue
            pivot = matrix[i]
            for j in range(i + 1, n):
                factor = Fraction(matrix[j][i], pivot[i])
                for k in range(m):
                    matrix[j][k] -= factor * pivot[k]
            rank += 1
        return rank
    
    instances_tested = 0
    min_rank_H_C = []
    r_C_values = []
    
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):
            A, B = generate_communication_instance(n)
            min_rank_H_C.append(compute_hodge_bundle_rank(A, B))
            r_C_values.append(compute_matrix_rank([A[i] + B[i] for i in range(n)]))
            instances_tested += 1
    
    if not min_rank_H_C or not r_C_values:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_min_rank_H_C = sum(min_rank_H_C) / len(min_rank_H_C)
    mean_r_C = sum(r_C_values) / len(r_C_values)
    
    covariance = sum((x - mean_min_rank_H_C) * (y - mean_r_C) for x, y in zip(min_rank_H_C, r_C_values))
    variance_min_rank_H_C = sum((x - mean_min_rank_H_C) ** 2 for x in min_rank_H_C)
    variance_r_C = sum((y - mean_r_C) ** 2 for y in r_C_values)
    
    if variance_min_rank_H_C == 0 or variance_r_C == 0:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    pearson_correlation = covariance / (math.sqrt(variance_min_rank_H_C) * math.sqrt(variance_r_C))
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": pearson_correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and min(result["metric_value"] for result in results if result["metric_value"] is not None) < 0.5:
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")