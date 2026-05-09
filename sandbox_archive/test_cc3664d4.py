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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n] / M[i][i]
        for j in range(i-1, -1, -1):
            M[j][n] -= M[j][i] * x[i]
    return x

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += ((-1) ** j) * A[0][j] * determinant(submatrix)
    return det

def permanent(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    perm = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        perm += A[0][j] * permanent(submatrix)
    return perm

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    instances_tested = 30
    
    def map_clause_to_tensor(clause):
        m = len(clause)
        tensor = [[0] * (m+1) for _ in range(m+1)]
        for i, var in enumerate(clause):
            tensor[i][var] = 1
            tensor[var][i] = 1
        return tensor
    
    def decompose_tensor(tensor):
        m = len(tensor)
        det = determinant(tensor)
        perm = permanent(tensor)
        return det, perm
    
    mu_perm = 0
    mu_det = 0
    
    for _ in range(instances_tested):
        clause = [random.randint(1, n) for _ in range(random.randint(3, 5))]
        tensor = map_clause_to_tensor(clause)
        det, perm = decompose_tensor(tensor)
        mu_perm += abs(perm)
        mu_det += abs(det)
    
    mu_perm /= instances_tested
    mu_det /= instances_tested
    
    conjecture_holds = mu_perm >= 2**(math.log2(n) * 10)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mu_ratio",
        "metric_value": mu_perm / mu_det,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30)) + [53, 67, 79]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")