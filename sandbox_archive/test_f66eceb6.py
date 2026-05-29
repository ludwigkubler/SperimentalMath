# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def kruskal(graph):
        edges = sorted([(graph[u][v], u, v) for u in graph for v in graph[u] if u < v])
        parent = {u: u for u in graph}
        rank = {u: 0 for u in graph}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                if rank[rootX] > rank[rootY]:
                    parent[rootY] = rootX
                elif rank[rootX] < rank[rootY]:
                    parent[rootX] = rootY
                else:
                    parent[rootY] = rootX
                    rank[rootX] += 1
        
        mst = []
        for weight, u, v in edges:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v))
        return mst
    
    def diameter(mst):
        n = len(graph)
        dist = [[float('inf')] * n for _ in range(n)]
        for u, v in mst:
            dist[u][v] = dist[v][u] = 1
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return max(max(row) for row in dist)
    
    def clique_size(graph, k):
        n = len(graph)
        for subset in combinations(range(n), k):
            if all(graph[u][v] == 1 for u, v in combinations(subset, 2)):
                return True
        return False
    
    n = random.randint(5, 40)
    graph = {i: {} for i in range(n)}
    for _ in range(random.randint(int(n * (n - 1) / 4), int(n * (n - 1) / 2))):
        u, v = random.sample(range(n), 2)
        if v not in graph[u]:
            graph[u][v] = graph[v][u] = random.randint(1, 10)
    
    k = min(3, n // 2)
    if not clique_size(graph, k):
        return {
            "metric_name": "diameter",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k-CLIQUE problem is not solvable on the graph"
        }
    
    mst = kruskal(graph)
    D = diameter(mst)
    p_n = lambda n: math.ceil(n ** (3/4))
    size_C = random.randint(p_n(n) ** 2, 10 * p_n(n) ** 2)
    
    return {
        "metric_name": "diameter",
        "metric_value": D,
        "instances_tested": 1,
        "conjecture_holds": D <= n ** (1/4),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_D = sum(result["metric_value"] for result in results) / len(results)
    std_D = math.sqrt(sum((result["metric_value"] - mean_D) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_D} std={std_D} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_D} std={std_D} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"diameter does not satisfy Θ(n^{1/4})\" first_failing_seed={first_failing_seed}")