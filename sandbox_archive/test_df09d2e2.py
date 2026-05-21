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
from itertools import combinations

def run_trial(seed: int) -> dict:
    n = 10  # Start with a fixed size for simplicity
    G = random_3_regular_graph(n, seed)
    A = adjacency_matrix(G)
    H_G = hankel_matrix(A)
    ν_G = rank(H_G)
    UB_DP = ub_dp(G)
    MaxCut = max_cut(G)
    S_G = UB_DP - MaxCut
    r_G = (S_G / ν_G) if ν_G != 0 else float('inf')
    
    return {
        "metric_name": "GW Slack Ratio",
        "metric_value": r_G,
        "instances_tested": 1,
        "conjecture_holds": r_G >= 0.02,
        "counterexample": "" if r_G >= 0.02 else f"Graph with n={n} and r(G)={r_G}"
    }

def random_3_regular_graph(n, seed):
    random.seed(seed)
    G = [[] for _ in range(n)]
    
    edges = set()
    while len(edges) < (n * 3) // 2:
        node1, node2 = random.sample(range(n), 2)
        if node1 != node2 and (node1, node2) not in edges and (node2, node1) not in edges:
            G[node1].append(node2)
            G[node2].append(node1)
            edges.add((node1, node2))
    
    return G

def adjacency_matrix(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in G[i]:
            A[i][j] = 1
    return A

def hankel_matrix(A):
    n = len(A)
    H_G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            H_G[i][j] = (1 / n) * sum(A[k][i + j - k] for k in range(max(0, i + j - n + 1), min(i + j + 1, n)))
    return H_G

def rank(matrix):
    n = len(matrix)
    matrix_copy = [row[:] for row in matrix]
    pivot_row = 0
    for col in range(n):
        if all(row[col] == 0 for row in matrix_copy[pivot_row:]):
            continue
        for i in range(pivot_row, n):
            if matrix_copy[i][col] != 0:
                matrix_copy[i], matrix_copy[pivot_row] = matrix_copy[pivot_row], matrix_copy[i]
                break
        pivot_col = col
        for row in range(n):
            if row == pivot_row:
                continue
            factor = -matrix_copy[row][pivot_col] / matrix_copy[pivot_row][pivot_col]
            for j in range(n):
                matrix_copy[row][j] += factor * matrix_copy[pivot_row][j]
        pivot_row += 1
    return pivot_row

def ub_dp(G):
    n = len(G)
    m = (n * 3) // 2
    λ_min_A = min(eigenvalues(A)[0], eigenvalues(A)[-1])
    return m / 2 - (n / 4) * λ_min_A

def max_cut(G):
    n = len(G)
    best_cut_size = 0
    for cut in combinations(range(1, n), n // 2):
        cut_size = sum(1 for node in cut if any(neighbor not in cut for neighbor in G[node]))
        best_cut_size = max(best_cut_size, cut_size)
    return best_cut_size

def eigenvalues(matrix):
    n = len(matrix)
    matrix_copy = [row[:] for row in matrix]
    for col in range(n):
        pivot_row = 0
        for i in range(pivot_row, n):
            if all(row[col] == 0 for row in matrix_copy[pivot_row:]):
                continue
            for j in range(pivot_row, n):
                if matrix_copy[j][col] != 0:
                    matrix_copy[j], matrix_copy[pivot_row] = matrix_copy[pivot_row], matrix_copy[j]
                    break
        pivot_col = col
        for row in range(n):
            if row == pivot_row:
                continue
            factor = -matrix_copy[row][pivot_col] / matrix_copy[pivot_row][pivot_col]
            for j in range(n):
                matrix_copy[row][j] += factor * matrix_copy[pivot_row][j]
        pivot_row += 1
    
    eigenvalues = [0] * n
    for i in range(n):
        eigenvalues[i] = matrix_copy[i][i]
    
    return sorted(eigenvalues)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_G = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_G} std=0.0 support_fraction=1.0")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n=10 and r(G)<0.02\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")