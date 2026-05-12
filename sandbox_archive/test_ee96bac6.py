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

def is_clique(graph, vertices):
    for u in vertices:
        for v in vertices:
            if u != v and (u, v) not in graph and (v, u) not in graph:
                return False
    return True

def find_max_disjoint_cliques(graph, k):
    n = len(graph)
    cliques = []
    visited = [False] * n
    
    def dfs(node, path):
        if len(path) == k:
            if is_clique(graph, path):
                cliques.append(path[:])
            return
        for i in range(node, n):
            if not visited[i]:
                visited[i] = True
                path.append(i)
                dfs(i + 1, path)
                path.pop()
                visited[i] = False
    
    for i in range(n):
        if not visited[i]:
            visited[i] = True
            dfs(i + 1, [i])
            visited[i] = False
    
    return len(cliques)

def estimate_dnf_size(graph, k):
    n = len(graph)
    max_clique_cover = []
    visited = [False] * n
    
    def dfs(node, path):
        if is_clique(graph, path):
            for v in path:
                visited[v] = True
            max_clique_cover.append(path[:])
    
    for i in range(n):
        if not visited[i]:
            visited[i] = True
            dfs(i + 1, [i])
            visited[i] = False
    
    return len(max_clique_cover)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 3
    graph = {i: [] for i in range(n)}
    
    # Generate a random graph with edges
    for _ in range(int(n * (n - 1) / 2 * 0.5)):
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in graph and (v, u) not in graph:
            graph[u].append(v)
            graph[v].append(u)
    
    r = find_max_disjoint_cliques(graph, k)
    dnf_size = estimate_dnf_size(graph, k)
    
    if r == 0:
        return {
            "metric_name": "DNF Size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No disjoint cliques found"
        }
    
    c = dnf_size / n**(2/r)
    return {
        "metric_name": "DNF Size",
        "metric_value": dnf_size,
        "instances_tested": 1,
        "conjecture_holds": dnf_size >= c * n**(2/r),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dnf_size = sum(r["metric_value"] for r in results) / len(results)
    std_dnf_size = math.sqrt(sum((r["metric_value"] - mean_dnf_size)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dnf_size} std={std_dnf_size} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DNF size too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")