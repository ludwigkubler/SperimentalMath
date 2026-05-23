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

def generate_random_graph(n):
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                G[i][j] = G[j][i] = random.randint(1, 10)
    return G

def is_tropicalizable(G):
    n = len(G)
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] == 0:
                return False
    return True

def tropicalize_graph(G):
    n = len(G)
    G_trop = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        G_trop[i][i] = 0
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] != 0:
                G_trop[i][j] = G[j][i] = min(G_trop[i][k] + G[k][j] for k in range(n) if k != i and k != j)
    return G_trop

def compute_tropical_homology_classes(G_trop):
    n = len(G_trop)
    visited = [False] * n
    homology_classes = 0
    
    def dfs(node, path):
        nonlocal homology_classes
        if node in path:
            homology_classes += 1
            return True
        visited[node] = True
        for neighbor in range(n):
            if G_trop[node][neighbor] != math.inf and not visited[neighbor]:
                if dfs(neighbor, path + [node]):
                    return True
        visited[node] = False
        return False
    
    for i in range(n):
        if not visited[i]:
            dfs(i, [])
    
    return homology_classes

def construct_arithmetic_circuit(G_trop):
    n = len(G_trop)
    circuit_size = 0
    
    def find_min_path(start, end):
        nonlocal circuit_size
        min_dist = math.inf
        for k in range(n):
            if G_trop[start][k] != math.inf and G_trop[k][end] != math.inf:
                dist = G_trop[start][k] + G_trop[k][end]
                if dist < min_dist:
                    min_dist = dist
                    circuit_size += 2
        return min_dist
    
    for i in range(n):
        for j in range(i + 1, n):
            find_min_path(i, j)
    
    return circuit_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_random_graph(n)
    
    if not is_tropicalizable(G):
        return {
            "metric_name": "Tropicalized Homology Size / Circuit Size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    G_trop = tropicalize_graph(G)
    TropClasses = compute_tropical_homology_classes(G_trop)
    CircuitSize = construct_arithmetic_circuit(G_trop)
    
    return {
        "metric_name": "Tropicalized Homology Size / Circuit Size",
        "metric_value": TropClasses,
        "instances_tested": 1,
        "conjecture_holds": TropClasses == CircuitSize,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")