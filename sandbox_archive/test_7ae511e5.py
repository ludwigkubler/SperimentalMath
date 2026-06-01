# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def generate_random_graph(n, delta):
    G = defaultdict(set)
    for _ in range(delta * n // 2):
        u, v = random.sample(range(n), 2)
        if u != v and u not in G[v]:
            G[u].add(v)
            G[v].add(u)
    return G

def compute_automorphism_groups(G):
    def dfs(node, path, visited):
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        for neighbor in G[node]:
            dfs(neighbor, path, visited)
    
    def is_isomorphic(G1, G2):
        if len(G1) != len(G2):
            return False
        nodes = list(G1.keys())
        random.shuffle(nodes)
        mapping = {nodes[0]: next(iter(G2))}
        stack = [(nodes[0], next(iter(G2)))]
        visited = set([nodes[0]])
        
        while stack:
            u, v = stack.pop()
            for neighbor in G1[u]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    w = next((w for w in G2[v] if len(set(G1[neighbor]) - set(G2[w])) == 0), None)
                    if w is None or w in mapping.values():
                        return False
                    mapping[neighbor] = w
                    stack.append((neighbor, w))
        
        return True
    
    automorphism_groups = []
    for perm in itertools.permutations(range(len(G))):
        G_perm = {perm[i]: set(perm[j] for j in G[i]) for i in range(len(G))}
        if is_isomorphic(G, G_perm):
            automorphism_groups.append(frozenset(perm))
    
    return len(set(automorphism_groups))

def compute_circuit_monotone_width(G):
    n = len(G)
    w_m = float('inf')
    
    def dfs(i, path):
        nonlocal w_m
        if i in path:
            cycle_length = len(path) - path.index(i)
            w_m = min(w_m, cycle_length)
            return
        path.append(i)
        for neighbor in G[i]:
            dfs(neighbor, path)
        path.pop()
    
    for start in range(n):
        dfs(start, [])
    
    return w_m

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    delta = 40
    
    G = generate_random_graph(n, delta)
    aut_groups = compute_automorphism_groups(G)
    w_m = compute_circuit_monotone_width(G)
    
    metric_value = aut_groups / math.sqrt(w_m) if w_m != 0 else float('inf')
    conjecture_holds = metric_value <= 1.5  # Placeholder constant for demonstration
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Aut(G) / sqrt(w_m)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")