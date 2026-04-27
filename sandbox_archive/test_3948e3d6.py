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

def is_connected(G):
    visited = [False] * len(G)
    stack = [0]
    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = True
            for v in range(len(G)):
                if G[u][v] and not visited[v]:
                    stack.append(v)
    return all(visited)

def is_3_regular(G):
    return all(sum(G[u]) == 3 for u in range(len(G)))

def adjacency_matrix_to_laplacian(A):
    n = len(A)
    D = [sum(row) for row in A]
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                L[i][j] = D[i]
            else:
                L[i][j] = -A[i][j]
    return L

def gaussian_elimination(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(M[k][i]))
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i + 1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x

def solve_linear_system(A, b):
    n = len(A)
    if not is_square_matrix(A) or len(b) != n:
        raise ValueError("Invalid input dimensions")
    if not is_invertible(A):
        raise ValueError("Matrix is not invertible")
    return gaussian_elimination(A, b)

def max_decision_depth(T):
    def dpll(assignment, clause_index):
        if clause_index == len(T):
            return 0
        for var in range(len(T)):
            if var not in assignment:
                new_assignment = assignment.copy()
                new_assignment[var] = True
                if all(any(new_assignment[j] for j in clause) for clause in T[clause_index]):
                    depth_true = dpll(new_assignment, clause_index + 1)
                    if depth_true == float('inf'):
                        return float('inf')
                    new_assignment[var] = False
                    depth_false = dpll(new_assignment, clause_index + 1)
                    if depth_false == float('inf'):
                        return float('inf')
                    return max(depth_true, depth_false) + 1
        return float('inf')
    return dpll({}, 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [6, 8, 10, 12]
    results = []
    
    for n in n_values:
        G = [[0] * n for _ in range(n)]
        while not is_connected(G) or not is_3_regular(G):
            for u in range(n):
                neighbors = [v for v in range(n) if G[u][v]]
                if len(neighbors) < 2:
                    continue
                v, w = random.sample(neighbors, 2)
                G[u][v] = G[v][u] = 1
                G[u][w] = G[w][u] = 1
        
        A_G = [row[:] for row in G]
        λs = sorted(math.eigenvalsh(A_G), reverse=True)
        η_G = sum(math.log(abs(11 - 3 * λ)) for λ in λs) / n
        η_G /= len(G)
        
        for _ in range(5):
            c = [random.randint(0, 1) for _ in range(n)]
            if sum(c) % 2 != 1:
                continue
            
            T = []
            for u in range(n):
                for v in range(u + 1, n):
                    if G[u][v]:
                        T.append([u * 3 + i - 1 for i in range(4)])
                        T.append([v * 3 + i - 1 for i in range(4)])
            
            d_DPLL = max_decision_depth(T)
            results.append((n, η_G, d_DPLL))
    
    total_d_DPLL = sum(d_DPLL for _, _, d_DPLL in results)
    avg_d_DPLL = total_d_DPLL / len(results)
    std_d_DPLL = math.sqrt(sum((d_DPLL - avg_d_DPLL) ** 2 for _, _, d_DPLL in results) / len(results))
    
    support_fraction = sum(1 for n, η_G, d_DPLL in results if d_DPLL >= n * η_G / 4) / len(results)
    
    conjecture_holds = support_fraction >= 0.95
    counterexample = "" if conjecture_holds else "d_DPLL < |V|·η(G)/4"
    
    return {
        "metric_name": "d_DPLL",
        "metric_value": avg_d_DPLL,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    avg_d_DPLL = sum(result["metric_value"] for result in results) / len(results)
    std_d_DPLL = math.sqrt(sum((result["metric_value"] - avg_d_DPLL) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={avg_d_DPLL} std={std_d_DPLL} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"d_DPLL < |V|·η(G)/4\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")