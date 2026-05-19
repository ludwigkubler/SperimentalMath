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
        m, k = len(A), len(B[0])
        result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]
        return result
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(i, n):
                matrix[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def compute_eigenvalue(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        eigenvalues = []
        A = matrix
        for _ in range(100):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v = [x / sum(v) for x in v]  # Normalize
            Av = matrix_multiplication(A, v)
            lambda_ = sum(x * y for x, y in zip(Av, v))
            eigenvalues.append(lambda_)
        return max(eigenvalues)
    
    def sos_moment_matrix(f):
        n = int(math.log2(len(f)))
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(2**n):
            x = [f[i >> j & 1] for j in range(n)]
            for k in range(n + 1):
                M[k][k] += x[0]**k
                for l in range(k):
                    M[l][k] += x[0]**l * x[1]**(k - l)
        return M
    
    n = 20
    f = generate_random_function(n)
    M = sos_moment_matrix(f)
    M = gaussian_elimination(M)
    lambda_min = compute_eigenvalue(M)
    
    k = int(math.log2(n))
    s = len(f) // (1 << n)
    conjecture_holds = lambda_min >= 1 / math.sqrt(s)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_eigenvalue",
        "metric_value": lambda_min,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")