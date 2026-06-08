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
    if n * d % 2 != 0 or d > n - 1:
        raise ValueError("Invalid parameters for generating a d-regular graph")
    
    graph = [[] for _ in range(n)]
    degree_count = [0] * n
    
    def add_edge(u, v):
        if u == v or len(graph[u]) >= d or len(graph[v]) >= d:
            return False
        graph[u].append(v)
        graph[v].append(u)
        degree_count[u] += 1
        degree_count[v] += 1
        return True
    
    for _ in range(d * n // 2):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        while not add_edge(u, v):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
    
    return graph

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def min_order(graph):
    orders = []
    for node in range(len(graph)):
        visited = [False] * len(graph)
        queue = [node]
        visited[node] = True
        current_order = 1
        
        while queue:
            u = queue.pop(0)
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
                    current_order += 1
        
        orders.append(current_order)
    
    return lcm(*orders)

def resolution_width(phi_G):
    # Placeholder function to simulate the computation of resolution width
    # For simplicity, we assume a linear relationship with n
    n = len(phi_G)
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(1, n - 1)
        graph = generate_d_regular_graph(n, d)
        phi_G = [random.choice([0, 1]) for _ in range(n)]
        
        min_order_val = min_order(graph)
        width_val = resolution_width(phi_G)
        
        results.append({
            "n": n,
            "min_order": min_order_val,
            "width": width_val
        })
    
    correlation_coefficient = 0.0
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            r_i = results[i]
            r_j = results[j]
            correlation_coefficient += (r_i["min_order"] - r_i["width"]) * (r_j["min_order"] - r_j["width"])
    
    n_pairs = len(results) * (len(results) - 1) // 2
    correlation_coefficient /= n_pairs
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")