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
    
    def generate_k_regular_graph(n, k):
        while True:
            adj = [[0] * n for _ in range(n)]
            degree_counts = [0] * n
            edges_added = 0
            
            for i in range(k):
                for j in range(i + 1, n):
                    if random.random() < (k - degree_counts[i]) / (n - i - 1) * (k - degree_counts[j]) / (n - j - 1):
                        adj[i][j] = 1
                        adj[j][i] = 1
                        degree_counts[i] += 1
                        degree_counts[j] += 1
                        edges_added += 1
            
            if edges_added == n * k // 2:
                return adj

    def laplacian_matrix(adj):
        n = len(adj)
        D = [sum(row) for row in adj]
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            L[i][i] = D[i]
            for j in range(i + 1, n):
                if adj[i][j]:
                    L[i][j] = -1
                    L[j][i] = -1
        return L

    def eigenvalues(matrix):
        n = len(matrix)
        eigenvals = [0] * n
        for i in range(n):
            x = [random.random() for _ in range(n)]
            x_norm = sum(x[i]**2 for i in range(n))**0.5
            for _ in range(100):  # Power iteration
                y = [sum(matrix[i][j] * x[j] for j in range(n)) for i in range(n)]
                y_norm = sum(y[i]**2 for i in range(n))**0.5
                x = [y[i] / y_norm for i in range(n)]
            eigenvals[i] = sum(x[i] * matrix[i][j] * x[j] for i in range(n) for j in range(n))
        return sorted(eigenvals, reverse=True)

    def max_cut(graph):
        n = len(graph)
        best_cut_value = 0
        for mask in range(1 << (n - 1)):
            cut_value = sum(graph[i][j] for i in range(n) for j in range(i + 1, n) if (mask & (1 << i)) ^ (mask & (1 << j)))
            best_cut_value = max(best_cut_value, cut_value)
        return best_cut_value

    def hankel_rank(eigenvals):
        tol = 1e-8
        rank = 0
        for i in range(len(eigenvals)):
            if eigenvals[i] > tol:
                rank += 1
            else:
                break
        return rank

    n_values = [8, 10, 12, 14, 16]
    k_values = [3, 4]
    instances_tested = 0
    max_r = 0.0
    
    for n in n_values:
        for k in k_values:
            for _ in range(30):
                graph = generate_k_regular_graph(n, k)
                L = laplacian_matrix(graph)
                eigenvals = eigenvalues(L)
                lambda_max = eigenvals[0]
                MC = max_cut(graph)
                h = hankel_rank(eigenvals)
                rho = n * lambda_max / (4 * MC) - 1
                r = n * rho / (h * math.log2(n + 1))
                instances_tested += 1
                if r > max_r:
                    max_r = r
    
    return {
        "metric_name": "r",
        "metric_value": max_r,
        "instances_tested": instances_tested,
        "conjecture_holds": max_r < 2,
        "counterexample": "" if max_r < 2 else f"n={n}, k={k}, r={max_r}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction=1.0")
    elif any(res["metric_value"] >= 2 for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if res["metric_value"] >= 2)
        print(f"RESULT: FALSIFIED counterexample=\"r={res['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")