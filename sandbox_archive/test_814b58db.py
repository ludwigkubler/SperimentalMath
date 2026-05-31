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
from math import log2, floor

def generate_d_regular_graph(n: int, d: int) -> list:
    if n < 2 * d + 1 or d == 0:
        raise ValueError("Invalid parameters for generating a d-regular graph")
    
    graph = [[] for _ in range(n)]
    degree_counts = [0] * n
    
    def add_edge(u, v):
        graph[u].append(v)
        graph[v].append(u)
        degree_counts[u] += 1
        degree_counts[v] += 1
    
    for i in range(d):
        neighbors = random.sample(range(i+1, min(n, i+d+1)), d-1)
        for neighbor in neighbors:
            add_edge(i, neighbor)
    
    return graph

def compute_reflections(graph: list) -> int:
    n = len(graph)
    visited = [False] * n
    
    def dfs(node):
        if visited[node]:
            return 0
        visited[node] = True
        count = 1
        for neighbor in graph[node]:
            count += dfs(neighbor)
        return count
    
    reflections = 0
    for i in range(n):
        if not visited[i]:
            reflections += dfs(i) - 1
    return reflections

def compute_shannon_entropy(graph: list) -> float:
    n = len(graph)
    degree_counts = [len(neighbors) for neighbors in graph]
    total_edges = sum(degree_counts) // 2
    entropy = 0.0
    
    for count in degree_counts:
        if count > 0:
            p = count / (n - 1)
            entropy -= p * log2(p)
    
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        if (n - 1) * (n - 2) // 2 < n * (d := floor((n - 1) / 2)):
            continue
        
        graph = generate_d_regular_graph(n, d)
        reflections = compute_reflections(graph)
        entropy = compute_shannon_entropy(graph)
        
        if reflections > 4 * entropy:
            conjecture_holds = False
            counterexample = f"Graph with n={n}, d={d} has |R(G)| > 4h(G)"
            break
        
        metric_values.append(reflections - entropy)
    
    return {
        "metric_name": "reflections_minus_entropy",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")