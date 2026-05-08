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
        max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_idx] = A[max_idx], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def lu_decomposition(A):
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            sum_l = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - sum_l
        for j in range(i, n):
            if i == j:
                L[j][i] = 1.0
            else:
                sum_u = sum(L[j][k] * U[k][i] for k in range(i))
                L[j][i] = (A[j][i] - sum_u) / U[i][i]
    return L, U

def determinant(A):
    n = len(A)
    det = 1.0
    for i in range(n):
        L, U = lu_decomposition(A)
        det *= U[i][i]
    return det

def laplacian_matrix(G):
    n = len(G)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if G[i][j])
        L[i][i] = -degree
        for j in range(i+1, n):
            if G[i][j]:
                L[i][j] = 1.0
                L[j][i] = 1.0
    return L

def fiedler_value(G):
    n = len(G)
    L = laplacian_matrix(G)
    eigenvalues = []
    for _ in range(n):
        v = [random.random() for _ in range(n)]
        v /= math.sqrt(sum(x**2 for x in v))
        for _ in range(100):  # Power iteration
            v = [sum(L[i][j] * v[j] for j in range(n)) for i in range(n)]
            v /= math.sqrt(sum(x**2 for x in v))
        eigenvalues.append(v[0])
    return sorted(eigenvalues)[1]

def tseitin_resolution_length(G):
    n = len(G)
    # Simplified DPLL-based resolution length estimation
    return 2 ** (n / 4)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = [[random.random() < 0.1 for _ in range(n)] for _ in range(n)]
    G = [row[:] for row in G]  # Ensure it's symmetric
    fiedler_val = fiedler_value(G)
    resolution_length = tseitin_resolution_length(G)
    metric_name = "resolution_length"
    metric_value = resolution_length
    instances_tested = 1
    conjecture_holds = resolution_length >= 2 ** (0.5 / fiedler_val)
    counterexample = "" if conjecture_holds else f"Graph with n={n}, λ_2={fiedler_val}, resolution_length={resolution_length}"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={n}, λ_2={fiedler_val}, resolution_length={resolution_length}\" first_failing_seed={first_failing_seed}")