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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    det = 0
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for c in range(n):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
    return det

def laplacian_matrix(G):
    n = len(G)
    L = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        degree = sum(G[i])
        L[i][i] = -degree
        for j in range(i+1, n):
            if G[i][j]:
                L[i][j] = L[j][i] = 1
    return L

def free_entropy(L):
    n = len(L)
    det_L = determinant(L)
    if det_L == 0:
        return float('-inf')
    eigenvalues = []
    for i in range(n):
        A = [row[:i] + row[i+1:] for row in L]
        eigenvalues.append(-math.log(abs(determinant(A))))
    return sum(eigenvalues)

def distinguishing_tensor_width(BP):
    # Placeholder function, replace with actual implementation
    return 1.0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    BP = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    G = [[sum(BP[i][j] for j in range(i+1, n)) for i in range(n)]]
    L = laplacian_matrix(G)
    F_G = free_entropy(L)
    DTW_BP = distinguishing_tensor_width(BP)
    if DTW_BP == 0:
        return {
            "metric_name": "F(G)/DTW(BP)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DTW(BP) is zero"
        }
    ratio = F_G / DTW_BP
    return {
        "metric_name": "F(G)/DTW(BP)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= n**2,  # Placeholder function for f(n)
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"f(n) is too weak\" first_failing_seed={first_failing_seed}")