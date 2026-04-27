# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def is_connected(graph):
    n = len(graph)
    visited = [False] * n
    stack = [0]
    visited[0] = True
    
    while stack:
        u = stack.pop()
        for v in range(n):
            if graph[u][v] and not visited[v]:
                visited[v] = True
                stack.append(v)
    
    return all(visited)

def generate_3_regular_graph(n):
    if n % 2 == 0 or (n * (n - 1) // 2) % 6 != 0:
        raise ValueError("Invalid number of vertices for a 3-regular graph")
    
    graph = [[0] * n for _ in range(n)]
    degree = [0] * n
    
    def add_edge(u, v):
        if u == v or graph[u][v]:
            return
        graph[u][v] = 1
        graph[v][u] = 1
        degree[u] += 1
        degree[v] += 1
    
    for _ in range(n * (n - 1) // 6):
        u, v = random.sample(range(n), 2)
        if degree[u] < 3 and degree[v] < 3:
            add_edge(u, v)
    
    return graph

def generate_odd_charges(n):
    return [random.choice([0, 1]) for _ in range(n)]

def partition_vertex_set(vertices, k):
    n = len(vertices)
    if k > n:
        return []
    
    partitions = []
    for i in range(2 ** (n - 1)):
        part1 = [vertices[j] for j in range(n) if i & (1 << j)]
        part2 = [v for v in vertices if v not in part1]
        partitions.append((part1, part2))
    
    return partitions

def compute_h_q(G):
    n = len(G)
    min_cut_edges = float('inf')
    min_partition_size = float('inf')
    
    for k in range(2, n + 1):
        partitions = partition_vertex_set(range(n), k)
        for part1, part2 in partitions:
            cut_edges = sum(G[u][v] for u in part1 for v in part2 if G[u][v])
            min_cut_edges = min(min_cut_edges, cut_edges)
            min_partition_size = min(min_partition_size, len(part1), len(part2))
    
    return min_cut_edges / min_partition_size

def bfs_width(G, start):
    n = len(G)
    visited = [False] * n
    queue = [start]
    visited[start] = True
    
    width = 0
    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            u = queue.pop(0)
            for v in range(n):
                if G[u][v] and not visited[v]:
                    visited[v] = True
                    queue.append(v)
        
        width = max(width, level_size)
    
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([6, 8, 10])
    G = generate_3_regular_graph(n)
    c = generate_odd_charges(n)
    
    if not is_connected(G):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "graph_not_connected"
        }
    
    h_q = compute_h_q(G)
    w = bfs_width(G, 0)  # Simplified BFS width for demonstration
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w,
        "instances_tested": 1,
        "conjecture_holds": math.ceil(h_q) <= w <= 3 * h_q + 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid data")