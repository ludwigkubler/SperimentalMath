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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u in range(n):
            if not graph[u]:
                continue
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(f'-{literals[v]}')
            clauses.append(clause)
            for i, v1 in enumerate(graph[u]):
                for j, v2 in enumerate(graph[u][i+1:], i+1):
                    clauses.append([f'-{literals[v1]}', f'-{literals[v2]}', literals[u]])
        return clauses
    
    def symplectic_invariant(clauses):
        n = len(clauses)
        msi = 0
        for clause in clauses:
            if len(clause) == 3:
                msi += 1
        return msi
    
    def resolution_width(clauses):
        # Simplified version of the resolution width calculation
        max_conflict_size = 0
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                if set(clauses[i]) & set(clauses[j]):
                    max_conflict_size = max(max_conflict_size, len(set(clauses[i]) | set(clauses[j])))
        return max_conflict_size
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = (sum((x[i] - mean_x)**2 for i in range(n)) / n) ** 0.5
        std_dev_y = (sum((y[i] - mean_y)**2 for i in range(n)) / n) ** 0.5
        return covariance / (std_dev_x * std_dev_y)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        d = 2  # For simplicity, use a constant degree
        graph = generate_d_regular_graph(n, d)
        if not graph:
            continue
        clauses = tseitin_formula(graph)
        msi_value = symplectic_invariant(clauses)
        width_value = resolution_width(clauses)
        results.append((msi_value, width_value))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    msi_values, width_values = zip(*results)
    correlation_coefficient = pearson_correlation(msi_values, width_values)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results)) ** 0.5
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if 'counterexample' in result)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")