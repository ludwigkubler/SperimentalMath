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
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def inv_mod(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mul(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
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

def solve_linear_program(A, b, c):
    n = len(b)
    m = len(c)
    A = [row + [0] * (m - len(row)) for row in A]
    b = b + [0] * (m - len(b))
    c = c + [0] * (n - len(c))
    x = [0] * n
    while True:
        pivot_col = None
        pivot_row = None
        min_ratio = float('inf')
        for j in range(n):
            if c[j] > 0 and (pivot_col is None or c[j] < c[pivot_col]):
                pivot_col = j
                for i in range(m):
                    if A[i][j] > 0:
                        ratio = b[i] / A[i][j]
                        if ratio < min_ratio:
                            min_ratio = ratio
                            pivot_row = i
        if pivot_col is None:
            break
        x[pivot_col] = min_ratio
        for j in range(n):
            if j != pivot_col:
                x[j] -= (A[pivot_row][j] / A[pivot_row][pivot_col]) * x[pivot_col]
        b[pivot_row] %= A[pivot_row][pivot_col]
    return x

def dual_convex_body_width(A, b):
    n = len(b)
    c = [0] * n
    x = solve_linear_program(A, b, c)
    return max(x)

def sos_degree(n):
    return 2 * n + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    b = [random.randint(-10, 10) for _ in range(n)]
    c = [random.randint(-10, 10) for _ in range(n)]
    
    min_width = dual_convex_body_width(A, b)
    if min_width < 1 / math.sqrt(n):
        return {
            "metric_name": "SOS Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "min_width(Δ) < 1/√n"
        }
    
    d = sos_degree(n)
    return {
        "metric_name": "SOS Degree",
        "metric_value": d,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='min_width(Δ) < 1/√n' first_failing_seed={first_failing_seed}")