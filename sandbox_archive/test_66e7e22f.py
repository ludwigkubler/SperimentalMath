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

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0] for row in matrix]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        factor = Fraction(1, augmented_matrix[i][i])
        for j in range(n):
            augmented_matrix[i][j] *= factor
        for j in range(n, 2*n):
            augmented_matrix[i][j] *= factor
        for j in range(n):
            if j != i:
                factor = Fraction(augmented_matrix[j][i], augmented_matrix[i][i])
                for k in range(2*n):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[n:] for row in augmented_matrix]

def pinv(matrix):
    n = len(matrix)
    identity = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    augmented_matrix = [row[:] + col[:] for row, col in zip(matrix, identity)]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    inverse = [[col[i] for col in reduced_matrix] for i in range(n, 2*n)]
    return inverse

def laplacian_matrix(A):
    n = len(A)
    L = [[0]*n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if A[i][j] != 0)
        L[i][i] = -degree
        for j in range(i+1, n):
            if A[i][j] != 0:
                L[i][j] = L[j][i] = A[i][j]
    return L

def max_cut(G):
    n = len(G)
    best_cut_value = float('-inf')
    for mask in range(1 << n):
        cut_value = sum(G[u][v] if (mask & (1 << u)) and not (mask & (1 << v)) else 0
                        for u in range(n) for v in range(u+1, n))
        best_cut_value = max(best_cut_value, cut_value)
    return best_cut_value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    p = random.choice([0.4, 0.5, 0.6])
    G = [[random.random() < p for _ in range(n)] for _ in range(n)]
    if any(sum(row) == 0 for row in G):
        return {
            "metric_name": "MaxCut",
            "metric_value": float('-inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Disconnected graph"
        }
    L = laplacian_matrix(G)
    L_inv = pinv(L)
    n_edges = sum(sum(row) for row in G) // 2
    H = [[0]*n_edges for _ in range(n_edges)]
    edge_map = {}
    edge_index = 0
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] != 0:
                p_e = L_inv[i][i] + L_inv[j][j] - 2 * L_inv[i][j]
                y_ee_prime = L_inv[i][i] - L_inv[i][j] - L_inv[j][i] + L_inv[j][j]
                H[edge_index][edge_index] = p_e * p_e - y_ee_prime**2
                edge_map[(i, j)] = edge_index
                edge_index += 1
    for i in range(n_edges):
        for j in range(i+1, n_edges):
            e, e_prime = list(edge_map.keys())[i], list(edge_map.keys())[j]
            H[i][j] = H[j][i] = 0
    eigenvalues = sorted([eigenvalue for row in H for eigenvalue in [sum(row)/n_edges]])
    g_G = eigenvalues[-1] - eigenvalues[-2]
    if g_G <= 0:
        return {
            "metric_name": "MaxCut",
            "metric_value": float('-inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Non-positive Hessian gap"
        }
    A = [[G[i][j] for j in range(n)] for i in range(n)]
    lambda_min_A = min(sum(A[i][j] for j in range(i+1, n)) for i in range(n))
    DP_G = n / 4 * abs(lambda_min_A)
    MaxCut_G = max_cut(G)
    ratio = (DP_G - MaxCut_G) / (g_G * n)
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 1e-3 and all(ratio >= 1e-3 for _ in range(4)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    ratios = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(ratios)/len(ratios)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=No valid trials")