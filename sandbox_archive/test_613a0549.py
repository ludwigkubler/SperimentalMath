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
    
    # Generate a random graph with n vertices
    n = 30
    G = {i: set() for i in range(n)}
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    num_edges = random.randint(2 * n, 3 * n)
    for _ in range(num_edges):
        u, v = random.choice(edges)
        G[u].add(v)
        G[v].add(u)
    
    # Compute the diameter of the graph
    def bfs_distance(graph, start):
        queue = [(start, 0)]
        visited = {start}
        while queue:
            node, dist = queue.pop(0)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        return max(distances.values()) if distances else 0
    
    distances = bfs_distance(G, 0)
    D_G = max(distances.values())
    
    # Compute the monomial ideal I(G) and its maximum number of generators M
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    def generate_monomial_ideal(G, n):
        ideal = set()
        for i in range(n):
            for j in G[i]:
                ideal.add((i, j))
        return ideal
    
    I_G = generate_monomial_ideal(G, n)
    M = len(I_G)
    
    # Check the conjecture
    c = 1.0
    if D_G > c * (M ** 2):
        return {
            "metric_name": "D(G)/M",
            "metric_value": D_G / M,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": f"D(G)={D_G}, M={M}"
        }
    
    # Check the second part of the conjecture
    def low_degree_expansion(graph, n):
        for i in range(n):
            neighbors = graph[i]
            if len(neighbors) > 2:
                return False
        return True
    
    if not low_degree_expansion(G, n):
        return {
            "metric_name": "D(G)/M",
            "metric_value": D_G / M,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": f"Graph does not have a low-degree expansion"
        }
    
    # Check the third part of the conjecture
    if len(I_G) > 2 ** (c * D_G):
        return {
            "metric_name": "D(G)/M",
            "metric_value": D_G / M,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": f"Number of generators exceeds 2^(c*D(G))"
        }
    
    return {
        "metric_name": "D(G)/M",
        "metric_value": D_G / M,
        "instances_tested": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph does not satisfy the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")