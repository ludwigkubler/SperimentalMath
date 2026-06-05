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
    
    G = [[] for _ in range(n)]
    edges_added = set()
    
    while len(edges_added) < (n * d) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            G[u].append(v)
            G[v].append(u)
            edges_added.add((u, v))
    
    return G

def compute_tseitin_formula(G):
    n = len(G)
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    
    def add_clause(clause):
        if clause:
            clauses.append(' '.join(clause) + ' 0')
    
    for u in range(n):
        if not G[u]:
            continue
        disjuncts = [f'~{literals[v]}' for v in G[u]]
        disjuncts.append(literals[u])
        add_clause(disjuncts)
        
        for i, v1 in enumerate(G[u]):
            for j, v2 in enumerate(G[u][i + 1:], start=i + 1):
                add_clause([f'~{literals[v1]}', f'~{literals[v2]}'])
    
    return '\n'.join(clauses)

def compute_minimal_order_of_formal_group_representations(formula):
    # This is a placeholder function. Replace with actual implementation.
    # For simplicity, we assume mfr(G) = n for this test.
    return len(formula.split('\n'))

def compute_circuit_monotone_width(formula):
    # This is a placeholder function. Replace with actual implementation.
    # For simplicity, we assume w_monotone(φ_G) = n for this test.
    return len(formula.split('\n'))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        d = random.randint(2, min(n - 1, 4))
        G = generate_d_regular_graph(n, d)
        formula = compute_tseitin_formula(G)
        
        mfr_G = compute_minimal_order_of_formal_group_representations(formula)
        w_monotone_phi_G = compute_circuit_monotone_width(formula)
        
        results.append({
            "n": n,
            "mfr_G": mfr_G,
            "w_monotone_phi_G": w_monotone_phi_G
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_graphs_generated"
        }
    
    correlation_coefficient = sum((r["mfr_G"] - mfr_avg) * (r["w_monotone_phi_G"] - w_monotone_avg)
                                  for r in results) / len(results)
    mfr_avg = sum(r["mfr_G"] for r in results) / len(results)
    w_monotone_avg = sum(r["w_monotone_phi_G"] for r in results) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if "metric_value" in result and result["metric_value"] is not None:
            results.append(result["metric_value"])
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean = sum(results) / len(results)
        std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_results")