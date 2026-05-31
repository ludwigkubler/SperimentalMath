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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
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
        for (i, j) in edges:
            clauses.append([f'-{literals[i]}', f'{literals[j]}'])
            clauses.append([f'{literals[i]}', f'-{literals[j]}'])
        return len(clauses)
    
    def automorphism_group(graph):
        n = len(graph)
        vertices = list(range(n))
        aut = []
        for perm in itertools.permutations(vertices):
            if all(graph[perm[i]][perm[j]] == graph[i][j] for i, j in edges):
                aut.append(perm)
        return aut
    
    def log2(x):
        if x <= 0:
            return None
        return math.log2(x)
    
    d_values = [3, 4, 5, 6, 7, 8, 9, 10]
    results = []
    for d in d_values:
        n = random.randint(5, 30)
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        phi_G = tseitin_formula(graph)
        A_G = automorphism_group(graph)
        if not A_G:
            continue
        log_A_G = log2(len(A_G))
        results.append((log_A_G, phi_G))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    mean_log_A_G = sum(x for x, _ in results) / n
    mean_phi_G = sum(y for _, y in results) / n
    cov = sum((x - mean_log_A_G) * (y - mean_phi_G) for x, y in results) / n
    var_log_A_G = sum((x - mean_log_A_G) ** 2 for x, _ in results) / n
    var_phi_G = sum((y - mean_phi_G) ** 2 for _, y in results) / n
    pearson_corr = cov / (math.sqrt(var_log_A_G) * math.sqrt(var_phi_G))
    
    valid_results = [x for x, y in results if x is not None and y is not None]
    support_fraction = sum(1 for x, y in valid_results if 0.5 <= x / y <= 1.5) / len(valid_results)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": n,
        "n_max": max(n for _, n in results),
        "conjecture_holds": pearson_corr >= 0.8 and support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if all(result["conjecture_holds"] for result in results):
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE")