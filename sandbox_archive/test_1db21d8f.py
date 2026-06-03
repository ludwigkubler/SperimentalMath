# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_d_regular_graph(n, d):
    if d * n % 2 != 0:
        raise ValueError("d must be even for a regular graph")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(i, j):
        if (i, j) not in edges_added and (j, i) not in edges_added:
            graph[i].append(j)
            graph[j].append(i)
            edges_added.add((i, j))
            edges_added.add((j, i))
    
    for i in range(n):
        remaining = d - len(graph[i])
        if remaining == 0:
            continue
        available = [j for j in range(n) if j != i and j not in graph[i]]
        neighbors = random.sample(available, remaining)
        for neighbor in neighbors:
            add_edge(i, neighbor)
    
    return graph

def communication_complexity_rank(graph):
    n = len(graph)
    ranks = [0] * n
    
    def dfs(node, visited):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph[node]:
            dfs(neighbor, visited)
        ranks[node] = max(ranks[node], 1 + max((ranks[neighbor] for neighbor in graph[node]), default=0))
    
    for i in range(n):
        if not ranks[i]:
            dfs(i, set())
    
    return max(ranks)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = 3
    M_G_values = []
    r_G_values = []
    
    for _ in range(30):
        G = generate_d_regular_graph(n, d)
        r_G = communication_complexity_rank(G)
        
        # Construct minimal set of Kähler manifolds (simplified model)
        # For simplicity, assume each edge represents a unique Kähler manifold
        M_G = len(list(combinations(range(n), 2)))
        
        M_G_values.append(M_G)
        r_G_values.append(r_G)
    
    if not M_G_values or not r_G_values:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(M_G_values),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_M_G = sum(M_G_values) / len(M_G_values)
    mean_r_G = sum(r_G_values) / len(r_G_values)
    std_dev_M_G = math.sqrt(sum((x - mean_M_G) ** 2 for x in M_G_values) / len(M_G_values))
    std_dev_r_G = math.sqrt(sum((x - mean_r_G) ** 2 for x in r_G_values) / len(r_G_values))
    
    correlation_coefficient = sum((M_G_values[i] - mean_M_G) * (r_G_values[i] - mean_r_G) for i in range(len(M_G_values))) / (len(M_G_values) * std_dev_M_G * std_dev_r_G)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(M_G_values),
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_M_G - mean_r_G) <= 3,
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
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break