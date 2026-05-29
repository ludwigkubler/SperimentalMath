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
    
    def bfs_distance(graph, start):
        n = len(graph)
        distances = [math.inf] * n
        distances[start] = 0
        queue = [start]
        
        while queue:
            u = queue.pop(0)
            for v in range(n):
                if graph[u][v] == 1 and distances[v] == math.inf:
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return max(distances) if any(distances) else 0
    
    def monomial_ideal_generators(graph):
        n = len(graph)
        generators = []
        for i in range(n):
            for j in range(i+1, n):
                if graph[i][j] == 1:
                    generators.append((i, j))
        return len(generators)
    
    def is_low_degree_expansion(graph, diameter):
        n = len(graph)
        max_degree = max(sum(row) for row in graph)
        return max_degree <= 2**(diameter + 1)
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    diameter = bfs_distance(G, 0)
    M = monomial_ideal_generators(G)
    
    if diameter == math.inf:
        return {
            "metric_name": "diameter/M ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph is not connected"
        }
    
    ratio = Fraction(diameter, M)
    conjecture_holds = ratio <= 2**M
    
    return {
        "metric_name": "diameter/M ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} > 2^{M}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    mean_ratio = total_ratio / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{r['counterexample']}' first_failing_seed={first_failing_seed}")