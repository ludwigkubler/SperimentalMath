# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
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

    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1] / A[i][i]
        for j in range(i-1, -1, -1):
            A[j][-1] -= A[j][i] * x[i]

    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def laplacian_eigenvalues(G):
    n = len(G)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(G[i])
        D[i][i] = degree
    L = matrix_multiply(D, G)
    eigenvalues = gaussian_elimination(L)
    return sorted(eigenvalues, reverse=True)

def max_cut(graph):
    n = len(graph)
    best_cut_value = 0
    
    for i in range(1 << (n-1)):
        cut_value = 0
        for j in range(n):
            for k in range(j+1, n):
                if (i >> j) & 1 and (i >> k) & 1:
                    cut_value += graph[j][k]
                elif not ((i >> j) & 1) and not ((i >> k) & 1):
                    cut_value -= graph[j][k]
        best_cut_value = max(best_cut_value, abs(cut_value))
    
    return best_cut_value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16]
    k_values = [3, 4]
    results = []
    
    for n in n_values:
        for k in k_values:
            graph = [[0] * n for _ in range(n)]
            degree_sum = 0
            while degree_sum != n * k:
                u = random.randint(0, n-1)
                v = random.randint(0, n-1)
                if u == v or graph[u][v] == 1:
                    continue
                graph[u][v] = 1
                graph[v][u] = 1
                degree_sum += 2
            
            eigenvalues = laplacian_eigenvalues(graph)
            h_G = len([e for e in eigenvalues if e != 0])
            lambda_max = max(eigenvalues)
            MC_G = max_cut(graph)
            rho_G = n * lambda_max / (4 * MC_G) - 1
            r = n * rho_G / (h_G * math.log2(n+1))
            
            results.append(r)
    
    metric_value = max(results)
    conjecture_holds = metric_value < 2
    counterexample = "" if conjecture_holds else f"max_r={metric_value}"
    
    return {
        "metric_name": "n·ρ(G)/(h(G)·log_2(n+1))",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial["metric_value"])
    
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r < 2) / len(results)
    
    if all(r < 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(r >= 2 for r in results):
        first_failing_seed = next(seed for seed, trial in enumerate(results) if trial["metric_value"] >= 2)
        print(f"RESULT: FALSIFIED counterexample=\"max_r={results[first_failing_seed]}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")