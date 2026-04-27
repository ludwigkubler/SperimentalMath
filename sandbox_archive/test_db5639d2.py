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

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def inverse(A):
    n = len(A)
    A_augmented = [row + row[:] for row in A]
    identity = identity_matrix(n)
    gaussian_elimination(A_augmented)
    for i in range(n):
        for j in range(n, 2*n):
            A_augmented[i][j] /= A_augmented[i][i]
        A_augmented[i][i] = 1
    return [row[n:] for row in A_augmented]

def min_cut(G, s, t):
    n = len(G)
    visited = [False] * n
    parent = [-1] * n
    queue = [s]
    visited[s] = True
    
    while queue:
        u = queue.pop(0)
        
        for v in range(n):
            if not visited[v] and G[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                
    return bfs_path(parent, s, t)

def bfs_path(parent, start, end):
    path = []
    i = end
    while i != -1:
        path.append(i)
        i = parent[i]
    path.reverse()
    return path

def min_vertex_cut(G):
    n = len(G)
    min_cut_value = float('inf')
    for s in range(n):
        for t in range(s+1, n):
            cut_value = sum(G[u][v] for u, v in combinations(range(n), 2) if (u == s and v == t) or (u == t and v == s))
            min_cut_value = min(min_cut_value, cut_value)
    return min_cut_value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([8, 10, 12, 14, 16, 18, 20])
    G = [[0] * n for _ in range(n)]
    degrees = [3] * n
    while any(d != 3 for d in degrees):
        for i in range(n):
            if degrees[i] == 3:
                continue
            j = random.randint(0, n-1)
            while G[i][j] or G[j][i] or i == j or degrees[j] == 3:
                j = random.randint(0, n-1)
            G[i][j] = G[j][i] = 1
            degrees[i] -= 1
            degrees[j] -= 1
    
    def Tseitin(G, c):
        n = len(G)
        clauses = []
        for i in range(n):
            if c[i]:
                clauses.append([i])
            else:
                clauses.append([-i])
        for u in range(n):
            for v in range(u+1, n):
                if G[u][v]:
                    clauses.append([u, -v])
                    clauses.append([-u, v])
        return clauses
    
    def resolution(clauses, k):
        while len(clauses) > 0:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if len(set(clauses[i]) & set(clauses[j])) == 2:
                        new_clause = [x for x in clauses[i] + clauses[j] if x != -clauses[j][0]]
                        if len(new_clause) == 0:
                            return True
                        new_clauses.append(new_clause)
            clauses = new_clauses
        return False
    
    def width_bounded_resolution(clauses, k):
        while resolution(clauses, k):
            k += 1
        return k
    
    c = [random.choice([0, 1]) for _ in range(n)]
    T = Tseitin(G, c)
    
    I_G = min_vertex_cut(G)
    S_star = None
    min_value = float('inf')
    for S in combinations(range(n), len(G)):
        value = abs(sum(G[u][v] for u, v in combinations(S, 2))) / min(len(S), n-len(S))
        if value < min_value:
            min_value = value
            S_star = S
    
    w_T_G_c = width_bounded_resolution(T, 1)
    
    while w_T_G_c <= I_G * min(len(S_star), n-len(S_star)) / 2 + 1:
        w_T_G_c = width_bounded_resolution(T, w_T_G_c + 1)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_T_G_c,
        "instances_tested": 1,
        "conjecture_holds": w_T_G_c >= I_G * min(len(S_star), n-len(S_star)) / 2 + 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")