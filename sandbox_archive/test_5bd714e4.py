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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        degree_count = [0] * n
        edges_added = 0
        
        while edges_added < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v]:
                graph[u].append(v)
                graph[v].append(u)
                degree_count[u] += 1
                degree_count[v] += 1
                edges_added += 1
        
        return graph
    
    def is_connected(graph):
        visited = [False] * len(graph)
        
        def dfs(node):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in graph[node]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
        
        dfs(0)
        return all(visited)
    
    def min_geometric_entropy(graph):
        n = len(graph)
        if not is_connected(graph):
            return float('inf')
        
        # Simplified geometric entropy calculation
        entropy = 0
        for node in range(n):
            degree = len(graph[node])
            entropy += math.log(degree + 1) / (n * (degree + 1))
        return entropy
    
    def circuit_monotone_complexity(graph):
        n = len(graph)
        if not is_connected(graph):
            return float('inf')
        
        # Simplified monotone complexity calculation
        complexity = 0
        for node in range(n):
            degree = len(graph[node])
            complexity += degree * (degree + 1) / 2
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        entropy = min_geometric_entropy(graph)
        complexity = circuit_monotone_complexity(graph)
        
        results.append({
            "n": n,
            "entropy": entropy,
            "complexity": complexity
        })
    
    if not results:
        return {
            "metric_name": "mge(G) / c_m(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_entropy = sum(result["entropy"] for result in results)
    total_complexity = sum(result["complexity"] for result in results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    ratio = total_entropy / total_complexity
    conjecture_holds = ratio <= 1
    
    return {
        "metric_name": "mge(G) / c_m(G)",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} > 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no data")
        sys.exit(0)
    
    total_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    mean_ratio = total_ratio / sum(1 for result in results if result["metric_value"] is not None)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")