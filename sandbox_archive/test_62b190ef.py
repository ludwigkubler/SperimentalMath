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
    
    def generate_random_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_multiplication(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        cols_B = len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return result
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
        for i in range(rows):
            max_row = max(range(i, rows), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            for j in range(cols + 1):
                augmented_matrix[i][j] /= augmented_matrix[i][i]
            for k in range(rows):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(cols + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[:-1] for row in augmented_matrix]
    
    def compute_eigenvalue(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        eigenvalues = []
        for k in range(1, n + 1):
            A_k = matrix_multiplication(matrix, identity)
            eigenvector = gaussian_elimination(A_k)[-1]
            eigenvalue = sum(eigenvector[i] * eigenvector[j] for i in range(n) for j in range(n))
            eigenvalues.append(eigenvalue)
        return min(eigenvalues)
    
    n = 20
    s = 5
    d = 3
    
    f = generate_random_function(n)
    M_k_f = [[sum(f[i] * f[j] for i, j in itertools.combinations(range(2**n), k)) for k in range(n + 1)] for _ in range(n + 1)]
    
    lambda_min = compute_eigenvalue(M_k_f)
    epsilon = 0.1
    k = math.ceil(math.log(s) / math.sqrt(2))
    
    conjecture_holds = lambda_min >= s**(-0.5) and epsilon < s**(-0.5)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimum_eigenvalue",
        "metric_value": lambda_min,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")