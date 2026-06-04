# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < (n * d) // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def circuit_monotone_width(graph):
        n = len(graph)
        if n == 0:
            return 0
        visited = [False] * n
        width = 0
        
        def dfs(node, parent):
            nonlocal width
            stack = [(node, parent)]
            while stack:
                current, parent = stack.pop()
                visited[current] = True
                for neighbor in graph[current]:
                    if not visited[neighbor]:
                        stack.append((neighbor, current))
                if parent is None:
                    width += 1
        
        for node in range(n):
            if not visited[node]:
                dfs(node, None)
        
        return width
    
    def integer_lattice_homology(graph):
        n = len(graph)
        if n == 0:
            return 0
        rank = 1
        for i in range(1, n):
            if all(len(graph[j]) > 0 for j in range(i)):
                rank += 1
        return rank
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        if std_dev_x == 0 or std_dev_y == 0:
            return 0
        return cov_xy / (std_dev_x * std_dev_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        homology_rank = integer_lattice_homology(graph)
        width = circuit_monotone_width(graph)
        results.append((homology_rank, width))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid graph generated"
        }
    
    x = [result[0] for result in results]
    y = [result[1] for result in results]
    corr_coeff = correlation_coefficient(x, y)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": corr_coeff >= 0.5 and corr_coeff <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")