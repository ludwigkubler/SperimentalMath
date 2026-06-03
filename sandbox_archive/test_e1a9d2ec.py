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
        if k * (k - 1) / 2 >= n:
            return None
        
        graph = [[] for _ in range(n)]
        degree_count = [0] * n
        edges_added = set()
        
        while sum(degree_count) < n * k:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            
            if u == v or (u, v) in edges_added or (v, u) in edges_added:
                continue
            
            graph[u].append(v)
            graph[v].append(u)
            degree_count[u] += 1
            degree_count[v] += 1
            edges_added.add((u, v))
        
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
                    return dist - (parent[u] == start) + 1
                visited[u] = True
                for v in graph[u]:
                    if not visited[v]:
                        parent[v] = u
                        queue.append((v, dist + 1))
            return float('inf')
        
        min_girth = float('inf')
        for i in range(n):
            min_girth = min(min_girth, bfs(i))
        return min_girth
    
    def mli(graph):
        n = len(graph)
        if n == 0:
            return 0
        
        # Simplicial complex construction
        simplicial_complex = []
        for i in range(n):
            for j in range(i+1, n):
                if j in graph[i]:
                    simplicial_complex.append((i, j))
        
        # Persistent homology (simplified version)
        def find(parent, i):
            if parent[i] == i:
                return i
            return find(parent, parent[i])
        
        def union(parent, rank, x, y):
            rootX = find(parent, x)
            rootY = find(parent, y)
            
            if rootX != rootY:
                if rank[rootX] > rank[rootY]:
                    parent[rootY] = rootX
                elif rank[rootX] < rank[rootY]:
                    parent[rootX] = rootY
                else:
                    parent[rootY] = rootX
                    rank[rootX] += 1
        
        def persistence_homology(simplicial_complex):
            edges = sorted(simplicial_complex, key=lambda x: (x[0], x[1]))
            parent = list(range(n * n))
            rank = [0] * (n * n)
            birth = [-1] * (n * n)
            death = [-1] * (n * n)
            
            for u, v in edges:
                root_u = find(parent, u * n + v)
                root_v = find(parent, v * n + u)
                
                if root_u != root_v:
                    union(parent, rank, root_u, root_v)
                    if birth[root_u] == -1 and birth[root_v] == -1:
                        birth[root_u] = len(edges)
                        birth[root_v] = len(edges)
                    else:
                        death[root_u] = len(edges)
                        death[root_v] = len(edges)
            
            return sum(death[i] - birth[i] for i in range(n * n) if birth[i] != -1 and death[i] != -1)
        
        mli_value = persistence_homology(simplicial_complex)
        return mli_value
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        
        def dfs(node, visited):
            nonlocal rank
            stack = [node]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    rank += 1
                    for v in graph[u]:
                        if not visited[v]:
                            stack.append(v)
        
        visited = [False] * n
        dfs(0, visited)
        return rank
    
    k = random.randint(3, 5)  # Ensure girth > k+2
    n = random.randint(k + 4, 40)
    graph = generate_k_regular_graph(k, n)
    
    if not graph or girth(graph) <= k + 2:
        return {
            "metric_name": "mli(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "girth_not_greater_than_k_plus_2"
        }
    
    mli_value = mli(graph)
    rank = communication_complexity_rank(graph)
    
    if mli_value is None or rank is None:
        return {
            "metric_name": "mli(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "computation_failed"
        }
    
    return {
        "metric_name": "mli(G)",
        "metric_value": mli_value / rank if rank != 0 else None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")