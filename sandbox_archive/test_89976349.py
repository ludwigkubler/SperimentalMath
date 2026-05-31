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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
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
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if (i, j) not in graph and (j, i) not in graph:
                        clauses.append([f'-{literals[i]}', f'-{literals[j]}', literals[k]])
                        clauses.append([f'-{literals[i]}', f'-{literals[k]}', literals[j]])
                        clauses.append([f'-{literals[j]}', f'-{literals[k]}', literals[i]])
        return clauses
    
    def resolution_width(clauses):
        if not clauses:
            return 0
        queue = [clauses]
        while queue:
            clause = queue.pop()
            for lit in clause:
                if lit.startswith('-'):
                    neg_lit = lit[1:]
                else:
                    neg_lit = '-' + lit
                new_clauses = []
                for c in queue:
                    if neg_lit in c:
                        new_clause = [l for l in c if l != neg_lit]
                        if not new_clause:
                            return len(clause)
                        new_clauses.append(new_clause)
                    else:
                        new_clauses.append(c)
                queue.extend(new_clauses)
        return 0
    
    def minimal_local_index(graph):
        n = len(graph)
        indices = [0] * n
        for i in range(n):
            for j in graph[i]:
                if indices[i] < indices[j]:
                    indices[i], indices[j] = indices[j], indices[i]
        return max(indices) - min(indices)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    results = []
    for _ in range(30):
        d = random.randint(2, 4)
        n = random.randint(5, 10)
        graph = generate_d_regular_graph(d, n)
        if not graph:
            continue
        clauses = tseitin_formula(graph)
        w_phi_G = resolution_width(clauses)
        i_G = minimal_local_index(graph)
        results.append((i_G, w_phi_G))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    x, y = zip(*results)
    corr_coeff = pearson_correlation(x, y)
    return {
        "metric_name": "Pearson correlation",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": n,
        "conjecture_holds": abs(corr_coeff) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation did not meet threshold\" first_failing_seed={first_failing_seed}")