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
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph
    
    def circuit_monotone_width(graph):
        n = len(graph)
        visited = [False] * n
        width = 0
        
        def dfs(node, parent):
            nonlocal width
            stack = [(node, parent)]
            while stack:
                node, parent = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in graph[node]:
                        if neighbor != parent and not visited[neighbor]:
                            stack.append((neighbor, node))
                            width += 1
        
        for i in range(n):
            if not visited[i]:
                dfs(i, -1)
        
        return width
    
    def integer_lattice_homology(graph):
        n = len(graph)
        homology = defaultdict(int)
        for node in graph:
            homology[node] = sum(1 for neighbor in graph[node] if node < neighbor)
        return sum(homology.values())
    
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_coefficients = []
    
    for n in n_values:
        d = random.randint(2, min(n-1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        w_m = circuit_monotone_width(graph)
        H_G_Z = integer_lattice_homology(graph)
        correlation_coefficients.append((H_G_Z, w_m))
    
    if not correlation_coefficients:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(correlation_coefficients)
    sum_x = sum(x for x, _ in correlation_coefficients)
    sum_y = sum(y for _, y in correlation_coefficients)
    sum_xy = sum(x * y for x, y in correlation_coefficients)
    sum_xx = sum(x ** 2 for x, _ in correlation_coefficients)
    
    mean_x = sum_x / n
    mean_y = sum_y / n
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(0.5 <= corr < 1 for corr in correlation_coefficients),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if "metric_value" in res) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if "metric_value" in res) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["metric_value"] < 0.5 for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"] and res["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")