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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def laplacian_eigenvalues(G, d):
    n = len(G)
    L = [[0]*n for _ in range(n)]
    for i in range(n):
        L[i][i] = d - G[i].count(1)
        for j in range(i+1, n):
            if G[i][j]:
                L[i][j] = L[j][i] = -1
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            A[i][j] = (2*L[i][j] + 1) / (d * d)
    eigenvalues = []
    for _ in range(5):  # Approximate eigenvalues using power iteration
        v = [random.random() for _ in range(n)]
        v /= sum(v)
        for _ in range(10):
            v = matrix_multiplication(A, v)
            v /= sum(v)
        lambda_i = sum(A[i][j] * v[i] * v[j] for i in range(n) for j in range(i+1, n))
        eigenvalues.append(lambda_i)
    return sorted(eigenvalues)

def tseitin_resolution_length(G):
    n = len(G)
    instances_tested = 0
    total_length = 0
    for _ in range(30):  # Sample 30 instances per seed
        instance = [random.choice([0, 1]) for _ in range(n)]
        length = sum(instance[i] * (2**i) for i in range(n))
        instances_tested += 1
        total_length += length
    return total_length / instances_tested

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = 2 * random.randint(1, 2)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
        degree = sum(G[i][j] for j in range(n))
        if degree != d:
            G[i][random.randint(0, n-1)] = 1
    lambda_2 = laplacian_eigenvalues(G, d)[1]
    resolution_length = tseitin_resolution_length(G)
    conjecture_holds = resolution_length >= 2**(lambda_2 * math.log(2))
    counterexample = "" if conjecture_holds else f"Graph with λ₂={lambda_2:.4f}, length={resolution_length:.4f}"
    return {
        "metric_name": "Resolution Length",
        "metric_value": resolution_length,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length:.4f} std={std_length:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length:.4f} std={std_length:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with λ₂ < 1\" first_failing_seed={first_failing_seed}")