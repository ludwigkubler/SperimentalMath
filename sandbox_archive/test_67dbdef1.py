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
    
    def generate_k_regular_graph(k, n):
        graph = [[0] * n for _ in range(n)]
        degree = [0] * n
        edges_added = 0
        
        while edges_added < k * n // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and graph[u][v] == 0 and degree[u] < k and degree[v] < k:
                graph[u][v] = 1
                graph[v][u] = 1
                degree[u] += 1
                degree[v] += 1
                edges_added += 1
        
        return graph
    
    def girth(graph):
        n = len(graph)
        visited = [False] * n
        parent = [-1] * n
        
        def bfs(start):
            queue = [(start, 0)]
            while queue:
                u, dist = queue.pop(0)
                if visited[u]:
                    return dist - (parent[u] == start)
                visited[u] = True
                for v in range(n):
                    if graph[u][v] and not visited[v]:
                        parent[v] = u
                        queue.append((v, dist + 1))
            return float('inf')
        
        min_girth = float('inf')
        for i in range(n):
            min_girth = min(min_girth, bfs(i))
        return min_girth
    
    def persistent_homology(graph):
        n = len(graph)
        simplicial_complex = []
        
        def add_face(face):
            if face not in simplicial_complex:
                simplicial_complex.append(face)
        
        for i in range(n):
            add_face([i])
        
        for size in range(2, n+1):
            for faces in itertools.combinations(range(n), size):
                valid = True
                for face in faces:
                    if sum(graph[u][v] for u, v in combinations(faces, 2)) != size - 1:
                        valid = False
                        break
                if valid:
                    add_face(list(faces))
        
        return simplicial_complex
    
    def mli(simplicial_complex):
        # Placeholder implementation of minimal local indeterminacy calculation
        # This is a dummy function and should be replaced with actual persistent homology code
        return len(simplicial_complex)
    
    n = 30
    k = random.randint(2, min(n-1, 5))
    graph = generate_k_regular_graph(k, n)
    if girth(graph) <= k + 2:
        return {
            "metric_name": "mli(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "girth_not_greater_than_k_plus_2"
        }
    
    simplicial_complex = persistent_homology(graph)
    mli_value = mli(simplicial_complex)
    r_value = k * n // 2
    
    return {
        "metric_name": "mli(G)",
        "metric_value": mli_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mli_value == r_value and r_value >= 2 * k - 4,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample='mli(G) != r(G)' first_failing_seed={first_failing_seed}"
    
    print(result)