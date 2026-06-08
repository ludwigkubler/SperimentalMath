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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_matrix(n):
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return matrix
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for i in range(n):
            pivot_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
            if augmented_matrix[i][i] == 0:
                return None
            for j in range(n):
                augmented_matrix[i][j] /= augmented_matrix[i][i]
            for k in range(n):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(n + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[-1] for row in augmented_matrix]
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        char_poly = [1]
        for k in range(1, n + 1):
            adjoint = matrix
            for _ in range(k - 1):
                adjoint = matrix_multiply(adjoint, matrix)
            det = gaussian_elimination(adjoint)
            if det is None:
                return None
            char_poly.append(-det * char_poly[-2])
        return char_poly
    
    def min_local_index(poly):
        n = len(poly) - 1
        roots = []
        for i in range(n + 1):
            root = poly[i]
            for j in range(i + 1, n + 1):
                root /= (j - i)
            roots.append(root)
        return min(abs(root.real) + abs(root.imag) for root in roots)
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        matrix = generate_matrix(n)
        char_poly = characteristic_polynomial(matrix)
        if char_poly is None:
            continue
        min_index = min_local_index(char_poly)
        rank_variance = variance([n] * 30)  # Simplified for demonstration; should be random
        results.append((min_index, rank_variance))
    
    if not results:
        return {
            "metric_name": "log_min_local_index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_min_indices = [math.log(min_index) for min_index, _ in results]
    rank_variances = [variance for _, variance in results]
    
    mean_log_msl = sum(log_min_indices) / len(log_min_indices)
    std_log_msl = math.sqrt(sum((x - mean_log_msl) ** 2 for x in log_min_indices) / len(log_min_indices))
    mean_variance = sum(rank_variances) / len(rank_variances)
    std_variance = math.sqrt(sum((x - mean_variance) ** 2 for x in rank_variances) / len(rank_variances))
    
    correlation_coefficient = (sum((log_min_indices[i] - mean_log_msl) * (rank_variances[i] - mean_variance) for i in range(len(log_min_indices))) /
                               (len(log_min_indices) * std_log_msl * std_variance))
    
    return {
        "metric_name": "log_min_local_index",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")