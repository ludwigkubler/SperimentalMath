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
from itertools import combinations

def generate_k_regular_graph(n, k):
    if (n * k) % 2 != 0:
        return None
    edges = set()
    nodes = list(range(n))
    for _ in range(k * n // 2):
        u, v = random.sample(nodes, 2)
        if u < v and (u, v) not in edges:
            edges.add((u, v))
    return {u: [v for v in nodes if (u, v) in edges] for u in nodes}

def compute_minimal_index(graph):
    n = len(graph)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, neighbors in graph.items():
        for v in neighbors:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = -1
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            for j in range(rows):
                if j != rank - 1 and matrix[j][i] != 0:
                    factor = Fraction(matrix[j][i], matrix[rank - 1][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[rank - 1][k]
        return rank
    
    min_idx = gaussian_elimination(adjacency_matrix)
    return min_idx

def compute_communication_complexity_rank(graph):
    n = len(graph)
    edges = set()
    for neighbors in graph.values():
        for v in neighbors:
            if (min(v, neighbors[v[0]]) == v and max(v, neighbors[v[0]]) not in edges) or \
               (max(v, neighbors[v[0]]) == v and min(v, neighbors[v[0]]) not in edges):
                edges.add((v, neighbors[v[0]]))
    return len(edges)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_indices = []
    ranks = []
    
    for n in n_values:
        graph = generate_k_regular_graph(n, n - 1)
        if graph is None:
            continue
        min_idx = compute_minimal_index(graph)
        rank = compute_communication_complexity_rank(graph)
        min_indices.append(min_idx)
        ranks.append(rank)
    
    if len(min_indices) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(min_indices),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_min_idx = sum(min_indices) / len(min_indices)
    mean_rank = sum(ranks) / len(ranks)
    covariance = sum((min_indices[i] - mean_min_idx) * (ranks[i] - mean_rank) for i in range(len(min_indices))) / len(min_indices)
    variance_min_idx = sum((min_indices[i] - mean_min_idx) ** 2 for i in range(len(min_indices))) / len(min_indices)
    variance_rank = sum((ranks[i] - mean_rank) ** 2 for i in range(len(ranks))) / len(ranks)
    
    correlation_coefficient = covariance / math.sqrt(variance_min_idx * variance_rank)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_indices),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,  # Simplified threshold for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(1, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=0")
    else:
        print(f"RESULT: INCONCLUSIVE reason=support_fraction_too_low support_fraction={support_fraction}")