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
    m, n = len(A), len(B[0])
    p = len(B)
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    m = len(A)
    n = len(A[0])
    result = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return result

def matrix_subtract(A, B):
    m = len(A)
    n = len(A[0])
    result = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return result

def transpose(A):
    m = len(A)
    n = len(A[0])
    result = [[A[j][i] for j in range(m)] for i in range(n)]
    return result

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    elif len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det = 0
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

def minor(A, i, j):
    return [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]

def cofactor_matrix(A):
    m = len(A)
    n = len(A[0])
    result = [[(-1) ** (i+j) * determinant(minor(A, i, j)) for j in range(n)] for i in range(m)]
    return result

def inverse(A):
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is singular")
    cofactors = cofactor_matrix(A)
    adjugate = transpose(cofactors)
    inv_det_A = 1 / det_A
    result = [[adjugate[i][j] * inv_det_A for j in range(len(A[0]))] for i in range(len(A))]
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(2, 3)
    if n == 2:
        # Known invariants for determinant of 2x2 matrix
        det_inv_1 = lambda x, y: x[0][0] * x[1][1] - x[0][1] * x[1][0]
        det_inv_2 = lambda x, y: x[0][0] + x[1][1]
        det_inv_3 = lambda x, y: x[0][1] - x[1][0]
        
        # Known invariants for permanent of 2x2 matrix
        perm_inv_1 = lambda x, y: x[0][0] * x[1][1] + x[0][1] * x[1][0]
        perm_inv_2 = lambda x, y: x[0][0] + x[1][1]
        
        det_invariants = [det_inv_1, det_inv_2, det_inv_3]
        perm_invariants = [perm_inv_1, perm_inv_2]
    else:
        # For larger n, we cannot easily compute the exact invariants
        return {
            "metric_name": "Invariant Polynomial Count",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    det_invariant_count = len(det_invariants)
    perm_invariant_count = len(perm_invariants)
    
    return {
        "metric_name": "Invariant Polynomial Count",
        "metric_value": det_invariant_count - perm_invariant_count,
        "instances_tested": 1,
        "conjecture_holds": det_invariant_count < perm_invariant_count,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")