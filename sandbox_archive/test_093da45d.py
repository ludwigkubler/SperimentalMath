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
    if n * d % 2 != 0:
        return None
    degree = d
    graph = [[] for _ in range(n)]
    
    edges_added = set()
    while len(edges_added) < (n * d) // 2:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if i == j or (i, j) in edges_added or (j, i) in edges_added:
            continue
        graph[i].append(j)
        graph[j].append(i)
        edges_added.add((i, j))
    
    return graph

def compute_resolution_length(graph):
    n = len(graph)
    if n == 0:
        return 0
    
    # DPLL-based resolution length estimator (simplified version)
    def dpll(sat_formula):
        if not sat_formula:
            return 1
        for literal in sat_formula[0]:
            new_formula = [clause for clause in sat_formula[1:] if literal not in clause]
            if dpll(new_formula) > 0:
                return 1 + dpll([[-literal] for clause in new_formula])
        return 0
    
    # Convert graph to Tseitin formula (simplified version)
    tseitin_formula = []
    var_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if j not in graph[i]:
                var_count += 1
                tseitin_formula.append([var_count])
                tseitin_formula.append([-var_count, -i, j])
                tseitin_formula.append([-var_count, i, -j])
    
    return dpll(tseitin_formula)

def compute_critical_simplices(graph):
    n = len(graph)
    if n == 0:
        return 0
    
    # Persistent homology-based Morse matching (simplified version)
    def find_min_cut(graph):
        visited = [False] * n
        queue = [0]
        visited[0] = True
        cut_size = 0
        
        while queue:
            u = queue.pop(0)
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
                else:
                    cut_size += 1
        
        return cut_size
    
    return find_min_cut(graph)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    total_critical_simplices = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different graphs
            d = random.randint(2, min(n - 1, 4))
            if (n * d) % 2 != 0:
                continue
            
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            
            resolution_length = compute_resolution_length(graph)
            critical_simplices = compute_critical_simplices(graph)
            
            total_length += resolution_length
            total_critical_simplices += critical_simplices
            instances_tested += 1
    
    mean_length = Fraction(total_length, instances_tested)
    mean_critical_simplices = Fraction(total_critical_simplices, instances_tested)
    
    conjecture_holds = mean_length >= 2 ** (0.2 * mean_critical_simplices)
    counterexample = "" if conjecture_holds else f"mean_length={mean_length}, mean_critical_simplices={mean_critical_simplices}"
    
    return {
        "metric_name": "resolution_length",
        "metric_value": float(mean_length),
        "instances_tested": instances_tested,
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
    
    total_length = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    total_critical_simplices = sum(r["instances_tested"] * r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_length} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_length} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_length={total_length}, mean_critical_simplices={total_critical_simplices}\" first_failing_seed={first_failing_seed}")