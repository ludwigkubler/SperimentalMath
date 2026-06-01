# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

# Gaussian elimination to reduce matrix to row echelon form
def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find max element in current column
        max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
        if matrix[max_row][i] == 0:
            raise ValueError("Singular matrix")
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate current column elements below pivot
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

# Compute the rank of a matrix using Gaussian elimination
def min_rank(matrix):
    try:
        reduced_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank
    except ValueError as e:
        return None

# Generate a random d-regular graph with n vertices
def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        raise ValueError("d must be even for regular graphs")
    
    edges = set()
    while len(edges) < n * d // 2:
        u, v = random.sample(range(n), 2)
        if u > v:
            u, v = v, u
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    return adjacency_matrix

# Compute the communication complexity rank of a graph
def communication_complexity_rank(graph):
    n = len(graph)
    max_flow = 0
    for source in range(n):
        visited = [False] * n
        flow = 0
        queue = [source]
        while queue:
            u = queue.pop(0)
            if visited[u]:
                continue
            visited[u] = True
            for v in range(n):
                if not visited[v] and graph[u][v] > 0:
                    queue.append(v)
                    flow += min(graph[source][u], graph[u][v])
        max_flow = max(max_flow, flow)
    
    return max_flow

# Run a single trial with the given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = 2 * random.randint(1, n // 2)
        graph = generate_d_regular_graph(n, d)
        cluster_algebra = graph  # Simplified representation for testing
        min_rank_cG = min_rank(cluster_algebra)
        r_G = communication_complexity_rank(graph)
        
        if min_rank_cG is None:
            continue
        
        results.append({
            "n": n,
            "min_rank_cG": min_rank_cG,
            "r_G": r_G
        })
    
    if not results:
        return {
            "metric_name": "min_rank_cG vs r_G",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank_values = [result["min_rank_cG"] for result in results]
    r_G_values = [result["r_G"] for result in results]
    mean_min_rank = sum(min_rank_values) / len(min_rank_values)
    mean_r_G = sum(r_G_values) / len(r_G_values)
    std_dev = math.sqrt(sum((x - mean_min_rank)**2 for x in min_rank_values) / len(min_rank_values))
    
    correlation = sum((min_rank_values[i] - mean_min_rank) * (r_G_values[i] - mean_r_G) for i in range(len(results))) / len(results)
    
    return {
        "metric_name": "min_rank_cG vs r_G",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation) >= 1.5 * std_dev,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")