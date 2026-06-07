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

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = {i: [] for i in range(n)}
    edges_added = set()
    for u in range(n):
        for v in range(u + 1, n):
            if len(graph[u]) == d and len(graph[v]) == d:
                break
            if (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
    return graph

def is_valid_d_regular_graph(G, n, d):
    for u in range(n):
        if len(G[u]) != d:
            return False
    return True

def geometric_entropy(graph, n):
    degrees = [len(graph[i]) for i in range(n)]
    total_degrees = sum(degrees)
    entropy = 0.0
    for degree in degrees:
        p = Fraction(degree, total_degrees)
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy

def resolution_proof_width(graph):
    n = len(graph)
    visited = [False] * n
    stack = []
    width = 0
    
    def dfs(u):
        nonlocal width
        stack.append(u)
        visited[u] = True
        
        for v in graph[u]:
            if not visited[v]:
                dfs(v)
        
        stack.pop()
        visited[u] = False
        width = max(width, len(stack))
    
    for u in range(n):
        if not visited[u]:
            dfs(u)
    
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = 2 * (n - 1) // n
        G = generate_d_regular_graph(n, d)
        if not is_valid_d_regular_graph(G, n, d):
            return {
                "metric_name": "resolution_proof_width",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        H_G = geometric_entropy(G, n)
        if H_G == 0:
            continue
        
        w_phi_G = resolution_proof_width(G)
        results.append(w_phi_G / H_G**2)
    
    if not results:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    conjecture_holds = all(x <= 10 for x in results)  # Arbitrary constant c
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std={math.sqrt(sum((result['metric_value'] - (sum(result['metric_value'] for result in results) / len(results)))**2 for result in results) / len(results))} support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")