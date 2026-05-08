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

def add_mod2(a, b):
    return (a + b) % 2

def multiply_mod2(a, b):
    return (a * b) % 2

def matrix_multiply_mod2(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] = add_mod2(C[i][j], multiply_mod2(A[i][l], B[l][j]))
    return C

def gaussian_elimination_mod2(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        pivot_row = -1
        for j in range(rank, m):
            if matrix[j][i] == 1:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for j in range(n):
            if j != i and matrix[rank][j] == 1:
                matrix[rank] = [add_mod2(matrix[rank][k], matrix[j][k]) for k in range(n)]
        rank += 1
    return rank

def slice_rank_upper_bound(T_P):
    m, n = len(T_P), len(T_P[0])
    rank = 0
    while True:
        max_reduction = -1
        axis = None
        vector = None
        for i in range(3):
            reduction = sum(sum(row[j] for row in T_P) for j in range(n)) if i == 0 else \
                       sum(sum(T_P[i][j] for i in range(m)) for j in range(n)) if i == 1 else \
                       sum(sum(T_P[i][j] for i in range(m)) for j in range(n))
            if reduction > max_reduction:
                max_reduction = reduction
                axis = i
        if max_reduction <= rank:
            break
        vector = [sum(T_P[i][j] for i in range(m)) if axis == 0 else \
                  sum(T_P[i][j] for j in range(n)) if axis == 1 else \
                  sum(T_P[i][j] for j in range(n)) for i in range(m)]
        for i in range(m):
            T_P[i] = [add_mod2(T_P[i][j], multiply_mod2(vector[j], vector[i])) for j in range(n)]
        rank += 1
    return rank

def generate_read_twice_bp(n, width):
    V = list(range(2 * n))
    edges = []
    for i in range(n):
        u = random.choice(V)
        v = random.choice(V)
        while u == v:
            v = random.choice(V)
        edges.append((u, v, i % width))
    return edges

def generate_ip2_bp(n):
    V = list(range(2 * n))
    edges = []
    for i in range(n):
        u = 2 * i
        v = 2 * i + 1
        edges.append((u, v, i))
    return edges

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    # Read-twice BPs
    for n in [6, 8, 10, 12, 14, 16, 18, 20]:
        for width in [2, 3, 4]:
            V = list(range(2 * n))
            edges = generate_read_twice_bp(n, width)
            T_P = [[0] * (n + 1) for _ in range(n + 1)]
            for u, v, j in edges:
                T_P[u][v][j] = 1
            rho = slice_rank_upper_bound(T_P)
            results.append({"metric_name": "rho", "metric_value": rho, "instances_tested": 1, "conjecture_holds": rho <= 6 * math.ceil(math.log2(n + 1)), "counterexample": ""})
    
    # IP_2 BPs
    for n in [4, 6, 8, 10, 12]:
        V = list(range(2 * n))
        edges = generate_ip2_bp(n)
        T_P = [[0] * (n + 1) for _ in range(n + 1)]
        for u, v, j in edges:
            T_P[u][v][j] = 1
        rho = slice_rank_upper_bound(T_P)
        results.append({"metric_name": "rho", "metric_value": rho, "instances_tested": 1, "conjecture_holds": rho >= n / 8, "counterexample": ""})
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    rho_values = [r["metric_value"] for r in all_results if r["metric_name"] == "rho"]
    conjecture_holds = all(r["conjecture_holds"] for r in all_results)
    
    if conjecture_holds:
        support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
        print(f"RESULT: SUPPORTED mean={sum(rho_values)/len(rho_values):.2f} std={math.sqrt(sum((x - sum(rho_values)/len(rho_values))**2 for x in rho_values) / len(rho_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        counterexample = next(r["counterexample"] for r in all_results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")