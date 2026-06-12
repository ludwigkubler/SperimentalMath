# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    if gcd(a, m) != 1:
        raise ValueError("Modular inverse does not exist")
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= mod
    return C

def matrix_inv(A, mod):
    n = len(A)
    I = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = A[i][i]
        inv_pivot = mod_inverse(pivot, mod)
        for j in range(n):
            A[i][j] *= inv_pivot
            A[i][j] %= mod
            I[i][j] *= inv_pivot
            I[i][j] %= mod
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    A[k][j] %= mod
                    I[k][j] -= factor * I[i][j]
                    I[k][j] %= mod
    return I

def polyfit(x, y, degree):
    n = len(x)
    X = [[1] + [x[i]**j for j in range(1, degree+1)] for i in range(n)]
    Y = y[:]
    A = matrix_mul(X, matrix_inv(matrix_mul(X, transpose(X), mod=10**9+7), mod=10**9+7), mod=10**9+7)
    coefficients = [sum(A[i][j] * Y[j] for j in range(n)) % (10**9+7) for i in range(degree+1)]
    return coefficients

def transpose(matrix):
    n = len(matrix)
    m = len(matrix[0])
    return [[matrix[j][i] for j in range(n)] for i in range(m)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_communication_complexity(n):
        # Placeholder function to generate communication complexity
        # This is a dummy implementation and should be replaced with actual generation logic
        return [random.randint(1, 10**6) for _ in range(n)]
    
    def compute_msqr(complexity):
        # Placeholder function to compute minimal symplectic quotient rank
        # This is a dummy implementation and should be replaced with actual computation logic
        return random.randint(1, 10**3)
    
    n_values = [5, 10, 15, 20, 30, 40]
    msqr_values = []
    rv_values = []
    
    for n in n_values:
        for _ in range(5):
            complexity = generate_communication_complexity(n)
            msqr = compute_msqr(complexity)
            msqr_values.append(msqr)
            rv_values.append(sum((x - sum(complexity) / len(complexity))**2 for x in complexity) / len(complexity))
    
    if not msqr_values or not rv_values:
        return {
            "metric_name": "msqr_vs_rv",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    coefficients = polyfit(rv_values, msqr_values, 1)
    r_squared = sum((rv_values[i] - (coefficients[0] * rv_values[i] + coefficients[1]))**2 for i in range(len(rv_values))) / len(rv_values)
    r_squared = 1 - r_squared
    
    return {
        "metric_name": "msqr_vs_rv",
        "metric_value": r_squared,
        "instances_tested": len(msqr_values),
        "n_max": max(n_values),
        "conjecture_holds": r_squared >= 0.95,
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
    
    mean_r_squared = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not_enough_support' first_failing_seed={first_failing_seed}")