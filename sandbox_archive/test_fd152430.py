# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if (i, j) not in graph and (j, k) not in graph and (k, i) not in graph:
                        clauses.append([f'-{literals[i]}', f'-{literals[j]}', literals[k]])
        return clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        resolvents = set()
        width = 0
        while queue:
            clause = queue.pop(0)
            if len(clause) > width:
                width = len(clause)
            for other in queue:
                common_literals = [lit for lit in clause if lit.startswith('-') and -int(lit[1:]) in other]
                if common_literals:
                    new_clause = list(set(clause + other) - set(common_literals))
                    if any(new_clause[i].startswith('-') and -int(new_clause[i][1:]) == new_clause[j] for i, j in combinations(range(len(new_clause)), 2)):
                        continue
                    resolvents.add(tuple(sorted(new_clause)))
                    queue.append(list(resolvents.pop()))
        return width
    
    def quotient_sheaves(graph):
        n = len(graph)
        sheaves = [set() for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                if not sheaves[i].intersection(sheaves[j]):
                    sheaves[i] |= {j}
        return sheaves
    
    def min_index(sheaves):
        n = len(sheaves)
        indices = [0] * n
        for i in range(n):
            for j in sheaves[i]:
                if not indices[j]:
                    indices[j] = 1
                else:
                    indices[j] += 1
        return max(indices)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    
    for n in range(5, n_max + 1):
        graph = generate_d_regular_graph(3, n)  # Example with d=3
        if not graph:
            continue
        
        clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        
        sheaves = quotient_sheaves(graph)
        min_index_value = min_index(sheaves)
        
        instances_tested += 1
        total_metric_value += min_index_value * width
    
    if instances_tested < 30:
        return {
            "metric_name": "min_index_times_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_metric = total_metric_value / instances_tested
    std_metric = (sum((x - mean_metric) ** 2 for x in range(5, n_max + 1)) / instances_tested) ** 0.5
    
    return {
        "metric_name": "min_index_times_width",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric = (sum((r["metric_value"] - mean_metric) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "not_enough_instances" for r in results):
        print("RESULT: INCONCLUSIVE not_enough_instances")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={first_failing_seed}")