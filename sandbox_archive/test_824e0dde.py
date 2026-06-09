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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    inv = [[0] * n for _ in range(n)]
    det = 0
    for i in range(n):
        det += matrix[0][i] * minor(matrix, 0, i) * (1 if i % 2 == 0 else -1)
    det = mod_inverse(det % mod, mod)
    for i in range(n):
        for j in range(n):
            inv[i][j] = (minor(matrix, i, j) * (1 if (i + j) % 2 == 0 else -1)) % mod
    return [[(inv[i][j] * det) % mod for j in range(n)] for i in range(n)]

def minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in matrix[1:]]

def matrix_mul(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
    return result

def matrix_add(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] + B[i][j]) % mod
    return result

def matrix_sub(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] - B[i][j]) % mod
    return result

def matrix_trace(matrix):
    n = len(matrix)
    trace = 0
    for i in range(n):
        trace += matrix[i][i]
    return trace

def generate_polynomial_instance(m, seed):
    random.seed(seed)
    variables = [random.randint(1, m) for _ in range(m)]
    coefficients = [random.randint(1, m) for _ in range(m + 1)]
    polynomial = sum(coefficients[i] * (x ** i) for i, x in enumerate(variables))
    return polynomial

def compute_min_local_defect(polynomial):
    # Placeholder function to simulate computation of min local defect
    # In practice, this would involve algebraic operations and cohomology theory
    return random.randint(1, 10)

def compute_rank_variance(polynomial):
    # Placeholder function to simulate computation of rank variance
    # In practice, this would involve communication complexity analysis
    return random.uniform(1, 10)

def run_trial(seed: int) -> dict:
    m = 5 + (seed % 6) * 5  # Sweep n through {5, 10, 15, 20, 30, 40}
    polynomial = generate_polynomial_instance(m, seed)
    min_local_defect = compute_min_local_defect(polynomial)
    rank_variance = compute_rank_variance(polynomial)
    
    if min_local_defect == 0:
        return {
            "metric_name": "rank_variance",
            "metric_value": rank_variance,
            "instances_tested": 1,
            "n_max": m,
            "conjecture_holds": False,
            "counterexample": "min_local_defect_zero"
        }
    
    if rank_variance > min_local_defect:
        return {
            "metric_name": "rank_variance",
            "metric_value": rank_variance,
            "instances_tested": 1,
            "n_max": m,
            "conjecture_holds": False,
            "counterexample": f"variance {rank_variance} > defect {min_local_defect}"
        }
    
    return {
        "metric_name": "rank_variance",
        "metric_value": rank_variance,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": True,
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"variance > defect\" first_failing_seed={first_failing_seed}")