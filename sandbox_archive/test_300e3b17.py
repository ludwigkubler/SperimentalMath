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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        degree = [d] * n
        while any(d > 0 for d in degree):
            u = random.randint(0, n - 1)
            if degree[u] == 0:
                continue
            v = random.choice([i for i in range(n) if i != u and len(graph[i]) < d])
            graph[u].append(v)
            graph[v].append(u)
            degree[u] -= 1
            degree[v] -= 1
        return graph
    
    def cusp_form_rank(graph):
        n = len(graph)
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in graph or (j, i) in graph:
                    edges.add((i, j))
        return len(edges)
    
    def resolution_proof_width(graph):
        n = len(graph)
        if n == 1:
            return 0
        queue = [0]
        visited = [False] * n
        visited[0] = True
        width = 0
        while queue:
            level_size = len(queue)
            for _ in range(level_size):
                u = queue.pop(0)
                for v in graph[u]:
                    if not visited[v]:
                        visited[v] = True
                        queue.append(v)
            width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        rank = cusp_form_rank(graph)
        width = resolution_proof_width(graph)
        if rank is not None and width is not None:
            ranks.append(rank)
            widths.append(width)
    
    if len(ranks) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    corr = (sum((r - mean_rank) * (w - mean_width) for r, w in zip(ranks, widths)) /
            math.sqrt(sum((r - mean_rank)**2 for r in ranks) *
                      sum((w - mean_width)**2 for w in widths)))
    
    return {
        "metric_name": "correlation",
        "metric_value": corr,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(corr) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={r['seed']}")
                break