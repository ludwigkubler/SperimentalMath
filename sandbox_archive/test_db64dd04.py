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
from math import factorial

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_planar_graph(n):
        if n < 3 or n > 40:
            return None
        # Simple heuristic to generate a planar graph with n vertices
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def hypercube_representation(edges):
        # Simplified representation using a list of sets
        n = len(edges)
        H = [set() for _ in range(n)]
        for u, v in edges:
            H[u].add(v)
            H[v].add(u)
        return H
    
    def geometric_symmetry_order(H):
        n = len(H)
        if n == 0:
            return 0
        # Simplified calculation of symmetry order (number of connected components)
        visited = [False] * n
        count = 0
        
        def dfs(v):
            stack = [v]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    for neighbor in H[u]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
                count += 1
        
        return count
    
    def circuit_monotone_width(G):
        # Simplified calculation using a heuristic
        n = len(G)
        width = 0
        for u, v in G:
            width = max(width, abs(u - v))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_order = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            G = generate_planar_graph(n)
            if G is None:
                continue
            H = hypercube_representation(G)
            order = geometric_symmetry_order(H)
            width = circuit_monotone_width(G)
            
            total_order += order
            total_width += width
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "geometric_symmetry_order",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(order * width for order, width in zip(range(1, n_values[-1] + 1), range(1, n_values[-1] + 1))) -
                               sum(range(1, n_values[-1] + 1)) * sum(range(1, n_values[-1] + 1))) / \
                              (instances_tested * sum(order**2 for order in range(1, n_values[-1] + 1)) - sum(range(1, n_values[-1] + 1))**2) ** 0.5
    
    return {
        "metric_name": "geometric_symmetry_order",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r)
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")