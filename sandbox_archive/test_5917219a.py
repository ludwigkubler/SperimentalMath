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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank:
                    factor = -A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def min_hodge_cohomology(G):
        n = len(G)
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in G:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        laplacian = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(adj_matrix[i][j] for j in range(n))
            laplacian[i][i] = degree
            for j in range(i + 1, n):
                laplacian[i][j] = -adj_matrix[i][j]
                laplacian[j][i] = -adj_matrix[i][j]
        
        return gaussian_elimination(laplacian)
    
    def circuit_monotone_width(G):
        n = len(G)
        max_width = 0
        for i in range(n):
            width = 1
            visited = [False] * n
            stack = [i]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    for v in G[u]:
                        if not visited[v]:
                            stack.append(v)
                            width += 1
            max_width = max(max_width, width)
        return max_width
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        
        G = [[] for _ in range(n)]
        edges_added = set()
        for u in range(n):
            for v in range(u + 1, n):
                if len(G[u]) < d and len(G[v]) < d:
                    if (u, v) not in edges_added and (v, u) not in edges_added:
                        G[u].append(v)
                        G[v].append(u)
                        edges_added.add((u, v))
        
        return G
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    w_values = []
    
    for n in n_values:
        for _ in range(5):
            d = random.randint(2, n - 1)
            G = generate_d_regular_graph(n, d)
            h = min_hodge_cohomology(G)
            w = circuit_monotone_width(G)
            h_values.append(h)
            w_values.append(w)
    
    if len(h_values) < 30:
        return {
            "metric_name": "Minimal Hodge Cohomology and Circuit Monotone Width",
            "metric_value": None,
            "instances_tested": len(h_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    h_avg = sum(h_values) / len(h_values)
    w_avg = sum(w_values) / len(w_values)
    correlation_coefficient = sum((h - h_avg) * (w - w_avg) for h, w in zip(h_values, w_values)) / len(h_values)
    
    if correlation_coefficient >= 0.7 and all(1.2 * w <= h <= 0.8 * w for h, w in zip(h_values, w_values)):
        return {
            "metric_name": "Minimal Hodge Cohomology and Circuit Monotone Width",
            "metric_value": correlation_coefficient,
            "instances_tested": len(h_values),
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Minimal Hodge Cohomology and Circuit Monotone Width",
            "metric_value": correlation_coefficient,
            "instances_tested": len(h_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Correlation: {correlation_coefficient}, H values out of range"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation out of range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")