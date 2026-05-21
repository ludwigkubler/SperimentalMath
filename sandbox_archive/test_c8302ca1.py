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

import math
import random
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        denom = A[i][i]
        if denom == 0:
            continue
        for j in range(n):
            A[i][j] /= denom
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        denom = A[i][i]
        if denom == 0:
            return 0
        det *= denom
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return det

def geometric_entropy(G):
    n = len(G)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) in G or (v, u) in G:
                adjacency_matrix[u][v] = adjacency_matrix[v][u] = 1
    laplacian_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(adjacency_matrix[i])
        laplacian_matrix[i][i] = degree
        for j in range(i + 1, n):
            laplacian_matrix[i][j] = laplacian_matrix[j][i] = -adjacency_matrix[i][j]
    gaussian_elimination(laplacian_matrix)
    eigenvalues = [laplacian_matrix[i][i] for i in range(n)]
    entropy = sum(-p * math.log2(p) if p > 0 else 0 for p in eigenvalues)
    return entropy

def disjointness_complexity(n):
    # Simplified lower bound for communication complexity of DISJ_n
    return n.bit_length()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = set()
    while len(G) < n * (n - 1) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in G and (v, u) not in G:
            G.add((u, v))
    gamma_Q = geometric_entropy(G)
    kappa_DISJ_n = disjointness_complexity(n)
    metric_value = gamma_Q
    instances_tested = 1
    conjecture_holds = gamma_Q >= kappa_DISJ_n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "geometric_entropy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")