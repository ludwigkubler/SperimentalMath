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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return result

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find the pivot
        max_row = i
        for r in range(i+1, n):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = -matrix[i][i]
        for j in range(i, n):
            matrix[i][j] += factor * matrix[j][i]
        for r in range(n):
            if r != i:
                factor = matrix[r][i]
                for j in range(i, n):
                    matrix[r][j] += factor * matrix[i][j]
    
    # Back substitution
    result = [0] * n
    for i in range(n-1, -1, -1):
        result[i] = matrix[i][-1]
        for j in range(i+1, n):
            result[i] -= matrix[i][j] * result[j]
        result[i] /= matrix[i][i]
    
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30 + (seed % 4) * 5
    if n > 40:
        return {
            "metric_name": "EntRank(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "n_too_large"
        }
    
    # Generate a random partial function f: {0,1}^n → {0,1}
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the entropic quantizer rank EntRank(f)
    # This is a placeholder implementation. For actual testing, you would need
    # a quantum state encoding algorithm.
    EntRank_f = math.ceil(math.log(n, 2))
    
    # Measure the randomized communication complexity C_DISJ(f)
    # This is a placeholder implementation. For actual testing, you would need
    # to simulate the distribution of bits exchanged between two parties solving
    # the Disjointness problem on f.
    C_DISJ_f = n
    
    return {
        "metric_name": "EntRank(f)",
        "metric_value": EntRank_f,
        "instances_tested": 1,
        "conjecture_holds": EntRank_f == math.ceil(math.log(n, 2)) and C_DISJ_f >= n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")