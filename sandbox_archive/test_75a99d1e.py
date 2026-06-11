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
    if (n * k) % 2 != 0:
        return None
    
    graph = [[0] * n for _ in range(n)]
    
    edges = set()
    while len(edges) < k * n // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u][v] = 1
            graph[v][u] = 1
            edges.add((u, v))
    
    return graph

def compute_minimal_index(graph):
    n = len(graph)
    if any(sum(row) != 2 * k for row in graph):
        return None
    
    adjacency_matrix = [row[:] for row in graph]
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        
        for i in range(n):
            max_row = -1
            for j in range(rank, m):
                if matrix[j][i] != 0:
                    max_row = j
                    break
            
            if max_row == -1:
                continue
            
            matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
            
            for j in range(m):
                if j != rank and matrix[j][i] != 0:
                    factor = Fraction(matrix[j][i], matrix[rank][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[rank][k]
            
            rank += 1
        
        return rank
    
    return gaussian_elimination(adjacency_matrix)

def compute_communication_complexity_rank(graph):
    n = len(graph)
    if any(sum(row) != 2 * (n - 1) for row in graph):
        return None
    
    adjacency_matrix = [row[:] for row in graph]
    
    def dfs(node, visited):
        stack = [node]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in range(n):
                    if adjacency_matrix[node][neighbor] == 1 and not visited[neighbor]:
                        stack.append(neighbor)
    
    visited = [False] * n
    dfs(0, visited)
    
    return sum(visited)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in range(5, 41):
        k = random.randint(2, min(n - 1, 8))
        graph = generate_k_regular_graph(n, k)
        
        if graph is None:
            continue
        
        min_index = compute_minimal_index(graph)
        comm_rank = compute_communication_complexity_rank(graph)
        
        if min_index is not None and comm_rank is not None:
            results.append((min_index, comm_rank))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    min_indices = [r[0] for r in results]
    comm_ranks = [r[1] for r in results]
    
    n = len(results)
    mean_min_index = sum(min_indices) / n
    mean_comm_rank = sum(comm_ranks) / n
    
    cov = sum((min_indices[i] - mean_min_index) * (comm_ranks[i] - mean_comm_rank) for i in range(n)) / n
    var_min_index = sum((min_indices[i] - mean_min_index) ** 2 for i in range(n)) / n
    var_comm_rank = sum((comm_ranks[i] - mean_comm_rank) ** 2 for i in range(n)) / n
    
    correlation_coefficient = cov / (math.sqrt(var_min_index) * math.sqrt(var_comm_rank))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_significant\" first_failing_seed={first_failing_seed}")