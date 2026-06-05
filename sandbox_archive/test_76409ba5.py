# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for i in range(n):
        neighbors = random.sample(range(n), d - 1)
        while any(j in graph[i] for j in neighbors):
            neighbors = random.sample(range(n), d - 1)
        for neighbor in neighbors:
            add_edge(i, neighbor)
    
    return graph

def eta_invariant(graph):
    n = len(graph)
    if n == 0 or all(len(neighbors) == 0 for neighbors in graph):
        return Fraction(0, 1)
    
    d = sum(len(neighbors) for neighbors in graph) // n
    return Fraction(n * (n - 1) // 2, d)

def monotone_width(graph):
    n = len(graph)
    if n == 0:
        return 0
    
    def dfs(node, visited, path):
        if node in visited:
            return 0
        visited.add(node)
        path.append(node)
        
        max_width = 1
        for neighbor in graph[node]:
            width = dfs(neighbor, visited, path)
            if width > max_width:
                max_width = width
        
        path.pop()
        visited.remove(node)
        return max_width
    
    visited = set()
    max_width = 0
    for node in range(n):
        width = dfs(node, visited, [])
        if width > max_width:
            max_width = width
    
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    eta_values = []
    w_mon_values = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, d=3)  # Assuming a 3-regular graph for simplicity
        eta = eta_invariant(graph)
        w_mon = monotone_width(graph)
        
        eta_values.append(eta)
        w_mon_values.append(w_mon)
    
    if len(eta_values) < 30 or len(w_mon_values) < 30:
        return {
            "metric_name": "eta_invariant",
            "metric_value": None,
            "instances_tested": len(eta_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation = sum((eta - eta_mean) * (w_mon - w_mon_mean) for eta, w_mon in zip(eta_values, w_mon_values)) / len(eta_values)
    eta_mean = sum(eta_values) / len(eta_values)
    w_mon_mean = sum(w_mon_values) / len(w_mon_values)
    
    if correlation < 0.7:
        return {
            "metric_name": "eta_invariant",
            "metric_value": None,
            "instances_tested": len(eta_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"low_correlation={correlation}"
        }
    
    mean_abs_diff = sum(abs(eta - w_mon) for eta, w_mon in zip(eta_values, w_mon_values)) / len(eta_values)
    
    if mean_abs_diff > 2:
        return {
            "metric_name": "eta_invariant",
            "metric_value": None,
            "instances_tested": len(eta_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"high_mean_abs_diff={mean_abs_diff}"
        }
    
    return {
        "metric_name": "eta_invariant",
        "metric_value": correlation,
        "instances_tested": len(eta_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Default list of prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" in r for r in results):
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{' '.join(counterexamples)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")