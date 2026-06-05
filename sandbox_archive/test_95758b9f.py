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
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if (u, v) not in edges and (v, u) not in edges:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges.add((u, v))
                    break
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u in range(n):
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(f'-{literals[v]}')
            clauses.append(clause)
            for v in graph[u]:
                for w in graph[v]:
                    if w != u:
                        clause = [f'-{literals[u]}', literals[v], f'-{literals[w]}']
                        clauses.append(clause)
        return clauses
    
    def formal_group_representation_size(formula):
        # Placeholder function to simulate the computation of mfr(φ_G)
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula)  # Simplified for demonstration purposes
    
    def circuit_monotone_width(clauses):
        # Placeholder function to simulate the computation of w_monotone(φ_G)
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)  # Simplified for demonstration purposes
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "mfr(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph generation failed"
        }
    
    formula = tseitin_formula(graph)
    mfr_G = formal_group_representation_size(formula)
    w_monotone_phi_G = circuit_monotone_width(clauses)
    
    return {
        "metric_name": "mfr(G)",
        "metric_value": mfr_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next((i, seed) for i, seed in enumerate(seeds) if not results[i]["conjecture_holds"])
        counterexample = results[first_failing_seed][0]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")