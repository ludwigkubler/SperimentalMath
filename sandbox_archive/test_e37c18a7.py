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

def generate_d_regular_graph(n, d):
    if n % d != 0:
        return None
    graph = {i: [] for i in range(n)}
    edges_added = 0
    while edges_added < n * d // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and v not in graph[u]:
            graph[u].append(v)
            graph[v].append(u)
            edges_added += 1
    return graph

def dfs(node, parent, level):
    max_level = level
    for neighbor in graph[node]:
        if neighbor != parent:
            child_level = dfs(neighbor, node, level + 1)
            max_level = max(max_level, child_level)
    return max_level

def circuit_monotone_width(graph):
    n = len(graph)
    width = 0
    for i in range(n):
        width = max(width, dfs(i, -1, 0))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        width = circuit_monotone_width(graph)
        order = len(graph)  # Simplified order as the number of vertices
        results.append((order, width))
    
    if not results:
        return {
            "metric_name": "circuit_monotone_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    order_values = [r[0] for r in results]
    width_values = [r[1] for r in results]
    mean_order = sum(order_values) / len(order_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation_coefficient = 0
    if len(order_values) > 1:
        numerator = sum((order_values[i] - mean_order) * (width_values[i] - mean_width) for i in range(len(order_values)))
        denominator = math.sqrt(sum((order_values[i] - mean_order) ** 2 for i in range(len(order_values))) * sum((width_values[i] - mean_width) ** 2 for i in range(len(width_values))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(order_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    all_results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        all_results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in all_results if r["metric_value"] is not None) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in all_results if r["metric_value"] is not None)) / len(all_results)
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")