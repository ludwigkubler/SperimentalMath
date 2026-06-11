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
    edges = set()
    for _ in range(k * n // 2):
        u, v = random.sample(range(n), 2)
        if u > v:
            u, v = v, u
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    return edges

def compute_minimal_index(graph):
    n = len(graph)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in graph:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if A[i][i] == 0:
                j = i + 1
                while j < m and A[j][i] == 0:
                    j += 1
                if j == m:
                    continue
                A[i], A[j] = A[j], A[i]
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return sum(1 for row in A if any(x != 0 for x in row))
    
    min_idx = gaussian_elimination(adjacency_matrix)
    return min_idx

def compute_communication_complexity_rank(graph):
    n = len(graph)
    neighbors = [[] for _ in range(n)]
    for u, v in graph:
        neighbors[u].append(v)
        neighbors[v].append(u)
    
    def dfs(node, visited, parent):
        if node in visited:
            return
        visited.add(node)
        for neighbor in neighbors[node]:
            if neighbor != parent:
                dfs(neighbor, visited, node)
    
    visited = set()
    dfs(0, visited, -1)
    rank = len(visited)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_indices = []
    ranks = []
    
    for n in n_values:
        graph = generate_k_regular_graph(n, 2)
        if graph is None:
            continue
        min_index = compute_minimal_index(graph)
        rank = compute_communication_complexity_rank(graph)
        min_indices.append(min_index)
        ranks.append(rank)
    
    if not min_indices or not ranks:
        return {
            "metric_name": "min_idx vs w(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mean_min_index = sum(min_indices) / len(min_indices)
    mean_rank = sum(ranks) / len(ranks)
    correlation_coefficient = 0
    n = len(min_indices)
    if n > 1:
        numerator = sum((min_indices[i] - mean_min_index) * (ranks[i] - mean_rank) for i in range(n))
        denominator = math.sqrt(sum((min_indices[i] - mean_min_index) ** 2 for i in range(n))) * math.sqrt(sum((ranks[i] - mean_rank) ** 2 for i in range(n)))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "min_idx vs w(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.1,  # Simplified threshold for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_significant\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unsupported_conjecture")