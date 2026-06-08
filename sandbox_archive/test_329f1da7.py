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
    
    def generate_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def matrix_rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        if m == 0 or n == 0:
            return 0
        rank = min(m, n)
        for i in range(rank):
            if matrix[i][i] == 0:
                found_pivot = False
                for k in range(i + 1, m):
                    if matrix[k][i] != 0:
                        matrix[i], matrix[k] = matrix[k], matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    rank -= 1
                    continue
            for j in range(n):
                if j != i:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        coeff = [1]
        for k in range(1, n + 1):
            new_coeff = [0] * (k + 1)
            new_coeff[0] = -sum(matrix[i][i] * coeff[-1] for i in range(k))
            for j in range(1, k + 1):
                new_coeff[j] = sum(matrix[i][j-1] * coeff[-j] for i in range(j)) - sum(matrix[i][k-j] * coeff[-j-1] for i in range(k-j+1, k+1))
            coeff = new_coeff
        return coeff
    
    def min_local_index(coeff):
        n = len(coeff)
        if n == 0:
            return 0
        roots = []
        for _ in range(30):  # Use a fixed number of iterations to find roots
            x = random.uniform(-10, 10)  # Initial guess
            for _ in range(20):
                fx = sum(coeff[i] * x**i for i in range(n))
                dfx = sum(i * coeff[i] * x**(i-1) for i in range(1, n))
                if dfx == 0:
                    break
                x -= fx / dfx
            roots.append(x)
        return min(abs(root.imag) for root in roots)
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    results = []
    for n in range(5, 41):
        matrix = generate_matrix(n)
        rank = matrix_rank(matrix)
        coeff = characteristic_polynomial(matrix)
        msl = min_local_index(coeff)
        results.append((n, rank, msl))
    
    ranks = [r for _, r, _ in results]
    msis = [msl for _, _, msl in results]
    
    var_rank = variance(ranks)
    mean_msi = sum(msis) / len(msis)
    
    correlation_coefficient = 0
    if var_rank != 0:
        correlation_coefficient = sum((r - mean_ranks) * (msl - mean_msi) for _, r, msl in results) / (len(results) * math.sqrt(var_rank * variance(msis)))
    
    return {
        "metric_name": "log_min_local_index",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    total_results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        total_results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in total_results) / len(total_results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in total_results) / len(total_results))
    support_fraction = sum(1 for result in total_results if result["conjecture_holds"]) / len(total_results)
    
    if all(result["conjecture_holds"] for result in total_results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, total_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")