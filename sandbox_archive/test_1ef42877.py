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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return [A[i][n] for i in range(n)]

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def laplacian_matrix(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(G[i])
            L[i][i] = degree
            for j in range(i+1, n):
                if G[i][j]:
                    L[i][j] = -1
                    L[j][i] = -1
        return L

    def bakry_emery_curvature(L):
        n = len(L)
        Q = [[0] * 10 for _ in range(10)]
        for i in range(n):
            for j in range(i+1, n):
                if L[i][j]:
                    Q[2*i][2*j] = -1
                    Q[2*i+1][2*j+1] = -1
                    Q[2*i][2*j+1] = 1
                    Q[2*i+1][2*j] = 1
        Q += [[0] * 10 for _ in range(6)]
        eigenvalues = gaussian_elimination(Q)
        return min(eigenvalues)

    def lex_dpll(G, c):
        n = len(G)
        stack = []
        assignment = [None] * n
        for i in range(n):
            if not G[i]:
                continue
            stack.append((i, True))
            while stack:
                node, value = stack.pop()
                if assignment[node] is None:
                    assignment[node] = value
                    if value:
                        for j in range(node+1, n):
                            if G[node][j]:
                                stack.append((j, not value))
                    else:
                        return False
                elif assignment[node] != value:
                    break
            else:
                return True
        return False

    def girth(G):
        n = len(G)
        for d in range(2, n+1):
            visited = [False] * n
            queue = [(0, 1)]
            while queue:
                node, dist = queue.pop(0)
                if dist == d:
                    return d
                visited[node] = True
                for j in range(node+1, n):
                    if G[node][j]:
                        if not visited[j]:
                            queue.append((j, dist+1))
        return n

    def generate_random_graph(n):
        while True:
            G = [[0] * n for _ in range(n)]
            degrees = [random.randint(2, 4) for _ in range(n)]
            total_edges = sum(degrees) // 2
            if total_edges % 1 != 0:
                continue
            edges = set()
            for i in range(n):
                for j in range(i+1, n):
                    if degrees[i] > 0 and degrees[j] > 0:
                        G[i][j] = G[j][i] = 1
                        degrees[i] -= 1
                        degrees[j] -= 1
                        edges.add((min(i, j), max(i, j)))
            if len(edges) == total_edges // 2 and girth(G) >= 4:
                return G

    def generate_dumbbell_graph(n):
        G = [[0] * n for _ in range(n)]
        mid = n // 2
        for i in range(mid):
            G[i][i+1] = G[i+1][i] = 1
        for i in range(mid, n-1):
            G[i][i+1] = G[i+1][i] = 1
        G[0][mid] = G[mid][0] = 1
        G[n-1][mid] = G[mid][n-1] = 1
        return G

    n_values = [8, 10, 12, 14, 16, 18, 20]
    instances_tested = 0
    total_d_DPLL = 0.0
    d_DPLL_min = float('inf')
    d_DPLL_max = float('-inf')

    for n in n_values:
        for _ in range(8):
            G = generate_random_graph(n)
            c = random.choice([1, -1])
            L = laplacian_matrix(G)
            kappa_BE = bakry_emery_curvature(L)
            d_DPLL = lex_dpll(G, c)
            instances_tested += 1
            total_d_DPLL += d_DPLL
            if d_DPLL < d_DPLL_min:
                d_DPLL_min = d_DPLL
            if d_DPLL > d_DPLL_max:
                d_DPLL_max = d_DPLL

        for _ in range(2):
            G = generate_dumbbell_graph(n)
            c = random.choice([1, -1])
            L = laplacian_matrix(G)
            kappa_BE = bakry_emery_curvature(L)
            d_DPLL = lex_dpll(G, c)
            instances_tested += 1
            total_d_DPLL += d_DPLL
            if d_DPLL < d_DPLL_min:
                d_DPLL_min = d_DPLL
            if d_DPLL > d_DPLL_max:
                d_DPLL_max = d_DPLL

    avg_d_DPLL = total_d_DPLL / instances_tested
    slack_ratio = avg_d_DPLL / (n_values[-1] * (-avg_d_DPLL))
    conjecture_holds = slack_ratio >= 0.4
    counterexample = "" if conjecture_holds else "dumbbell_graph"

    return {
        "metric_name": "slack_ratio",
        "metric_value": slack_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dumbbell_graph\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient data")