# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det_val = 0
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (c % 2)
        sub_det = det(submatrix)
        det_val += sign * A[0][c] * sub_det
    return det_val

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_bipartite(G):
        n = len(G)
        color = [-1] * n
        queue = [0]
        color[0] = 0
        while queue:
            u = queue.pop(0)
            for v in range(n):
                if G[u][v] and color[v] == -1:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif G[u][v] and color[v] == color[u]:
                    return False
        return True
    
    def adjacency_matrix(G):
        n = len(G)
        A = [[0 for _ in range(n)] for _ in range(n)]
        for u in range(n):
            for v in range(u+1, n):
                if G[u][v]:
                    A[u][v] = 1
                    A[v][u] = 1
        return A
    
    def normalized_ihara_entropy(G):
        n = len(G)
        A = adjacency_matrix(G)
        eigenvalues = [math.eigenvalue(A)[0] for _ in range(n)]
        return (1 / n) * sum(math.log(abs(11 - 3 * λ)) for λ in eigenvalues)
    
    def dpll(T, assignment):
        if not T:
            return True
        var = next(v for v in range(len(T)) if v not in assignment)
        for val in [0, 1]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if dpll([clause for clause in T if val == 1 or all(x != -var-1 for x in clause)], new_assignment):
                return True
        return False
    
    def tseitin(G, c):
        n = len(G)
        m = sum(c[v] for v in range(n))
        T = []
        for v in range(n):
            if c[v]:
                T.append([-v-1, -m-1])
                for u in range(v+1, n):
                    if G[v][u]:
                        T.append([v+1, u+1, m+1])
                        T.append([v+1, u+1, -m-1])
                        T.append([u+1, v+1, m+1])
                        T.append([u+1, v+1, -m-1])
                T.append([-v-1, m+1])
            else:
                for u in range(v+1, n):
                    if G[v][u]:
                        T.append([v+1, u+1, m+1])
                        T.append([v+1, u+1, -m-1])
                        T.append([u+1, v+1, m+1])
                        T.append([u+1, v+1, -m-1])
                T.append([-v-1, -m-1])
        return T
    
    def max_decision_depth(T):
        n = len(G)
        assignment = {}
        depth = 0
        stack = [(T, assignment)]
        while stack:
            T, assignment = stack.pop()
            if not T:
                continue
            var = next(v for v in range(len(T)) if v not in assignment)
            for val in [0, 1]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                stack.append((T, new_assignment))
            depth += 1
        return depth
    
    n_values = [6, 8, 10, 12]
    instances_tested = 0
    d_DPLL_total = 0
    for n in n_values:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        G = [row[:] for row in G]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    G[j][i] = 1
                else:
                    G[j][i] = 0
        for _ in range(5):
            c = [random.choice([0, 1]) for _ in range(n)]
            if sum(c) % 2 == 1:
                T = tseitin(G, c)
                d_DPLL = max_decision_depth(T)
                instances_tested += 1
                d_DPLL_total += d_DPLL
    
    mean_d_DPLL = d_DPLL_total / instances_tested
    support_fraction = instances_tested / (len(n_values) * 30 * 5)
    
    return {
        "metric_name": "d_DPLL",
        "metric_value": mean_d_DPLL,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.95 and all(d_DPLL > n_values[i] * normalized_ihara_entropy(G) / 4 for i, G in enumerate(Gs)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d_DPLL = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d_DPLL} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")