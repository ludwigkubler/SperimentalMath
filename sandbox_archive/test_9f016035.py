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
    n = random.randint(5, 40)
    G = generate_random_planar_graph(n)
    
    mvol_G = compute_minimal_hyperbolic_volume(G)
    ccom_G = compute_communication_complexity(G)
    
    if mvol_G is None or ccom_G is None:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = compute_correlation(mvol_G, ccom_G)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) > 0.8 and abs(compute_mean_absolute_difference(mvol_G, ccom_G)) <= 3,
        "counterexample": "" if correlation_coefficient > 0.8 and abs(compute_mean_absolute_difference(mvol_G, ccom_G)) <= 3 else "Pearson Correlation Coefficient < 0.8 or Mean Absolute Difference > 3"
    }

def generate_random_planar_graph(n: int) -> list:
    # Implement a simple planar graph generator
    if n == 1:
        return [[], []]
    
    G = [[] for _ in range(n)]
    edges = set()
    
    def add_edge(u, v):
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            G[u].append(v)
            G[v].append(u)
    
    # Add initial edges to form a cycle
    for i in range(n - 1):
        add_edge(i, i + 1)
    add_edge(0, n - 1)
    
    # Add additional edges while ensuring planarity
    for _ in range(n - 3):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and u not in G[v] and (u, v) not in edges:
            add_edge(u, v)
    
    return G

def compute_minimal_hyperbolic_volume(G: list) -> float:
    # Implement the algorithm for minimal hyperbolic volume
    # Placeholder implementation: return a random value between 0 and n
    return random.uniform(0, len(G))

def compute_communication_complexity(G: list) -> int:
    # Implement the standard algorithm for communication complexity of planar graphs
    # Placeholder implementation: return the number of edges
    return sum(len(neighbors) for neighbors in G) // 2

def compute_correlation(x: float, y: float) -> float:
    # Compute Pearson correlation coefficient
    if x == 0 or y == 0:
        return 0
    
    return (x * y - 1) / math.sqrt((x**2 - 1) * (y**2 - 1))

def compute_mean_absolute_difference(x: float, y: float) -> float:
    # Compute mean absolute difference
    if x == 0 or y == 0:
        return 0
    
    return abs(x - y)

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")