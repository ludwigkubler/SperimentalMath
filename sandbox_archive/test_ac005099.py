# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, permutations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j]*x[j] for j in range(i+1, n))) / A[i][i]
    return x

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        sign = (-1) ** (c % 2)
        sub_det = determinant(submatrix)
        det += sign * matrix[0][c] * sub_det
    return det

def permanent(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    perm = list(permutations(range(n)))
    det = 0
    for p in perm:
        prod = 1
        for i in range(n):
            prod *= matrix[i][p[i]]
        det += prod
    return det

def young_tableaux_count(n, k):
    if n == 0 or k == 0:
        return 1
    return sum(young_tableaux_count(i, k-1) * young_tableaux_count(n-i-1, k-1) for i in range(k))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    poly = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    perm_count = permanent(poly)
    det_count = determinant(poly)
    tableaux_count = young_tableaux_count(n, n)
    
    conjecture_holds = perm_count > 2**n and det_count <= n**n
    counterexample = "" if conjecture_holds else "Permanent is not exponential or determinant is not polynomial"
    
    return {
        "metric_name": "tableaux_count",
        "metric_value": tableaux_count,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Permanent is not exponential or determinant is not polynomial\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")