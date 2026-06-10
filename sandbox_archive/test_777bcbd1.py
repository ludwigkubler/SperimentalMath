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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        
        while any(count != d for count in degree_count):
            u, v = random.sample(range(n), 2)
            if adj_matrix[u][v] == 1:
                continue
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
            degree_count[u] += 1
            degree_count[v] += 1
        
        return adj_matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(matrix[j][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def frege_proof_depth(graph):
        n = len(graph)
        stack = []
        visited = [False] * n
        
        def dfs(node):
            if visited[node]:
                return 0
            visited[node] = True
            max_depth = 0
            for neighbor in range(n):
                if graph[node][neighbor] == 1:
                    depth = dfs(neighbor)
                    if depth > max_depth:
                        max_depth = depth
            stack.append(node)
            return max_depth + 1
        
        for node in range(n):
            dfs(node)
        
        return len(stack) - n
    
    def mrank(graph):
        n = len(graph)
        incidence_matrix = [[0] * (n + n) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if graph[i][j] == 1:
                    incidence_matrix[i][i] += 1
                    incidence_matrix[j][n + i] += 1
        
        return gaussian_elimination(incidence_matrix)
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "mrank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mrank_val = mrank(graph)
    if mrank_val is None:
        return {
            "metric_name": "mrank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "gaussian_elimination_failed"
        }
    
    proof_depth = frege_proof_depth(graph)
    
    return {
        "metric_name": "mrank",
        "metric_value": mrank_val / proof_depth if proof_depth > 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(mrank_val - proof_depth) <= max(2 * min(mrank_val, proof_depth), 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if not math.isinf(res["metric_value"])) / len(results)
    std_metric_value = (sum((res["metric_value"] - mean_metric_value) ** 2 for res in results if not math.isinf(res["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")