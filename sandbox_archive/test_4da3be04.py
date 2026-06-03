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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Swap with a row below that has a non-zero pivot
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Eliminate the entries below the pivot
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(matrix):
    matrix = gaussian_elimination(matrix)
    r = sum(1 for row in matrix if any(row))
    return r

def minimal_local_indeterminacy(M):
    n = len(M)
    alpha_M = 0
    for i in range(n):
        for j in range(i + 1, n):
            if M[i][j] != 0:
                alpha_M += 1
    return alpha_M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        alpha_M = minimal_local_indeterminacy(M)
        r_M = rank(M)
        
        results.append({
            "alpha_M": alpha_M,
            "r_M": r_M
        })
    
    if not results:
        return {
            "metric_name": "minimal_local_indeterminacy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_matrix"
        }
    
    total_alpha = sum(result["alpha_M"] for result in results)
    total_r = sum(result["r_M"] for result in results)
    mean_alpha = Fraction(total_alpha, len(results))
    mean_r = Fraction(total_r, len(results))
    
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((result["alpha_M"] - mean_alpha) * (result["r_M"] - mean_r) for result in results)
        denominator = math.sqrt(sum((result["alpha_M"] - mean_alpha) ** 2 for result in results)) * math.sqrt(sum((result["r_M"] - mean_r) ** 2 for result in results))
        correlation_coefficient = numerator / denominator
    
    max_n = max(n_values)
    
    return {
        "metric_name": "minimal_local_indeterminacy",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(mean_alpha - mean_r) / max_n <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")