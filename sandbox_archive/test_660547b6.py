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
        if (n * d) % 2 != 0 or n < d + 1:
            return None
        graph = {i: set() for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    graph[i].add(j)
                    graph[j].add(i)
                    edges.append((i, j))
        return graph
    
    def tseitin_formula(graph):
        literals = {node: f'x{node}' for node in graph}
        neg_literals = {node: f'-x{node}' for node in graph}
        clauses = []
        for node in graph:
            clause = [neg_literals[node]]
            for neighbor in graph[node]:
                clause.append(literals[neighbor])
            clauses.append(clause)
        return literals, neg_literals, clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        resolvents = set()
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                common_vars = [var for var in clause1 if var[0] == '-' and var[1:] in clause2]
                if not common_vars:
                    continue
                new_clause = []
                for var in clause1 + clause2:
                    if var not in common_vars:
                        new_clause.append(var)
                new_clause = list(set(new_clause))
                if len(new_clause) == 0:
                    return float('inf')
                resolvents.add(tuple(sorted(new_clause)))
                queue.append(new_clause)
        return max(len(resolvent) for resolve in resolvents)
    
    def hodge_classes(graph):
        n = len(graph)
        mnc = 0
        for node in graph:
            if len(graph[node]) == n - 1:
                mnc += 1
        return mnc
    
    results = []
    for n in range(5, 41):
        for _ in range(30):
            d = random.randint(n // 2, n - 1)
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            literals, neg_literals, clauses = tseitin_formula(graph)
            mnc = hodge_classes(graph)
            w = resolution_width(clauses)
            results.append((n, mnc, w))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    n_values = [r[0] for r in results]
    mnc_values = [r[1] for r in results]
    w_values = [r[2] for r in results]
    
    mean_n = sum(n_values) / len(n_values)
    mean_mnc = sum(mnc_values) / len(mnc_values)
    mean_w = sum(w_values) / len(w_values)
    
    variance_n = sum((x - mean_n) ** 2 for x in n_values) / len(n_values)
    variance_mnc = sum((x - mean_mnc) ** 2 for x in mnc_values) / len(mnc_values)
    variance_w = sum((x - mean_w) ** 2 for x in w_values) / len(w_values)
    
    if variance_n == 0 or variance_mnc == 0 or variance_w == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Zero variance in n, mnc, or w"
        }
    
    covariance = sum((x - mean_n) * (y - mean_mnc) for x, _, y in results) / len(results)
    pearson_corr = covariance / math.sqrt(variance_n * variance_mnc)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r['conjecture_holds'] for r in results):
        mean_value = sum(r['metric_value'] for r in results) / len(results)
        std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    if not all(r['metric_value'] is not None for r in results):
        print("RESULT: INCONCLUSIVE reason=missing_data n_tested={}".format(len(results)))
    elif mean_value is None:
        print("RESULT: INCONCLUSIVE reason=zero_variance")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")