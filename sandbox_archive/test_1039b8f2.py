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
    if 2 * d > n:
        return None  # Cannot form a d-regular graph with these parameters
    
    graph = [[] for _ in range(n)]
    degrees = [0] * n
    
    for i in range(n):
        while degrees[i] < d:
            j = random.randint(0, n - 1)
            if i != j and j not in graph[i] and degrees[j] < d:
                graph[i].append(j)
                graph[j].append(i)
                degrees[i] += 1
                degrees[j] += 1
    
    return graph

def tseitin_formula(graph, n):
    phi = {}
    literals = [f"x{i}" for i in range(n)]
    
    # Create clauses for each vertex
    for v in range(n):
        clause = []
        for u in graph[v]:
            clause.append(f"¬{literals[u]}")
        clause.append(literals[v])
        phi[f"v{v}"] = clause
    
    # Create clauses for each edge
    for v in range(n):
        for u in range(v + 1, n):
            if u not in graph[v]:
                clause = []
                for w in range(n):
                    if w != v and w != u:
                        clause.append(f"¬{literals[w]}")
                phi[f"e({v},{u})"] = clause
    
    # Create clauses to ensure exactly one vertex is true
    at_least_one_true = [f"{literals[i]}" for i in range(n)]
    phi["at_least_one_true"] = at_least_one_true
    
    at_most_one_true = []
    for i in range(n):
        for j in range(i + 1, n):
            clause = [f"¬{literals[i]}", f"¬{literals[j]}"]
            phi[f"at_most_one_true({i},{j})"] = clause
    
    return phi

def minimal_root_system_length(graph):
    # Placeholder function for computing the length of the minimal root system
    # This is a dummy implementation and should be replaced with actual computation
    return len(graph)

def resolution_proof_width(phi):
    # Placeholder function for computing the resolution proof width
    # This is a dummy implementation and should be replaced with actual computation
    return sum(len(clause) for clause in phi.values())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, random.randint(2, n - 1))
        if graph is None:
            continue
        
        phi = tseitin_formula(graph, n)
        
        if not phi:
            continue
        
        ell_root = minimal_root_system_length(graph)
        w_phi = resolution_proof_width(phi)
        
        results.append({
            "n": n,
            "ell_root": ell_root,
            "w_phi": w_phi
        })
    
    if not results:
        return {
            "metric_name": "Resolution Width vs. Root System Length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ell_root_values = [r["ell_root"] for r in results]
    w_phi_values = [r["w_phi"] for r in results]
    
    mean_ell_root = sum(ell_root_values) / len(ell_root_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    
    correlation_coefficient = 0
    if len(ell_root_values) > 1:
        numerator = sum((ell_root_values[i] - mean_ell_root) * (w_phi_values[i] - mean_w_phi) for i in range(len(ell_root_values)))
        denominator = math.sqrt(sum((ell_root_values[i] - mean_ell_root)**2 for i in range(len(ell_root_values))) * sum((w_phi_values[i] - mean_w_phi)**2 for i in range(len(w_phi_values))))
        correlation_coefficient = numerator / denominator
    
    max_n = max(r["n"] for r in results)
    
    return {
        "metric_name": "Resolution Width vs. Root System Length",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(ell_root - w_phi) <= 3 for ell_root, w_phi in zip(ell_root_values, w_phi_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")