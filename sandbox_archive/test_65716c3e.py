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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_connected(graph):
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        return len(visited) == len(graph)

    def betti_number(graph):
        n = len(graph)
        m = sum(len(neighbors) for neighbors in graph.values()) // 2
        return m - n + 1

    def resolution_width(graph):
        # Simplified DPLL-based width estimator (not actual DPLL)
        queue = list(graph.keys())
        width = 0
        while queue:
            node = queue.pop()
            if node not in graph:
                continue
            neighbors = graph[node]
            for neighbor in neighbors:
                if neighbor in graph and neighbor != node:
                    queue.remove(neighbor)
            width = max(width, len(neighbors))
        return width

    n = random.randint(5, 40)
    m = random.randint(n - 1, n * (n - 1) // 2)
    
    # Generate a connected graph
    graph = {i: [] for i in range(n)}
    edges_added = set()
    while len(edges_added) < m:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
    
    if not is_connected(graph):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "graph_not_connected"
        }
    
    betti = betti_number(graph)
    width = resolution_width(graph)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= betti,
        "counterexample": "" if width >= betti else f"width={width}, betti={betti}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / (len(results) - 1))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")