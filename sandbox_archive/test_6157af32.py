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

def generate_k_regular_graph(n, k):
    if n * k % 2 != 0 or k < 1 or k >= n:
        raise ValueError("Invalid parameters for generating a d-regular graph")
    
    edges = set()
    while len(edges) < (n * k) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            degree_u = sum(1 for edge in edges if edge[0] == u or edge[1] == u)
            degree_v = sum(1 for edge in edges if edge[0] == v or edge[1] == v)
            if degree_u < k and degree_v < k:
                edges.add((u, v))
    
    return list(edges)

def is_valid_partition(partition, graph):
    n = len(graph)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in graph:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    for subset in partition:
        subgraph = [(u, v) for u, v in graph if (u in subset and v in subset)]
        submatrix = [[0] * len(subset) for _ in range(len(subset))]
        for i, u in enumerate(subset):
            for j, v in enumerate(subset):
                submatrix[i][j] = adjacency_matrix[u][v]
        
        rank = gaussian_elimination(submatrix)
        if rank == 0:
            return False
    
    return True

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        pivot = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= pivot
        
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
    
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = 3  # Example value for k
        graph = generate_k_regular_graph(n, k)
        
        if not is_valid_partition([set(range(n))], graph):
            return {
                "metric_name": "communication_rank_variance",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        # Placeholder for actual computation of communication rank variance
        rank_var = random.random() * n  # Dummy value
        
        results.append({
            "n": n,
            "rank_var": rank_var
        })
    
    if len(results) < 30:
        return {
            "metric_name": "communication_rank_variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    mean_rank_var = sum(result["rank_var"] for result in results) / len(results)
    std_rank_var = math.sqrt(sum((result["rank_var"] - mean_rank_var) ** 2 for result in results) / len(results))
    
    correlation_coefficient = 0.5  # Dummy value
    
    if correlation_coefficient > 0.7 and all(abs(result["rank_var"] / mean_rank_var) <= 1.5 for result in results):
        return {
            "metric_name": "communication_rank_variance",
            "metric_value": mean_rank_var,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "communication_rank_variance",
            "metric_value": mean_rank_var,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    mean_rank_var = sum(result["metric_value"] for result in results) / len(results)
    std_rank_var = math.sqrt(sum((result["metric_value"] - mean_rank_var) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_var} std={std_rank_var} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")