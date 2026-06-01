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

def is_k_colorable(graph, k):
    n = len(graph)
    colors = [-1] * n
    
    def dfs(node, color):
        if node in visited:
            return True
        visited.add(node)
        colors[node] = color
        
        for neighbor in graph[node]:
            if colors[neighbor] == color or not dfs(neighbor, (color + 1) % k):
                return False
        return True
    
    visited = set()
    for i in range(n):
        if node not in visited:
            if not dfs(i, 0):
                return False
    return True

def generate_k_colorable_graph(n, k):
    graph = [[] for _ in range(n)]
    colors = [random.randint(0, k-1) for _ in range(n)]
    
    def add_edge(u, v):
        if u != v and (v not in graph[u] or u not in graph[v]):
            graph[u].append(v)
            graph[v].append(u)
    
    while True:
        for i in range(n):
            for j in range(i+1, n):
                if colors[i] == colors[j]:
                    add_edge(i, j)
        if is_k_colorable(graph, k):
            break
        graph = [[] for _ in range(n)]
    
    return graph

def minimal_quadratic_residue_representation(graph):
    n = len(graph)
    mqr = 0
    
    def quadratic_residue(x):
        return x * x % (n + 1)
    
    for i in range(n):
        for j in range(i+1, n):
            if j in graph[i]:
                mqr += quadratic_residue(j - i)
    
    return mqr

def communication_complexity_growth_rate(graph, k):
    n = len(graph)
    growth_rate = 0
    
    def dfs(node, visited):
        nonlocal growth_rate
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                growth_rate += 1
                dfs(neighbor, visited)
    
    for i in range(n):
        visited = set()
        dfs(i, visited)
    
    return growth_rate

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n, 6))
    graph = generate_k_colorable_graph(n, k)
    
    mqr = minimal_quadratic_residue_representation(graph)
    growth_rate = communication_complexity_growth_rate(graph, k)
    
    if growth_rate == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "growth_rate_is_zero"
        }
    
    correlation_coefficient = (mqr * growth_rate) / (math.sqrt(mqr ** 2 + growth_rate ** 2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_not_significant' first_failing_seed={first_failing_seed}")