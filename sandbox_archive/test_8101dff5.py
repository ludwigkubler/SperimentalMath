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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d >= n:
            return None
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < d * n // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph
    
    def is_connected(graph):
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(neighbor for neighbor in graph[node] if neighbor not in visited)
        return len(visited) == len(graph)
    
    def compute_entropy(graph):
        n = len(graph)
        degree_sum = sum(len(neighbors) for neighbors in graph.values())
        p = Fraction(degree_sum, 2 * n)
        entropy = -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)
        return entropy
    
    def compute_min_reflections(graph):
        if not is_connected(graph):
            return float('inf')
        
        n = len(graph)
        reflections = set()
        
        for node in range(n):
            neighbors = graph[node]
            for neighbor in neighbors:
                if neighbor < node:
                    continue
                reflection = (node, neighbor)
                reflections.add(reflection)
        
        return len(reflections)
    
    def is_valid_graph(graph):
        n = len(graph)
        degree_sum = sum(len(neighbors) for neighbors in graph.values())
        return degree_sum == 2 * n
    
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            d = random.randint(2, min(n - 1, 4))
            graph = generate_d_regular_graph(n, d)
            if not is_valid_graph(graph):
                continue
            instances_tested += 1
            n_max = max(n_max, n)
            entropy = compute_entropy(graph)
            reflections = compute_min_reflections(graph)
            metric_values.append(reflections / entropy)
    
    mean_value = sum(metric_values) / len(metric_values) if metric_values else float('nan')
    std_dev = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else float('nan')
    
    return {
        "metric_name": "Reflections per Entropy",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results if not math.isnan(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(not math.isnan(r["metric_value"]) and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not math.isnan(r["metric_value"]) and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not math.isnan(result["metric_value"]) and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid data")