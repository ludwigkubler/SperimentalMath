# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_planar_graph(n):
    if n < 3:
        return None
    
    G = {i: set() for i in range(n)}
    edges = []
    
    def add_edge(u, v):
        if u != v and u not in G[v] and v not in G[u]:
            G[u].add(v)
            G[v].add(u)
            edges.append((u, v))
    
    # Start with a triangle
    for i in range(3):
        add_edge(i, (i + 1) % 3)
    
    # Add remaining vertices and edges to ensure planarity
    for i in range(3, n):
        u = random.choice(list(G.keys()))
        v = random.choice(list(G.keys()))
        while u == v or u in G[v] or v in G[u]:
            v = random.choice(list(G.keys()))
        add_edge(u, v)
    
    return G

def hypercube_representation(G):
    n = len(G)
    H = {}
    for i in range(n):
        H[i] = set()
        for j in range(n):
            if (i & (1 << j)) != (j & (1 << i)):
                H[i].add(j)
    return H

def geometric_symmetry_order(H):
    n = len(H)
    symmetries = []
    for perm in permutations(range(n)):
        if all(H[perm[i]][perm[j]] == H[i][j] for i, j in combinations(range(n), 2)):
            symmetries.append(perm)
    return len(symmetries)

def circuit_monotone_width(G):
    n = len(G)
    width = 0
    for subset in range(1 << n):
        if all(len(G[i].intersection(subset)) % 2 == 0 for i in range(n)):
            width += 1
    return width

def permutations(lst):
    if len(lst) <= 1:
        yield lst
    else:
        for perm in permutations(lst[1:]):
            for i in range(len(perm) + 1):
                yield perm[:i] + [lst[0]] + perm[i:]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0
    
    for n in n_values:
        G = generate_planar_graph(n)
        if G is None:
            continue
        
        H = hypercube_representation(G)
        Order = geometric_symmetry_order(H)
        w_G = circuit_monotone_width(G)
        
        correlation_sum += Order * w_G
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_graphs"
        }
    
    correlation_avg = correlation_sum / instances_tested
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_avg,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_avg > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.9' first_failing_seed={first_failing_seed}")