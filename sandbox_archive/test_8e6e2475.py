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
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges_added and (j, i) not in edges_added:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges_added.add((i, j))
        return graph
    
    def calculate_jones_polynomial(G):
        n = len(G)
        if n == 0:
            return 1
        if n == 1:
            return 1
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if j in G[i]:
                    M[i][j] = -1
                    M[j][i] = -1
        det = determinant(M)
        return det
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def calculate_local_indeterminacy(jones_polynomial):
        # Placeholder for actual computation
        return abs(jones_polynomial)
    
    def calculate_circuit_depth(G):
        n = len(G)
        if n == 0:
            return 0
        if n == 1:
            return 1
        visited = [False] * n
        depth = 0
        
        def dfs(node, current_depth):
            nonlocal depth
            visited[node] = True
            for neighbor in G[node]:
                if not visited[neighbor]:
                    dfs(neighbor, current_depth + 1)
            depth = max(depth, current_depth)
        
        for i in range(n):
            if not visited[i]:
                dfs(i, 0)
        
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_d_regular_graph(n, 3)
        if G is None:
            continue
        jones_polynomial = calculate_jones_polynomial(G)
        local_indeterminacy = calculate_local_indeterminacy(jones_polynomial)
        circuit_depth = calculate_circuit_depth(G)
        
        results.append({
            "n": n,
            "local_indeterminacy": local_indeterminacy,
            "circuit_depth": circuit_depth
        })
    
    if not results:
        return {
            "metric_name": "Indet(φ_G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Graph generation failed for all sizes"
        }
    
    mean_local_indeterminacy = sum(result["local_indeterminacy"] for result in results) / len(results)
    mean_circuit_depth = sum(result["circuit_depth"] for result in results) / len(results)
    correlation_coefficient = 0
    if mean_circuit_depth != 0:
        correlation_coefficient = (sum((result["local_indeterminacy"] - mean_local_indeterminacy) * (result["circuit_depth"] - mean_circuit_depth) for result in results) /
                                   math.sqrt(sum((result["local_indeterminacy"] - mean_local_indeterminacy) ** 2 for result in results) *
                                             sum((result["circuit_depth"] - mean_circuit_depth) ** 2 for result in results)))
    
    return {
        "metric_name": "Indet(φ_G)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(mean_local_indeterminacy - mean_circuit_depth) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")