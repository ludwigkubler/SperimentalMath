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
    M = [A[i] + b[i] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n):
            M[i][j] /= factor
        b[i] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def kronecker_coefficient(n, k, m):
    if k > n or m > n:
        return 0
    A = [[0] * (n + 1) for _ in range(n + 1)]
    B = [[0] * (n + 1) for _ in range(n + 1)]
    C = [[0] * (n + 1) for _ in range(n + 1)]
    A[0][0] = 1
    B[0][0] = 1
    for i in range(1, n + 1):
        A[i][i-1] = i
        B[i][i-1] = i
    for i in range(n):
        C[i+1][i] = i + 1
    for _ in range(k - 1):
        C = matrix_multiply(C, A)
    for _ in range(m - 1):
        C = matrix_multiply(C, B)
    return C[0][n]

def generate_cnf(n):
    clauses = []
    for i in range(1, n + 1):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(2, 5))]
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = int(n ** 0.6)
    m = int(n ** 0.4)
    
    permanent_coefficient = kronecker_coefficient(n, k, m)
    determinant_coefficient = kronecker_coefficient(n, k, m)
    
    if permanent_coefficient == 0 or determinant_coefficient == 0:
        return {
            "metric_name": "Kronecker Coefficient Exponential Gap",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    if permanent_coefficient > determinant_coefficient * math.exp(2 * n):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Permanent coefficient {permanent_coefficient} not exponentially larger than determinant coefficient {determinant_coefficient}"
    
    return {
        "metric_name": "Kronecker Coefficient Exponential Gap",
        "metric_value": permanent_coefficient / determinant_coefficient,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")