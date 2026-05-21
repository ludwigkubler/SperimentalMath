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
        edges = [(u, v) for u in range(n) for v in range(u+1, n)]
        random.shuffle(edges)
        m = n - 1
        added_edges = 0
        while added_edges < m:
            u, v = edges.pop()
            if not (v in G[u] or any(v in G[w] and w in G[u] for w in G[v])):
                G[u].add(v)
                G[v].add(u)
                added_edges += 1
        return G
    
    def girth(G):
        n = len(G)
        distances = {i: float('inf') for i in range(n)}
        distances[0] = 0
        queue = [0]
        while queue:
            u = queue.pop(0)
            for v in G[u]:
                if distances[v] == float('inf'):
                    distances[v] = distances[u] + 1
                    queue.append(v)
        return min(distances.values())
    
    def is_subgraph(H, G):
        return all(u in G and v in G[u] for u, v in H)
    
    def communication_complexity(G, H):
        if not is_subgraph(H, G):
            return float('inf')
        
        n = len(G)
        m = len(H)
        K = {i: set() for i in range(n)}
        for u in range(n//2):
            K[u].add(u + n//2)
            K[u + n//2].add(u)
        
        def hamming_distance(A, B):
            return sum(a != b for a, b in zip(A, B))
        
        def min_hamming_distance(subgraph, graph):
            distances = [float('inf')] * len(graph)
            queue = [0]
            distances[0] = 0
            while queue:
                u = queue.pop(0)
                for v in subgraph[u]:
                    if distances[v] == float('inf'):
                        distances[v] = distances[u] + 1
                        queue.append(v)
            return min(distances)
        
        def estimate_complexity(subgraph, graph):
            n = len(graph)
            m = len(subgraph)
            K = {i: set() for i in range(n)}
            for u in range(n//2):
                K[u].add(u + n//2)
                K[u + n//2].add(u)
            
            distances = [float('inf')] * len(graph)
            queue = [0]
            distances[0] = 0
            while queue:
                u = queue.pop(0)
                for v in subgraph[u]:
                    if distances[v] == float('inf'):
                        distances[v] = distances[u] + 1
                        queue.append(v)
            
            return sum(distances) / m
        
        complexity = estimate_complexity(H, G)
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        G = generate_graph(n)
        if girth(G) < n:
            continue
        
        H = {i: set() for i in range(n)}
        edges = [(u, v) for u in range(n) for v in range(u+1, n)]
        random.shuffle(edges)
        m = n // 2
        added_edges = 0
        while added_edges < m:
            u, v = edges.pop()
            if not (v in H[u] or any(v in H[w] and w in H[u] for w in H[v])):
                H[u].add(v)
                H[v].add(u)
                added_edges += 1
        
        complexity = communication_complexity(G, H)
        total_complexity += complexity
        instances_tested += 1
    
    mean_complexity = total_complexity / instances_tested if instances_tested > 0 else float('inf')
    conjecture_holds = mean_complexity >= 0.5 * (n + math.log2(n)) and all(complexity >= 0.8 * (n - math.log2(n)) for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_complexity = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")