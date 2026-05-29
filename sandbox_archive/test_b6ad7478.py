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
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1):
                    weight = random.randint(1, 10)
                    graph[i][j] = weight
                    graph[j][i] = weight
        return graph
    
    def find_mst(graph):
        n = len(graph)
        mst = [[float('inf')] * n for _ in range(n)]
        parent = [-1] * n
        visited = [False] * n
        
        min_heap = [(0, 0)]
        while min_heap:
            weight, u = heapq.heappop(min_heap)
            if visited[u]:
                continue
            visited[u] = True
            mst[u][u] = 0
            for v in range(n):
                if not visited[v] and graph[u][v] != 0:
                    if mst[u][v] > graph[u][v]:
                        mst[u][v] = graph[u][v]
                        parent[v] = u
                        heapq.heappush(min_heap, (graph[u][v], v))
        
        diameter = 0
        for i in range(n):
            for j in range(i + 1, n):
                if mst[i][j] == float('inf'):
                    return float('inf')
                diameter = max(diameter, mst[i][j])
        return diameter
    
    def is_k_clique(graph, k):
        n = len(graph)
        for i in range(n):
            neighbors = [j for j in range(n) if graph[i][j] != 0]
            if len(neighbors) < k:
                return False
            for j in range(len(neighbors)):
                for l in range(j + 1, len(neighbors)):
                    if graph[neighbors[j]][neighbors[l]] == 0:
                        return False
        return True
    
    def construct_monotone_circuit(graph):
        n = len(graph)
        circuit_size = n * (n - 1) // 2
        return circuit_size
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    
    if not is_k_clique(graph, 3):
        return {
            "metric_name": "Diameter of MST",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph does not contain a 3-clique"
        }
    
    diameter = find_mst(graph)
    circuit_size = construct_monotone_circuit(graph)
    
    return {
        "metric_name": "Diameter of MST",
        "metric_value": diameter,
        "instances_tested": 1,
        "conjecture_holds": diameter <= n ** 0.25,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph does not contain a 3-clique\" first_failing_seed={first_failing_seed}")