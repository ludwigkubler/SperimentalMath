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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_max_cut_instance(n):
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.append((i, j))
    return edges

def degree_matrix(edges, n):
    D = [[0] * n for _ in range(n)]
    for u, v in edges:
        D[u][u] += 1
        D[v][v] += 1
    return D

def adjacency_matrix(edges, n):
    A = [[0] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = 1
        A[v][u] = 1
    return A

def matrix_multiply(A, B):
    m = len(A)
    p = len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(A):
    return [list(row) for row in zip(*A)]

def identity_matrix(n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def matrix_addition(A, B):
    m = len(A)
    n = len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_subtraction(A, B):
    m = len(A)
    n = len(A[0])
    C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return C

def scalar_multiplication(A, c):
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_trace(A):
    return sum(A[i][i] for i in range(len(A)))

def matrix_power(A, k):
    if k == 1:
        return A
    elif k % 2 == 0:
        B = matrix_power(A, k // 2)
        return matrix_multiply(B, B)
    else:
        B = matrix_power(A, (k - 1) // 2)
        return matrix_multiply(matrix_multiply(B, B), A)

def spectral_radius(M):
    n = len(M)
    x = [Fraction(1, math.sqrt(n))] * n
    for _ in range(100):  # Power iteration method
        y = matrix_multiply(M, x)
        x = scalar_multiplication(y, Fraction(1, matrix_norm(y)))
    return max(abs(x[i]) for i in range(n))

def matrix_norm(A):
    return math.sqrt(sum(sum(a[i][j] ** 2 for j in range(len(a[0]))) for a in A))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    edges = generate_max_cut_instance(n)
    D = degree_matrix(edges, n)
    A = adjacency_matrix(edges, n)
    M = matrix_addition(D, scalar_multiplication(A, -Fraction(1, 2)))
    
    rho_M = spectral_radius(M)
    c = rho_M / math.sqrt(n)
    approximation_ratio = c / math.sqrt(n)
    
    return {
        "metric_name": "approximation_ratio",
        "metric_value": float(approximation_ratio),
        "instances_tested": 1,
        "conjecture_holds": abs(c - 1) < 0.1 and abs(approximation_ratio - 1) < 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")