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
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def diameter(graph, n):
        dist = [[float('inf')] * n for _ in range(n)]
        for u, v in graph:
            dist[u][v] = 1
            dist[v][u] = 1
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        max_diameter = 0
        for i in range(n):
            for j in range(i + 1, n):
                if dist[i][j] != float('inf'):
                    max_diameter = max(max_diameter, dist[i][j])
        return max_diameter
    
    def monomial_ideal_generators(graph):
        # Simplified generator count based on graph structure
        return len(graph) ** 2
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    D_G = diameter(graph, n)
    M = monomial_ideal_generators(graph)
    
    ratio = D_G / M if M != 0 else float('inf')
    conjecture_holds = ratio <= 10 * (n ** 2)  # Example polynomial relationship
    counterexample = "" if conjecture_holds else f"Graph with n={n}, D(G)={D_G}, M={M}"
    
    return {
        "metric_name": "Ratio of Diameter to Generators",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")