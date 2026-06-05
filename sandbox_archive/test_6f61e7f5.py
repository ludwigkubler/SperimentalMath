# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for i in range(n):
        for j in range(i + 1, n):
            if len(graph[i]) < d and len(graph[j]) < d:
                add_edge(i, j)
    
    return graph

def compute_eta_invariant(graph):
    # Placeholder implementation of eta-invariant computation
    # This is a dummy function and should be replaced with the actual algorithm
    return Fraction(0, 1)

def measure_monotone_width(graph):
    n = len(graph)
    max_width = 0
    
    def dfs(node, visited, path):
        nonlocal max_width
        if len(path) > max_width:
            max_width = len(path)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor, visited, path + [neighbor])
                visited.remove(neighbor)
    
    for i in range(n):
        visited = set([i])
        dfs(i, visited, [i])
    
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    eta_values = []
    width_values = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)  # Example degree
        eta = compute_eta_invariant(graph)
        width = measure_monotone_width(graph)
        
        eta_values.append(eta)
        width_values.append(width)
    
    correlation_coefficient = sum((a - b) * (c - d) for a, b, c, d in zip(eta_values, [sum(eta_values) / len(eta_values)] * len(eta_values), width_values, [sum(width_values) / len(width_values)] * len(width_values))) / (len(eta_values) * sum((a - b) ** 2 for a, b in zip(eta_values, [sum(eta_values) / len(eta_values)] * len(eta_values)))) ** 0.5
    mean_abs_difference = sum(abs(a - b) for a, b in zip(eta_values, [Fraction(n, 1) for n in width_values])) / len(eta_values)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and mean_abs_difference <= 2,
        "counterexample": "" if correlation_coefficient >= 0.7 and mean_abs_difference <= 2 else "Correlation too low or mean absolute difference too high"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")