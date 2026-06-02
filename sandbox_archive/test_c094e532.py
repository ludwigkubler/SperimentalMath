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
    
    def generate_k_regular_graph(n, k):
        if (n * k) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * k // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def k_theory_rank(graph):
        n = len(graph)
        adj_matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                adj_matrix[u][v] = 1
        rank = 0
        for i in range(n):
            if sum(adj_matrix[i]) > 0:
                rank += 1
                for j in range(n):
                    if adj_matrix[j][i] == 1:
                        for k in range(n):
                            adj_matrix[j][k] -= adj_matrix[i][k]
        return rank
    
    def communication_complexity_rank(graph):
        n = len(graph)
        min_bits = float('inf')
        for u in range(n):
            for v in range(u + 1, n):
                bits = 0
                visited = set()
                queue = [u]
                while queue:
                    node = queue.pop(0)
                    if node == v:
                        break
                    for neighbor in graph[node]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                            bits += 1
                min_bits = min(min_bits, bits)
        return min_bits
    
    n_values = [5, 10, 15, 20, 30, 40]
    rk_K_values = []
    r_G_values = []
    
    for n in n_values:
        graph = generate_k_regular_graph(n, k=3)
        if graph is None:
            continue
        rk_K = k_theory_rank(graph)
        r_G = communication_complexity_rank(graph)
        if rk_K == 0 or r_G == 0:
            continue
        rk_K_values.append(rk_K)
        r_G_values.append(r_G)
    
    if not rk_K_values or not r_G_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(rk_K_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mean_rk_K = sum(rk_K_values) / len(rk_K_values)
    mean_r_G = sum(r_G_values) / len(r_G_values)
    covariance = sum((rk_K - mean_rk_K) * (r_G - mean_r_G) for rk_K, r_G in zip(rk_K_values, r_G_values)) / len(rk_K_values)
    variance_rk_K = sum((rk_K - mean_rk_K) ** 2 for rk_K in rk_K_values) / len(rk_K_values)
    variance_r_G = sum((r_G - mean_r_G) ** 2 for r_G in r_G_values) / len(r_G_values)
    correlation_coefficient = covariance / (math.sqrt(variance_rk_K) * math.sqrt(variance_r_G))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(rk_K_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")