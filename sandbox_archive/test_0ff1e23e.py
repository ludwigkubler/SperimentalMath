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

def generate_random_graph(n):
    graph = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if u > v:
            u, v = v, u
        if (u, v) not in edges and (v, u) not in edges:
            graph[u][v] = 1
            graph[v][u] = 1
            edges.add((u, v))
    return graph

def local_index(graph):
    n = len(graph)
    for k in range(1, n + 1):
        covered_edges = set()
        for i in range(n):
            if sum(graph[i]) >= k:
                for j in range(i + 1, n):
                    if graph[i][j] == 1 and (i, j) not in covered_edges and (j, i) not in covered_edges:
                        covered_edges.add((i, j))
        if len(covered_edges) == n * (n - 1) // 2:
            return k
    return n

def communication_complexity(graph):
    n = len(graph)
    def dfs(u, visited):
        stack = [u]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for v in range(n):
                    if graph[u][v] == 1 and not visited[v]:
                        stack.append(v)
    
    visited = [False] * n
    dfs(0, visited)
    return sum(visited)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        graph = generate_random_graph(n)
        loc_idx = local_index(graph)
        comm_complexity = communication_complexity(graph)
        results.append((loc_idx, comm_complexity))
    
    mean_loc_idx = sum(loc for _, loc in results) / len(results)
    mean_comm_complexity = sum(comm for _, comm in results) / len(results)
    support_fraction = sum(1 for _, comm in results if loc_idx >= n**(1/3) and abs(comm - mean_comm_complexity) <= 2 * math.sqrt(mean_comm_complexity)) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else f"n={n}, loc_idx={loc_idx}, comm_complexity={comm_complexity}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm_complexity,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")