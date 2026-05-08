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

def matrix_multiply(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def matrix_scale(A, c):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] * c
    return C

def identity_matrix(n):
    I = [[0]*n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def transpose(A):
    n = len(A)
    B = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            B[j][i] = A[i][j]
    return B

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        det += (-1)**j * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
    return det

def inverse(A):
    n = len(A)
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    adjugate = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = (-1)**(i+j) * determinant(minor)
            adjugate[j][i] = cofactor
    return matrix_scale(adjugate, 1/det)

def gaussian_elimination(A):
    n = len(A)
    B = [row[:] for row in A]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(B[j][i]) > abs(B[max_row][i]):
                max_row = j
        B[i], B[max_row] = B[max_row], B[i]
        for j in range(i+1, n):
            factor = B[j][i] / B[i][i]
            for k in range(n):
                B[j][k] -= factor * B[i][k]
    return B

def is_invertible(A):
    try:
        inverse(A)
        return True
    except ValueError:
        return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    if n > 30:
        n = 30
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    C = matrix_multiply(A, B)
    det_C = determinant(C)
    if det_C == 0:
        return {
            "metric_name": "Determinant",
            "metric_value": det_C,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Matrix is not invertible"
        }
    inv_C = inverse(C)
    metric_value = sum(sum(abs(x) for x in row) for row in inv_C)
    return {
        "metric_name": "Spectral Norm",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 31)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")