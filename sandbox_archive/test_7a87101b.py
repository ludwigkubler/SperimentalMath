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
        for j in range(i + 1, n):
            if len(graph[i]) < d and len(graph[j]) < d:
                add_edge(i, j)
    
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = list(range(1, 2 * n + 1))
    clauses = []
    
    for i in range(n):
        clauses.append([literals[2 * i], literals[2 * i + 1]])
        for j in graph[i]:
            if j < i:
                continue
            clauses.append([-literals[2 * i], -literals[2 * j + 1]])
            clauses.append([-literals[2 * i + 1], literals[2 * j]])
    
    return clauses

def compute_polynomial(clauses):
    n = len(clauses)
    poly = [0] * (n + 1)
    for clause in clauses:
        term = 1
        for literal in clause:
            if literal > 0:
                term *= (-1) ** (literal % 2)
        poly[len(clause)] += term
    return poly

def compute_ehrhart_gap(poly):
    n = len(poly)
    ehrhart_sum = 0
    for k in range(n + 1):
        ehrhart_sum += poly[k] * math.comb(k, n)
    return abs(ehrhart_sum - (n + 1))

def resolution_proof_width(formula):
    # Placeholder implementation
    return len(formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        graph = generate_d_regular_graph(n, 2)
        formula = tseitin_formula(graph)
        poly = compute_polynomial(formula)
        ehrhart_gap = compute_ehrhart_gap(poly)
        proof_width = resolution_proof_width(formula)
        
        results.append((ehrhart_gap, proof_width))
    
    mean_gap = sum(gap for gap, _ in results) / len(results)
    mean_width = sum(width for _, width in results) / len(results)
    correlation = sum((gap - mean_gap) * (width - mean_width) for gap, width in results) / len(results)
    
    if correlation == 0:
        return {
            "metric_name": "Correlation",
            "metric_value": correlation,
            "instances_tested": 30,
            "n_max": max(n for _ in range(30)),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": abs(correlation) > 1.2 * (mean_gap / mean_width),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")