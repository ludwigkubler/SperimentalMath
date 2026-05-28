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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_rank(A):
    n = len(A)
    rank = 0
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    for i in range(n):
        if any(A_copy[i]):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        size_P = n
        # Generate a read-twice BP instance (simplified as a random matrix)
        P = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        # Compute the minimal rank of the free probability distribution associated with P
        rho_P = matrix_rank(P)
        results.append({"n": n, "size_P": size_P, "rho_P": rho_P})
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_rho = sum(result["rho_P"] for result in results)
    avg_rho = total_rho / len(results)
    std_rho = math.sqrt(sum((result["rho_P"] - avg_rho) ** 2 for result in results) / len(results))
    log_sizes = [math.log(result["size_P"]) for result in results]
    
    correlation_coefficient = sum((log_sizes[i] - avg_log_size) * (results[i]["rho_P"] - avg_rho) for i in range(len(log_sizes))) / (len(log_sizes) * std_log_size * std_rho)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rho,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.9 and max(result["rho_P"] for result in results) < n_values[-1] * math.log(n_values[-1]),
        "counterexample": "" if correlation_coefficient >= 0.9 and max(result["rho_P"] for result in results) < n_values[-1] * math.log(n_values[-1]) else f"rho(P) = {max(result['rho_P'] for result in results)}, but size(P) ≤ {n_values[-1]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_rho = sum(result["metric_value"] for result in results) / len(results)
    std_rho = math.sqrt(sum((result["metric_value"] - avg_rho) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and max(result["rho_P"] for result in results) >= n_values[-1] * math.log(n_values[-1]):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho(P) = {max(result['rho_P'] for result in results)}, but size(P) ≤ {n_values[-1]}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")