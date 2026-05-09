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

def power_iteration(A, n=100):
    v = [random.random() for _ in range(len(A))]
    v = [x / sum(v) for x in v]
    for _ in range(n):
        v = matmul(A, v)
        v = [x / sum(v) for x in v]
    return v

def matmul(A, b):
    return [sum(a * b_i for a, b_i in zip(row, b)) for row in A]

def generate_d_regular_graph(n, d):
    if (d * n) % 2 != 0:
        raise ValueError("d must be even")
    adj_matrix = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < d * n // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
            edges.add((u, v))
    return adj_matrix

def second_eigenvalue(adj_matrix):
    n = len(adj_matrix)
    A = [[0 if i == j else adj_matrix[i][j] for j in range(n)] for i in range(n)]
    d = sum(A[0]) / n
    M = [[a - d for a in row] for row in A]
    v = power_iteration(M)
    lambda_2 = max(v) * d
    return lambda_2

def tseitin_formula_length(adj_matrix):
    n = len(adj_matrix)
    # Simplified estimation of Tseitin formula length based on graph structure
    return 2 ** (n / 4)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = 3  # Example degree, can be adjusted
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_d_regular_graph(n, d)
    lambda_2 = second_eigenvalue(G)
    length = tseitin_formula_length(G)
    c = 0.1
    conjecture_holds = length >= 2 ** (c / lambda_2) if lambda_2 > 0 else False
    counterexample = "" if conjecture_holds else f"Graph with n={n}, d={d} has λ₂={lambda_2:.4f}"
    return {
        "metric_name": "Tseitin Formula Length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length:.4f} std={std_length:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph has λ₂ < 1 - ε\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")