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

def generate_k_colorable_graph(n, k):
    if n <= 0 or k <= 0:
        return None
    
    colors = list(range(k))
    graph = [[] for _ in range(n)]
    
    for i in range(n):
        available_colors = set(colors)
        used_colors = {colors[j] for j in range(i) if any(graph[j][k] == i for k in range(len(graph[j])))}
        available_colors -= used_colors
        if not available_colors:
            return None
        
        color = random.choice(list(available_colors))
        graph[i].append(color)
    
    return graph

def compute_min_ring_norm(graph):
    n = len(graph)
    if n == 0:
        return 0
    
    # Polynomial representation of the graph
    poly = [1] * (n + 1)
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                poly[i] *= (i - j)
                poly[j] *= (j - i)
    
    # Minimal local ring norm
    min_norm = float('inf')
    for coeff in poly:
        if coeff != 0:
            norm = abs(coeff) ** (1 / n)
            if norm < min_norm:
                min_norm = norm
    
    return min_norm

def compute_communication_rank(graph):
    n = len(graph)
    rank = 0
    visited = [False] * n
    
    def dfs(node, parent):
        nonlocal rank
        visited[node] = True
        for neighbor in range(n):
            if graph[node][neighbor] and neighbor != parent:
                rank += 1
                dfs(neighbor, node)
    
    for i in range(n):
        if not visited[i]:
            dfs(i, -1)
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n, 4))
    
    graph = generate_k_colorable_graph(n, k)
    if graph is None:
        return {
            "metric_name": "min_ring_norm",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    min_ring_norm = compute_min_ring_norm(graph)
    communication_rank = compute_communication_rank(graph)
    
    if communication_rank == 0:
        return {
            "metric_name": "min_ring_norm",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "communication_rank_zero"
        }
    
    correlation = (min_ring_norm - communication_rank) / (min_ring_norm + communication_rank)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.9,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r.get("counterexample", "unknown")
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")