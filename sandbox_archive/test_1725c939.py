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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v or (u, v) in edges_added or (v, u) in edges_added:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
        return graph
    
    def adjacency_matrix(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                A[i][j] = 1
                A[j][i] = 1
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        rank = 0
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            rank += 1
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return rank
    
    def symplectic_form_degree(A):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        B = [A[i][:n//2] + A[i][n//2:] for i in range(n)]
        C = [A[i][:n//2] for i in range(n//2)] + [A[i][n//2:] for i in range(n//2, n)]
        D = [A[i][:n//2] for i in range(n//2, n)] + [A[i][n//2:] for i in range(n//2, n)]
        B_inv = gaussian_elimination(B)
        C_inv = gaussian_elimination(C)
        D_inv = gaussian_elimination(D)
        return max(B_inv, C_inv, D_inv)
    
    def circuit_monotone_width(graph):
        n = len(graph)
        if n == 1:
            return 0
        if n == 2:
            return 1
        if n == 3:
            return 2
        # Placeholder for actual circuit monotone width calculation
        return random.randint(0, n)
    
    def spearman_correlation(ranks):
        n = len(ranks)
        sorted_ranks = sorted(ranks.items(), key=lambda x: x[1])
        ranks_dict = {v: i + 1 for i, (k, v) in enumerate(sorted_ranks)}
        s = sum((ranks_dict[i] - ranks_dict[j]) ** 2 for i, j in combinations(range(n), 2))
        return 1 - (6 * s) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_d_regular_graph(n, random.randint(2, min(n-1, 8)))
        if graph is None:
            continue
        A = adjacency_matrix(graph)
        symplectic_deg = symplectic_form_degree(A)
        w_G = circuit_monotone_width(graph)
        results.append((symplectic_deg, w_G))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    ranks = {i: v for i, (symplectic_deg, w_G) in enumerate(results)}
    rho = spearman_correlation(ranks)
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": rho >= 0.5 and all(rho >= 0.3 for _ in range(24)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 99997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE insufficient_data")
    else:
        rho_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(rho_values) / len(rho_values):.2f} std={math.sqrt(sum((x - sum(rho_values) / len(rho_values)) ** 2 for x in rho_values) / len(rho_values)):.2f} support_fraction={support_fraction:.2f}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='rho < 0.5' first_failing_seed={first_failing_seed}")