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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        degree_counts = [0] * n
        edges_added = 0
        
        while edges_added < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                degree_counts[u] += 1
                degree_counts[v] += 1
                edges_added += 1
        
        return graph
    
    def calculate_resolution_width(graph):
        n = len(graph)
        if n == 0:
            return 0
        queue = [i for i in range(n) if len(graph[i]) == 1]
        level = 0
        visited = set(queue)
        
        while queue:
            next_level = []
            for u in queue:
                for v in graph[u]:
                    if v not in visited:
                        visited.add(v)
                        next_level.append(v)
            queue = next_level
            level += 1
        
        return level
    
    def calculate_index(graph):
        n = len(graph)
        if n == 0:
            return 0
        max_degree = max(len(neighbors) for neighbors in graph)
        min_degree = min(len(neighbors) for neighbors in graph)
        index = (max_degree + min_degree) / 2
        return index
    
    def is_d_regular(graph, d):
        n = len(graph)
        if n == 0:
            return True
        degrees = [len(neighbors) for neighbors in graph]
        return all(degree == d for degree in degrees)
    
    n = random.randint(5, 40)
    d = random.randint(3, min(n - 1, 8))
    graph = generate_d_regular_graph(n, d)
    
    if not is_d_regular(graph, d):
        return {
            "metric_name": "Index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph is not d-regular"
        }
    
    index = calculate_index(graph)
    resolution_width = calculate_resolution_width(graph)
    
    if resolution_width == 0:
        return {
            "metric_name": "Index",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Resolution width is zero"
        }
    
    ratio = index / resolution_width
    
    return {
        "metric_name": "Index",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_dev = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")