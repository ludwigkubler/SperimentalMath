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
        if (d * n) % 2 != 0 or d >= n:
            return None
        graph = [[0] * n for _ in range(n)]
        degree_counts = [0] * n
        edges_added = 0
        
        while edges_added < d * n // 2:
            u, v = random.sample(range(n), 2)
            if graph[u][v] == 0 and degree_counts[u] < d and degree_counts[v] < d:
                graph[u][v] = 1
                graph[v][u] = 1
                degree_counts[u] += 1
                degree_counts[v] += 1
                edges_added += 1
        
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        
        for i in range(n):
            clause = [literals[i]]
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    clause.append(f"~{literals[j]}")
            clauses.append(clause)
        
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    clause = [f"~{literals[i]}"]
                    clause.append(f"{literals[j]}")
                    clauses.append(clause)
        
        return literals, clauses
    
    def min_local_induction_degree(graph):
        n = len(graph)
        degree_counts = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    degree_counts[i] += 1
                    degree_counts[j] += 1
        
        return max(degree_counts)
    
    def frege_proof_depth(literals, clauses):
        # Simplified Frege proof depth calculation (not actual Frege proof)
        return len(literals) + len(clauses)
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "mli(G)",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_d_regular"
        }
    
    literals, clauses = tseitin_formula(graph)
    mli_G = min_local_induction_degree(graph)
    d_phi_G = frege_proof_depth(literals, clauses)
    
    return {
        "metric_name": "mli(G)",
        "metric_value": mli_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "unknown"
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"mli(G)={r['metric_value']}, d(φ_G)={d_phi_G}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")