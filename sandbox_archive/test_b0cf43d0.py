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

def generate_random_d_regular_graph(n, d):
    if n % d != 0:
        return None
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(d):
            neighbor = (i + j + 1) % n
            if neighbor not in graph[i]:
                graph[i].append(neighbor)
                graph[neighbor].append(i)
    return graph

def is_valid_graph(graph, d):
    if graph is None:
        return False
    n = len(graph)
    for i in range(n):
        if len(graph[i]) != d:
            return False
    return True

def compute_mqr(graph):
    n = len(graph)
    mqr = 0
    for node in range(n):
        visited = [False] * n
        stack = [node]
        while stack:
            current = stack.pop()
            if not visited[current]:
                visited[current] = True
                mqr += 1
                for neighbor in graph[current]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
    return mqr

def compute_r(graph):
    n = len(graph)
    r = 0
    for node in range(n):
        degree = len(graph[node])
        if degree > r:
            r = degree
    return r

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            d = random.randint(2, min(n - 1, 8))
            graph = generate_random_d_regular_graph(n, d)
            if not is_valid_graph(graph, d):
                continue
            mqr = compute_mqr(graph)
            r = compute_r(graph)
            results.append((mqr, r))
    if not results:
        return {
            "metric_name": "mqr(G) / r(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    mqr_values = [r[0] for r in results]
    r_values = [r[1] for r in results]
    mean_mqr_over_r = sum(mqr_values) / sum(r_values)
    return {
        "metric_name": "mqr(G) / r(G)",
        "metric_value": mean_mqr_over_r,
        "instances_tested": len(results),
        "n_max": max(40, n),
        "conjecture_holds": all(mqr >= r for mqr, r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mqr(G) / r(G) < 1.0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")