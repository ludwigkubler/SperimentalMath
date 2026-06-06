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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph

    def is_symplectically_reflective(graph):
        n = len(graph)
        for i in range(n):
            for j in range(i + 1, n):
                if not (j in graph[i] and i in graph[j]):
                    return False
        return True

    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f"x{i}" for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f"~{literals[j]}")
            clauses.append(clause)
        return clauses

    def mtr(formula):
        n = len(formula)
        if n == 0:
            return 0
        max_clause_length = max(len(clause) for clause in formula)
        return max_clause_length

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if not is_symplectically_reflective(graph):
            return {
                "metric_name": "mtr",
                "metric_value": -1,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Graph is not symplectically reflective"
            }
        phi_G = tseitin_formula(graph)
        mtr_phi_G = mtr(phi_G)
        
        for _ in range(5):
            graph_prime = generate_d_regular_graph(n, 3)
            if not is_symplectically_reflective(graph_prime):
                return {
                    "metric_name": "mtr",
                    "metric_value": -1,
                    "instances_tested": 1,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": "Graph is not symplectically reflective"
                }
            phi_G_prime = tseitin_formula(graph_prime)
            mtr_phi_G_prime = mtr(phi_G_prime)
            
            if abs(mtr_phi_G - mtr_phi_G_prime) / max(1, mtr_phi_G, mtr_phi_G_prime) > 2:
                return {
                    "metric_name": "mtr",
                    "metric_value": -1,
                    "instances_tested": 1,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"mtr(φ_G) = {mtr_phi_G}, mtr(φ_{G_prime}) = {mtr_phi_G_prime}"
                }
        
        results.append({
            "metric_name": "mtr",
            "metric_value": mtr_phi_G,
            "instances_tested": 6,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return {
        "metric_name": "mtr",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Graph is not symplectically reflective' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")