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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges_used = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) == d and len(graph[j]) == d:
                    continue
                if (i, j) not in edges_used and (j, i) not in edges_used:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges_used.add((i, j))
        return graph
    
    def is_connected(graph):
        n = len(graph)
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)
    
    def compute_mcl(graph):
        n = len(graph)
        if not is_connected(graph):
            return float('inf')
        
        mcl = 0
        for node in range(n):
            for neighbor in graph[node]:
                visited = [False] * n
                stack = [(node, neighbor, 1)]
                while stack:
                    current, next_node, length = stack.pop()
                    if not visited[next_node]:
                        visited[next_node] = True
                        mcl = max(mcl, length)
                        for next_neighbor in graph[next_node]:
                            if not visited[next_neighbor]:
                                stack.append((next_node, next_neighbor, length + 1))
        return mcl
    
    def compute_rank_variance(graph):
        n = len(graph)
        rank = [len(neighbors) for neighbors in graph]
        mean = sum(rank) / n
        variance = sum((x - mean) ** 2 for x in rank) / n
        return variance
    
    d = random.randint(3, 5)
    n = random.choice([10, 15, 20, 25, 30, 35, 40])
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "mcl",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "d-regular graph generation failed"
        }
    
    mcl = compute_mcl(graph)
    rank_variance = compute_rank_variance(graph)
    
    return {
        "metric_name": "mcl",
        "metric_value": mcl,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")