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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            if j != i:
                factor = Fraction(matrix[j][i], pivot)
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def matrix_rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    A = [row[:] for row in matrix]
    rank = 0
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda x: abs(A[x][i]))
        if A[max_row][i] == 0:
            continue
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(m):
            A[i][j] /= pivot
        rank += 1
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(m):
                    A[j][k] -= factor * A[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n * n > 1000:  # Avoid excessive memory usage
            continue
        
        protocol = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        rank_comm_complexity = matrix_rank(protocol)
        
        p_adic_unit_ball = [sum(row[i] * (2 ** i) for i in range(n)) % n for row in protocol]
        min_p_adic_rank = min(p_adic_unit_ball)
        
        results.append({
            "n": n,
            "rank_comm_complexity": rank_comm_complexity,
            "min_p_adic_rank": min_p_adic_rank
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    
    rank_comm_values = [result["rank_comm_complexity"] for result in results]
    min_p_adic_values = [result["min_p_adic_rank"] for result in results]
    
    mean_rank_comm = sum(rank_comm_values) / instances_tested
    mean_min_p_adic = sum(min_p_adic_values) / instances_tested
    
    variance_rank_comm = sum((x - mean_rank_comm) ** 2 for x in rank_comm_values) / instances_tested
    variance_min_p_adic = sum((x - mean_min_p_adic) ** 2 for x in min_p_adic_values) / instances_tested
    
    covariance = sum((rank_comm_values[i] - mean_rank_comm) * (min_p_adic_values[i] - mean_min_p_adic) for i in range(instances_tested)) / instances_tested
    correlation_coefficient = covariance / math.sqrt(variance_rank_comm * variance_min_p_adic)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_instances")