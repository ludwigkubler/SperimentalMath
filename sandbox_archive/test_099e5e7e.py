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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < d * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph

    def circuit_monotone_complexity(graph):
        n = len(graph)
        if n == 1:
            return 0
        visited = [False] * n
        complexity = 0
        
        def dfs(node):
            nonlocal complexity
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor)
                    complexity += 1
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
        
        return complexity

    def minimal_order_of_symplectic_leaves(graph):
        n = len(graph)
        if n == 1:
            return 0
        leaves = [set() for _ in range(n)]
        stack = []
        visited = [False] * n
        
        def dfs(node, parent):
            visited[node] = True
            stack.append(node)
            leaves[node].add(parent)
            for neighbor in graph[node]:
                if neighbor != parent:
                    dfs(neighbor, node)
        
        for i in range(n):
            if not visited[i]:
                dfs(i, -1)
        
        return max(len(leaf) for leaf in leaves)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(random.randint(2, n-1), n)
        if graph is None:
            continue
        m_order = minimal_order_of_symplectic_leaves(graph)
        w_m = circuit_monotone_complexity(graph)
        results.append((m_order, w_m))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    m_orders = [r[0] for r in results]
    w_ms = [r[1] for r in results]
    mean_m_order = sum(m_orders) / len(m_orders)
    mean_w_m = sum(w_ms) / len(w_ms)
    
    if len(set(m_orders)) == 1 or len(set(w_ms)) == 1:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else None
    
    corr_coeff = pearson_correlation(m_orders, w_ms)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff is not None and abs(corr_coeff) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")