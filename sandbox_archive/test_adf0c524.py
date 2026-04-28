# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3_regular_graph(n):
        while True:
            edges = set()
            for i in range(n):
                neighbors = [j for j in range(n) if j != i]
                random.shuffle(neighbors)
                for j in neighbors[:2]:
                    edge = tuple(sorted((i, j)))
                    if (edge[1], edge[0]) not in edges:
                        edges.add(edge)
            if len(edges) == n * 3 // 2 and all(len(set(v for u, v in edges if u == i)) == 2 for i in range(n)):
                return [set() for _ in range(n)], list(edges)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def laplacian_matrix(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(1 for j in G[i] if (i, j) in edges or (j, i) in edges)
            L[i][i] = -degree
            for j in G[i]:
                if (i, j) in edges:
                    L[i][j] = 1
        return L
    
    def eigenvalues(A):
        n = len(A)
        A = [[A[i][j] for j in range(n)] for i in range(n)]
        Q = [[0] * n for _ in range(n)]
        R = [[0] * n for _ in range(n)]
        for k in range(n):
            Q[k][k] = 1
            r = [A[i][k] / A[k][k] if i != k else 0 for i in range(k + 1, n)]
            R[k] = r[:]
            for j in range(k + 1, n):
                A[j][k] -= sum(Q[j][i] * R[i][k] for i in range(k))
        Q = gaussian_elimination(Q)
        R = gaussian_elimination(R)
        eigenvals = [R[i][i] for i in range(n)]
        return eigenvals
    
    def lex_dpll(T, assignment):
        if not T:
            return True
        var = next(v for v in range(len(T)) if v not in assignment)
        for val in (0, 1):
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if all(new_assignment[v] == (T[v][i] ^ new_assignment[i]) % 2 for i in range(len(T[v]))):
                if lex_dpll([t for t in T if var not in t], new_assignment):
                    return True
        return False
    
    def d_DPLL(T, c):
        assignment = [None] * len(T)
        return lex_dpll(T, assignment)
    
    n = random.choice([8, 10, 12, 14, 16, 18, 20])
    G, edges = generate_3_regular_graph(n)
    L = laplacian_matrix(G)
    eigenvals = sorted(eigenvalues(L))
    kappa_BE = min(eigenvals[2:]) if len(eigenvals) > 2 else float('inf')
    kappa_bar_G = kappa_BE / n
    T = [[(i, j) for j in G[i] if (i, j) in edges or (j, i) in edges] for i in range(n)]
    c = random.choice([0, 1])
    d_DPLL_val = d_DPLL(T, c)
    
    return {
        "metric_name": "slack_ratio",
        "metric_value": d_DPLL_val / (n * (-kappa_bar_G)),
        "instances_tested": 1,
        "conjecture_holds": d_DPLL_val >= 0.4 * n * (-kappa_bar_G),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_slack_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_slack_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slack_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slack_ratio < 0.4\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")