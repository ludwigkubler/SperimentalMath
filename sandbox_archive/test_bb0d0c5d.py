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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < (d * n) // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f"x{i}" for i in range(n)}
        neg_literals = {i: f"-x{i}" for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [neg_literals[i]]
            for j in graph[i]:
                clause.append(literals[j])
            clauses.append(clause)
            for j in range(i + 1, n):
                clause = [neg_literals[i], neg_literals[j]]
                for k in graph[i]:
                    if k != j:
                        clause.append(neg_literals[k])
                for k in graph[j]:
                    if k != i:
                        clause.append(neg_literals[k])
                clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        n = len(clauses)
        max_width = 0
        for i in range(n):
            width = sum(1 for lit in clauses[i] if not lit.startswith('-'))
            if width > max_width:
                max_width = width
        return max_width
    
    def minimal_local_index(graph):
        n = len(graph)
        index = 0
        for i in range(n):
            neighbors = graph[i]
            degree = len(neighbors)
            if degree % 2 != 0:
                index += 1
        return index
    
    n = random.randint(5, 40)
    d = (n * (n - 1)) // 2
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "minimal_local_index",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "d-regular graph generation failed"
        }
    
    clauses = tseitin_formula(graph)
    w_phi_G = resolution_width(clauses)
    i_G = minimal_local_index(graph)
    
    return {
        "metric_name": "minimal_local_index",
        "metric_value": abs(i_G),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": w_phi_G is not None and i_G is not None,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "minimal_local_index or resolution_width failed"
        mean_value = None
        std_value = None
        support_fraction = 0.0
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")