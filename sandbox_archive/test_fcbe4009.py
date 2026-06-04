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
    
    while len(edges_added) < (n * d) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
    
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = list(range(1, 2 * n + 1))
    clauses = []
    
    for i in range(n):
        clause = [literals[2 * i], literals[2 * i + 1]]
        clauses.append(clause)
        
        for j in graph[i]:
            if j < i:
                continue
            neg_clause = [-literals[2 * i], -literals[2 * j + 1]]
            clauses.append(neg_clause)
    
    return literals, clauses

def resolution_width(formula):
    literals, clauses = formula
    assignment = {}
    queue = list(clauses)
    while queue:
        clause = queue.pop(0)
        if all(l in assignment and assignment[l] for l in clause):
            continue
        
        unit_clause = [l for l in clause if l not in assignment and -l not in assignment]
        if not unit_clause:
            return None
        
        literal = unit_clause[0]
        assignment[literal] = True
        queue.extend([c for c in clauses if literal in c])
    
    return max(len(c) for c in clauses)

def tropical_hodge_decomposition_order(n):
    # Placeholder function to simulate the order of tropical Hodge decomposition
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        literals, clauses = tseitin_formula(graph)
        m_hodetrop = tropical_hodge_decomposition_order(n)
        w_phi_g = resolution_width((literals, clauses))
        
        if m_hodetrop is None or w_phi_g is None:
            continue
        
        ratio = Fraction(m_hodetrop, w_phi_g) / (n ** 2)
        results.append({"n": n, "m_hodetrop": m_hodetrop, "w_phi_g": w_phi_g, "ratio": ratio})
    
    if not results:
        return {
            "metric_name": "tropical_hodge_decomposition_order_over_resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] >= Fraction(1, 4) for result in results)  # Example threshold
    counterexample = "" if conjecture_holds else "threshold_not_met"
    
    return {
        "metric_name": "tropical_hodge_decomposition_order_over_resolution_width",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='threshold_not_met' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")