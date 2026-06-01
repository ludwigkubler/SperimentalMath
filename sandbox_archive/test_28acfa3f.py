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
    if (n * d) % 2 != 0:
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

def is_planar(graph):
    def dfs(node, parent, visited, rec_stack):
        visited[node] = True
        rec_stack[node] = True
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node, visited, rec_stack):
                    return True
            elif rec_stack[neighbor]:
                return True
        
        rec_stack[node] = False
        return False
    
    n = len(graph)
    visited = [False] * n
    rec_stack = [False] * n
    
    for i in range(n):
        if not visited[i]:
            if dfs(i, -1, visited, rec_stack):
                return False
    
    def check_planarity():
        queue = []
        for node in range(n):
            if len(graph[node]) > 5:
                return False
            queue.append((node, 0))
        
        while queue:
            node, depth = queue.pop(0)
            if depth > 3:
                return False
            for neighbor in graph[node]:
                if neighbor != queue[-1][0]:
                    queue.append((neighbor, depth + 1))
        
        return True
    
    return check_planarity()

def minimal_order_of_hodge_structure(graph):
    if not is_planar(graph):
        return None
    
    n = len(graph)
    moh = 2 * n
    for i in range(n):
        moh = min(moh, len(graph[i]))
    
    return moh

def resolution_proof_width(graph):
    def bfs(start):
        queue = [start]
        visited = set([start])
        level = {start: 0}
        
        while queue:
            node = queue.pop(0)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    level[neighbor] = level[node] + 1
        
        return max(level.values())
    
    n = len(graph)
    width = 0
    for i in range(n):
        width = max(width, bfs(i))
    
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            d = random.randint(2, min(n - 1, 4))
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            moh = minimal_order_of_hodge_structure(graph)
            width = resolution_proof_width(graph)
            if moh is not None and width >= n ** 0.5 / 2:
                results.append((moh, width))
    
    if len(results) < 15:
        return {
            "metric_name": "minimal_order_of_hodge_structure",
            "metric_value": -1,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    moh_values = [moh for moh, _ in results]
    width_values = [width for _, width in results]
    
    mean_moh = sum(moh_values) / len(moh_values)
    std_moh = math.sqrt(sum((x - mean_moh) ** 2 for x in moh_values) / len(moh_values))
    mean_width = sum(width_values) / len(width_values)
    std_width = math.sqrt(sum((x - mean_width) ** 2 for x in width_values) / len(width_values))
    
    return {
        "metric_name": "minimal_order_of_hodge_structure",
        "metric_value": mean_moh,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": mean_width >= 0.5 * mean_moh ** 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_moh = sum(r["metric_value"] for r in results) / len(results)
    std_moh = math.sqrt(sum((r["metric_value"] - mean_moh) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_moh} std={std_moh} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")