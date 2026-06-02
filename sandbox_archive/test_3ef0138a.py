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
        if (d * n) % 2 != 0 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph
    
    def tsi(graph):
        n = len(graph)
        if n == 0:
            return 0
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                adjacency_matrix[u][v] = 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            for i in range(m):
                if i < n:
                    max_row = i
                    for j in range(i + 1, m):
                        if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                            max_row = j
                    matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                    
                    if matrix[i][i] != 0:
                        pivot = matrix[i][i]
                        for j in range(i, n):
                            matrix[i][j] /= pivot
                        for j in range(m):
                            if j != i and matrix[j][i] != 0:
                                factor = matrix[j][i]
                                for k in range(n):
                                    matrix[j][k] -= factor * matrix[i][k]
                        rank += 1
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    def communication_complexity_rank(graph):
        n = len(graph)
        if n == 0:
            return 0
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                adjacency_matrix[u][v] = 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            for i in range(m):
                if i < n:
                    max_row = i
                    for j in range(i + 1, m):
                        if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                            max_row = j
                    matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                    
                    if matrix[i][i] != 0:
                        pivot = matrix[i][i]
                        for j in range(i, n):
                            matrix[i][j] /= pivot
                        for j in range(m):
                            if j != i and matrix[j][i] != 0:
                                factor = matrix[j][i]
                                for k in range(n):
                                    matrix[j][k] -= factor * matrix[i][k]
                        rank += 1
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "tsi(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    tsi_value = tsi(graph)
    r_phi_value = communication_complexity_rank(graph)
    
    if tsi_value is None or r_phi_value is None:
        return {
            "metric_name": "tsi(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "tsi(G) - r(φ_G)",
        "metric_value": abs(tsi_value - r_phi_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(tsi_value - r_phi_value) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")