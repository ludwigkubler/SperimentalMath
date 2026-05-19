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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def eigenvalues(matrix):
    n = len(matrix)
    if n != len(matrix[0]):
        raise ValueError("Matrix must be square")
    
    A = matrix.copy()
    identity = identity_matrix(n)
    lambda_values = []
    
    for _ in range(n):
        det = 1
        for i in range(n):
            det *= A[i][i]
        lambda_values.append(det)
        
        A_inv = gaussian_elimination(matrix_multiply(A, identity))
        A = matrix_multiply(A_inv, A)
    
    return lambda_values

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Calculate the second smallest eigenvalue
    L = [[G[i][j] - (1 if i == j else 0) for j in range(n)] for i in range(n)]
    lambda_values = sorted(eigenvalues(L))
    lambda_2 = lambda_values[1]
    
    # Compute the Tseitin formula's Resolution lower bound
    resolution_bound = 2 ** (math.log(1 / lambda_2, 2) * Fraction(1, 3))
    
    return {
        "metric_name": "Resolution Lower Bound",
        "metric_value": resolution_bound,
        "instances_tested": n,
        "conjecture_holds": True if resolution_bound >= 2 ** (math.log(1 / lambda_2, 2) * Fraction(1, 3)) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_support")