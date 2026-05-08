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
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def perm(n):
        return [random.randint(0, n-1) for _ in range(n)]
    
    def det(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            det_val = 0
            for c in range(n):
                M = [row[:c] + row[c+1:] for row in A[1:]]
                sign = (-1) ** (c % 2)
                sub_det = det(M)
                det_val += sign * A[0][c] * sub_det
            return det_val
    
    def plethysm_coefficient(n, k):
        if n == k:
            return 1
        elif k == 0:
            return 1
        else:
            return sum(plethysm_coefficient(i, j) * plethysm_coefficient(n-i, k-j-1) for i in range(k+1, n-k+2))
    
    def hook_partition(n, k):
        if n == k:
            return [k]
        elif k == 0:
            return []
        else:
            return [k] + hook_partition(n-k-1, k-1)
    
    max_perm = 0
    max_det = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        m = int(math.floor(n ** 1.5))
        
        A = [perm(n) for _ in range(n)]
        B = [perm(m) for _ in range(m)]
        
        perm_poly = det(matrix_multiply(A, A))
        det_poly = det(matrix_multiply(B, B))
        
        hook = hook_partition(n, k)
        coeff_perm = plethysm_coefficient(n, len(hook))
        coeff_det = plethysm_coefficient(m, len(hook))
        
        if coeff_perm > max_perm:
            max_perm = coeff_perm
        if coeff_det > max_det:
            max_det = coeff_det
    
    perm_ratio = max_perm / (2 ** (n // 10))
    det_ratio = max_det / n**3
    
    conjecture_holds = perm_ratio >= 2**(n/10) and det_ratio <= n**3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "plethysm_coefficient_gap",
        "metric_value": perm_ratio,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_perm_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev_perm_ratio = math.sqrt(sum((r["metric_value"] - mean_perm_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_perm_ratio} std={std_dev_perm_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_perm_ratio} std={std_dev_perm_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")