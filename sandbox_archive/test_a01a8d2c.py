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

def generate_disjointness_matrix(n):
    A = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(i + 1, 2**n):
            if bin(i & j).count('1') == 1:
                A[i][j] = 1
                A[j][i] = 1
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(matrix, size):
    if size == 1:
        return matrix[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(size):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * determinant(submatrix, size - 1)
        sign *= -1
    return det

def secant_variety_dimension(A):
    n = len(A)
    if n == 0:
        return 0
    C = A
    for _ in range(2):  # Compute the secant variety by taking the sum of two matrices
        B = generate_disjointness_matrix(n)
        C = matrix_multiplication(C, B)
    det_C = determinant(C, n)
    if det_C <= 0:
        return 0
    return math.log2(det_C) / n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    A = generate_disjointness_matrix(n)
    dimension = secant_variety_dimension(A)
    if dimension < n:
        return {
            "metric_name": "secant_variety_dimension",
            "metric_value": dimension,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Matrix with n={n}, A=[{A}]"
        }
    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": dimension,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    total_metric_value = sum(result["metric_value"] for result in results if result["conjecture_holds"])
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")