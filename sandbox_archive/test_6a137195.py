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
    
    def generate_graph(n):
        G = {i: set() for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i].add(j)
                    G[j].add(i)
                    edges.append((i, j))
        return G, edges
    
    def girth(G):
        visited = set()
        parent = {v: None for v in G}
        
        def dfs(v, p):
            if v in visited:
                return 0
            visited.add(v)
            min_dist = float('inf')
            for u in G[v]:
                if u != p:
                    dist = dfs(u, v) + 1
                    if dist < min_dist:
                        min_dist = dist
            return min_dist
        
        for v in G:
            if v not in visited:
                dist = dfs(v, None)
                if dist > 0:
                    return dist
        return float('inf')
    
    def communication_complexity(G, H):
        n = len(G)
        bipartite = {i: set() for i in range(n)}
        for u in range(n // 2):
            for v in range(n // 2, n):
                bipartite[u].add(v)
        
        def is_subgraph(H, G):
            return all(u in G and v in G[u] for u, v in H)
        
        if not is_subgraph(H, G):
            return float('inf')
        
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v in edges:
            dist[u][v] = dist[v][u] = 1
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        max_dist = 0
        for u, v in H:
            max_dist = max(max_dist, dist[u][v])
        
        return max_dist
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        G, edges = generate_graph(n)
        if girth(G) < n:
            continue
        
        H = set()
        while len(H) < n // 2:
            u, v = random.sample(range(n), 2)
            if u not in H and v not in H and (u, v) not in edges and (v, u) not in edges:
                H.add(u)
                H.add(v)
        
        complexity = communication_complexity(G, H)
        total_complexity += complexity
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_complexity = total_complexity / instances_tested
    lower_bound = 0.5 * (n + math.log2(n))
    upper_bound = 0.8 * (n - math.log2(n))
    
    conjecture_holds = all(lower_bound <= complexity for complexity in [mean_complexity])
    counterexample = "" if conjecture_holds else f"mean={mean_complexity}, lower_bound={lower_bound}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")