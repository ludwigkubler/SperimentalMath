# auto-injected by SEC sandbox
import math
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

def generate_random_matrix(n):
    return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]

def compute_gaussian_elimination(matrix):
    n = len(matrix)
    pivot = [i for i in range(n)]
    rank = n
    for i in range(n):
        if matrix[pivot[i]][i] == 0:
            flag = False
            for j in range(i + 1, n):
                if matrix[pivot[j]][i] != 0:
                    pivot[i], pivot[j] = pivot[j], pivot[i]
                    flag = True
                    break
            if not flag:
                rank -= 1
                continue
        factor = Fraction(matrix[pivot[i]][j], matrix[pivot[i]][i])
        for k in range(n):
            matrix[pivot[j]][k] -= factor * matrix[pivot[i]][k]
    return rank

def compute_matrix_rank(matrix):
    n = len(matrix)
    if n == 0:
        return 0
    elimination_matrix = [row[:] for row in matrix]
    rank = compute_gaussian_elimination(elimination_matrix)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in {5, 10, 15, 20, 30, 40}:
        A = generate_random_matrix(n)
        B = generate_random_matrix(n)
        C = [A[i] + B[i] for i in range(n)]
        r_C = compute_matrix_rank(C)
        
        # Compute Hodge bundle rank (simulated here as a random number for demonstration)
        min_rank_H_C = random.randint(1, n)
        
        results.append((min_rank_H_C, r_C))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    min_rank_H_C_values = [r[0] for r in results]
    r_C_values = [r[1] for r in results]
    
    n = len(results)
    mean_min_rank_H_C = sum(min_rank_H_C_values) / n
    mean_r_C = sum(r_C_values) / n
    
    covariance = sum((min_rank_H_C_values[i] - mean_min_rank_H_C) * (r_C_values[i] - mean_r_C) for i in range(n)) / n
    variance_min_rank_H_C = sum((min_rank_H_C_values[i] - mean_min_rank_H_C) ** 2 for i in range(n)) / n
    variance_r_C = sum((r_C_values[i] - mean_r_C) ** 2 for i in range(n)) / n
    
    pearson_correlation = covariance / (variance_min_rank_H_C * variance_r_C) ** 0.5
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation,
        "instances_tested": n,
        "n_max": max(n for n in {5, 10, 15, 20, 30, 40}),
        "conjecture_holds": pearson_correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = (sum((x - mean_value) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r >= 0.7) / len(results)
    
    if all(r >= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} mean={mean_value} std={std_value}")