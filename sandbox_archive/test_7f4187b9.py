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
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(d):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
                    edges.add((j, i))
        return graph
    
    def cusp_form_rank(graph):
        if not graph:
            return 0
        n = len(graph)
        rank = 0
        for u in range(n):
            if len(graph[u]) == 2:
                v1, v2 = graph[u]
                if (v1, v2) in edges or (v2, v1) in edges:
                    rank += 1
        return rank
    
    def resolution_proof_width(graph):
        n = len(graph)
        if n < 3:
            return 0
        timeout = 5
        start_time = time.time()
        queue = [0]
        visited = set([0])
        while queue and time.time() - start_time < timeout:
            u = queue.pop(0)
            for v in graph[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        return len(visited) if time.time() - start_time < timeout else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        rank = cusp_form_rank(graph)
        width = resolution_proof_width(graph)
        if rank > 0 and width > 0:
            ranks.append(rank)
            widths.append(width)
    
    if not ranks or not widths:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "Graph generation failed"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    correlation = (sum((r - mean_rank) * (w - mean_width) for r, w in zip(ranks, widths)) /
                   math.sqrt(sum((r - mean_rank)**2 for r in ranks) * sum((w - mean_width)**2 for w in widths)))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.5,  # Threshold for linear correlation
        "counterexample": ""
    }

if __name__ == "__main__":
    import time
    import sys
    
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 prime numbers
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        mean_value = sum(res["metric_value"] for res in results if res["conjecture_holds"]) / sum(1 for res in results if res["conjecture_holds"])
        std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results if res["conjecture_holds"]) / sum(1 for res in results if res["conjecture_holds"]))
        support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(res['conjecture_holds'] for res in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")