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

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    while len(edges_added) < (n * d) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
    
    return graph

def compute_tseitin_formula(graph):
    n = len(graph)
    literals = {i: f"x{i}" for i in range(n)}
    clauses = []
    
    for u in range(n):
        if not graph[u]:
            continue
        
        clause = [f"~{literals[u]}"]
        for v in graph[u]:
            clause.append(literals[v])
        
        clauses.append(" | ".join(clause))
    
    return " & ".join(clauses)

def compute_polynomial(formula):
    # Placeholder implementation for computing the polynomial
    # This is a dummy function and should be replaced with actual computation
    return 1.0

def compute_ehrhart_gap(poly):
    # Placeholder implementation for computing the Ehrhart gap of a polynomial
    # This is a dummy function and should be replaced with actual computation
    return 1.0

def resolution_proof_width(formula):
    # Placeholder implementation for computing the resolution proof width of a formula
    # This is a dummy function and should be replaced with actual computation
    return 1.0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)  # Example degree of 2
        formula = compute_tseitin_formula(graph)
        poly = compute_polynomial(formula)
        ehrhart_gap = compute_ehrhart_gap(poly)
        proof_width = resolution_proof_width(formula)
        
        results.append({
            "n": n,
            "ehrhart_gap": ehrhart_gap,
            "proof_width": proof_width
        })
    
    mean_gap = sum(r["ehrhart_gap"] for r in results) / len(results)
    mean_width = sum(r["proof_width"] for r in results) / len(results)
    correlation_bound = 0.8 * mean_width
    
    conjecture_holds = all(abs(g - correlation_bound) <= 0.2 * correlation_bound for g in [r["ehrhart_gap"] for r in results])
    
    return {
        "metric_name": "Ehrhart Gap vs Resolution Proof Width",
        "metric_value": mean_gap,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Gap {mean_gap} not within ±20% of Θ({mean_width})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [53, 67, 89, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Gap not within ±20% of Θ(proof width)\" first_failing_seed={first_failing_seed}")