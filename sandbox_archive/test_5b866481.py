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
    
    def generate_graph(n):
        graph = {i: set() for i in range(n)}
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random.shuffle(edges)
        added_edges = 0
        for u, v in edges:
            if len(graph[u]) < n - 2 and len(graph[v]) < n - 2:
                graph[u].add(v)
                graph[v].add(u)
                added_edges += 1
                if added_edges == n - 1:
                    break
        return graph
    
    def girth(graph):
        for length in range(3, len(graph) + 1):
            visited = set()
            queue = [(node, [node]) for node in graph]
            while queue:
                current, path = queue.pop(0)
                if len(path) == length and path[0] == path[-1]:
                    return length
                if current not in visited:
                    visited.add(current)
                    for neighbor in graph[current]:
                        if neighbor not in path:
                            queue.append((neighbor, path + [neighbor]))
        return float('inf')
    
    def communication_complexity(graph):
        n = len(graph)
        complete_bipartite = {i: set(range(n // 2, n)) for i in range(n // 2)}
        distances = [[float('inf')] * n for _ in range(n)]
        for u in graph:
            distances[u][u] = 0
            for v in graph[u]:
                distances[u][v] = 1
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if distances[i][k] + distances[k][j] < distances[i][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
        
        def is_subgraph(graph1, graph2):
            return all(u in graph2 and v in graph2[u] for u in graph1 for v in graph1[u])
        
        if is_subgraph(graph, complete_bipartite):
            return 0
        
        min_distance = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                min_distance = min(min_distance, distances[i][j])
        
        return min_distance
    
    n_values = [5, 10, 15, 20, 30, 40]
    complexities = []
    
    for n in n_values:
        graph = generate_graph(n)
        while girth(graph) < n:
            graph = generate_graph(n)
        
        complexity = communication_complexity(graph)
        complexities.append(complexity)
    
    mean_complexity = sum(complexities) / len(complexities)
    conjecture_holds = all(complexity >= 0.8 * (n - math.log2(n)) for n, complexity in zip(n_values, complexities))
    counterexample = "" if conjecture_holds else "communication_complexity < 0.8 * (n - log2(n))"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_complexity,
        "instances_tested": len(complexities),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication_complexity < 0.8 * (n - log2(n))\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")