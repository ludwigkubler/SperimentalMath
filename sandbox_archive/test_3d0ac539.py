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
        if (n * k) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for u in range(n):
            for v in range(u + 1, n):
                if len(graph[u]) < k and len(graph[v]) < k and (u, v) not in edges:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges.add((u, v))
        return graph
    
    def compute_minimal_index(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in graph.items():
            for neighbor in v:
                adjacency_matrix[u][neighbor] = 1
        
        # Gaussian elimination to find rank
        rank = 0
        for i in range(n):
            if all(adjacency_matrix[j][i] == 0 for j in range(rank)):
                continue
            rank += 1
            for j in range(i + 1, n):
                if adjacency_matrix[j][i] != 0:
                    for k in range(n):
                        adjacency_matrix[j][k] -= adjacency_matrix[i][k]
        return rank
    
    def compute_communication_complexity_rank(graph):
        n = len(graph)
        max_degree = max(len(neighbors) for neighbors in graph.values())
        return max_degree
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if (n * k) % 2 != 0:
            continue
        graph = generate_k_regular_graph(n, k)
        if graph is None:
            continue
        
        min_idx = compute_minimal_index(graph)
        w_G = compute_communication_complexity_rank(graph)
        
        results.append((min_idx, w_G))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_indices = [r[0] for r in results]
    w_Gs = [r[1] for r in results]
    
    mean_min_idx = sum(min_indices) / len(min_indices)
    mean_w_G = sum(w_Gs) / len(w_Gs)
    covariance = sum((min_indices[i] - mean_min_idx) * (w_Gs[i] - mean_w_G) for i in range(len(min_indices))) / len(min_indices)
    variance_min_idx = sum((min_indices[i] - mean_min_idx) ** 2 for i in range(len(min_indices))) / len(min_indices)
    variance_w_G = sum((w_Gs[i] - mean_w_G) ** 2 for i in range(len(w_Gs))) / len(w_Gs)
    
    correlation_coefficient = covariance / math.sqrt(variance_min_idx * variance_w_G)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_indices),
        "n_max": max(len(graph) for graph in results if graph is not None),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")