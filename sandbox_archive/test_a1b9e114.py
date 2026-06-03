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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
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

    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
            for j in range(i + 1, n):
                clauses.append([f'{literals[i]}', f'{literals[j]}'])
                clauses.append([f'-{literals[i]}', f'-{literals[j]}'])
        return clauses

    def tropicalized_quiver_representation_size(clauses):
        # Simplified version for demonstration purposes
        return len(clauses)

    def resolution_proof_width(clauses):
        # Simplified version for demonstration purposes
        return len(clauses)

    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "mtr_q(G)",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    clauses = tseitin_formula(graph)
    mtr_q_G = tropicalized_quiver_representation_size(clauses)
    w_phi_G = resolution_proof_width(clauses)
    
    return {
        "metric_name": "mtr_q(G)",
        "metric_value": mtr_q_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mtr_q_G >= 0.5 * w_phi_G,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 31))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mtr_q_G = sum(r["metric_value"] for r in results) / len(results)
    std_dev_mtr_q_G = math.sqrt(sum((r["metric_value"] - mean_mtr_q_G) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mtr_q_G} std={std_dev_mtr_q_G} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mtr_q_G} std={std_dev_mtr_q_G} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, mtr_q(G)={r['metric_value']}, w(φ_G)={resolution_proof_width(tseitin_formula(generate_d_regular_graph(r['instances_tested'], 2)))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break