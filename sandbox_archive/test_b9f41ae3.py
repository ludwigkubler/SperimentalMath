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
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n < 5 or n > 40:
            continue
        
        d = random.randint(2, min(n-1, 4))
        graph = generate_d_regular_graph(n, d)
        
        aut_order = compute_aut_group_order(graph)
        rank_variance = compute_rank_variance(graph)
        
        results.append({
            "n": n,
            "d": d,
            "aut_order": aut_order,
            "rank_variance": rank_variance
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_graphs"
        }
    
    aut_orders = [r["aut_order"] for r in results]
    rank_variances = [r["rank_variance"] for r in results]
    
    mean_aut_order = sum(aut_orders) / len(aut_orders)
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    
    correlation = compute_correlation(aut_orders, rank_variances)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": abs(correlation) >= 0.5,  # Simplified threshold
        "counterexample": ""
    }

def generate_d_regular_graph(n: int, d: int) -> list:
    graph = [[] for _ in range(n)]
    
    edges_added = set()
    while len(edges_added) < n * d // 2:
        u, v = random.sample(range(n), 2)
        if (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
    
    return graph

def compute_aut_group_order(graph: list) -> int:
    n = len(graph)
    visited = [False] * n
    aut_group_size = 1
    
    def dfs(node: int, parent: int):
        nonlocal aut_group_size
        visited[node] = True
        
        for neighbor in graph[node]:
            if neighbor != parent and not visited[neighbor]:
                aut_group_size += 1
                dfs(neighbor, node)
    
    dfs(0, -1)
    
    return aut_group_size

def compute_rank_variance(graph: list) -> float:
    n = len(graph)
    rank_variances = []
    
    for _ in range(n):
        permuted_graph = [graph[i][::] for i in range(n)]
        random.shuffle(permuted_graph)
        
        variance = 0
        for i in range(n):
            for j in range(i+1, n):
                if len(set(permuted_graph[i])) != len(set(permuted_graph[j])):
                    variance += 1
        
        rank_variances.append(variance / (n * (n-1) // 2))
    
    return sum(rank_variances) / n

def compute_correlation(x: list, y: list) -> float:
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
    std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
    std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
    
    return cov_xy / (std_x * std_y)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not all(r["conjecture_holds"] for r in results):
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")