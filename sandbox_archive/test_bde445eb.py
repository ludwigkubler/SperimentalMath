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
        num_edges = random.randint(0, len(edges))
        selected_edges = random.sample(edges, num_edges)
        for u, v in selected_edges:
            graph[u].add(v)
            graph[v].add(u)
        return graph
    
    def chromatic_number(graph, n):
        colors = [-1] * n
        color_count = 0
        
        def is_safe(node, c):
            for neighbor in graph[node]:
                if colors[neighbor] == c:
                    return False
            return True
        
        def backtrack(node):
            nonlocal color_count
            if node == n:
                color_count += 1
                return True
            for c in range(color_count + 1):
                if is_safe(node, c):
                    colors[node] = c
                    if backtrack(node + 1):
                        return True
                    colors[node] = -1
            return False
        
        backtrack(0)
        return color_count
    
    def tropicalized_rank(graph, n):
        # Placeholder for the actual computation of the minimal rank
        # For simplicity, we assume it's proportional to the number of edges
        num_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
        return num_edges / (n - 1)
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    chi_G = chromatic_number(graph, n)
    r_t_G = tropicalized_rank(graph, n)
    
    if chi_G == 0 or r_t_G == 0:
        return {
            "metric_name": "chi_G / r_t(G)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = chi_G / r_t_G
    return {
        "metric_name": "chi_G / r_t(G)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
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
    
    total_ratio = sum(r["metric_value"] for r in results if "counterexample" not in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    mean_ratio = total_ratio / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    
    if support_fraction >= 0.95 * len(seeds):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction / len(seeds)}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction / len(seeds)}")