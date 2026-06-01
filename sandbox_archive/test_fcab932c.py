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
    n = 10  # Start with a small size and increase if needed
    max_degree = 40
    instances_tested = 30
    n_max = n
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        G = generate_random_graph(n, max_degree)
        aut_count = count_automorphism_groups(G)
        w_m = compute_circuit_monotone_width(G)
        
        if w_m == 0:
            continue
        
        ratio = Fraction(aut_count, math.sqrt(w_m))
        if conjecture_holds and ratio > 1:  # Adjust the constant factor as needed
            conjecture_holds = False
            counterexample = f"Ratio {ratio} exceeds acceptable bound for n={n}"
        
        n_max = max(n_max, n)
    
    return {
        "metric_name": "Ratio of Automorphism Groups to sqrt(Circuit Monotone Width)",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_random_graph(n: int, max_degree: int) -> list:
    G = [[] for _ in range(n)]
    edges = set()
    
    for i in range(n):
        degree = random.randint(1, min(max_degree, n - 1))
        neighbors = random.sample(range(n), degree)
        for neighbor in neighbors:
            if (i, neighbor) not in edges and (neighbor, i) not in edges:
                G[i].append(neighbor)
                G[neighbor].append(i)
                edges.add((i, neighbor))
    
    return G

def count_automorphism_groups(G: list) -> int:
    # This is a placeholder for the actual automorphism group counting algorithm
    # For simplicity, we'll use a brute-force approach to count unique subgraphs
    n = len(G)
    subgraphs = set()
    
    def dfs(node, path):
        if node not in path:
            path.append(node)
            for neighbor in G[node]:
                dfs(neighbor, path)
            subgraphs.add(tuple(sorted(path)))
            path.pop()
    
    for i in range(n):
        dfs(i, [])
    
    return len(subgraphs)

def compute_circuit_monotone_width(G: list) -> int:
    # This is a placeholder for the actual circuit monotone width computation algorithm
    # For simplicity, we'll use a brute-force approach to find the smallest monotone circuit
    n = len(G)
    w_m = float('inf')
    
    def dfs(node, path):
        if node not in path:
            path.append(node)
            for neighbor in G[node]:
                dfs(neighbor, path)
            if len(path) < w_m:
                w_m = len(path)
            path.pop()
    
    for i in range(n):
        dfs(i, [])
    
    return w_m

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")