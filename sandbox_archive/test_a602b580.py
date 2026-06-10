# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = [[False] * n for _ in range(n)]
    degree = [0] * n
    
    for i in range(n):
        while degree[i] < d:
            j = random.randint(0, n-1)
            if i == j or graph[i][j]:
                continue
            graph[i][j] = True
            graph[j][i] = True
            degree[i] += 1
            degree[j] += 1
    
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = [f"x{i}" for i in range(n)]
    clauses = []
    
    def add_clause(clause):
        clauses.append(clause)
    
    for i in range(n):
        clause = [literals[i]]
        for j in range(n):
            if graph[i][j]:
                clause.append(f"~{literals[j]}")
        add_clause(clause)
    
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                clause = [f"~{literals[i]}", f"~{literals[j]}", literals[k]]
                add_clause(clause)
                clause = [f"~{literals[i]}", literals[j], f"~{literals[k]}"]
                add_clause(clause)
                clause = [literals[i], f"~{literals[j]}", f"~{literals[k]}"]
                add_clause(clause)
    
    return literals, clauses

def resolution_width(clauses):
    n = len(clauses)
    queue = []
    unit_clauses = {}
    
    for i in range(n):
        if len(clauses[i]) == 1:
            unit_clauses[clauses[i][0]] = True
            queue.append(clauses[i][0])
    
    while queue:
        literal = queue.pop(0)
        for i in range(n):
            if literal in clauses[i]:
                continue
            new_clause = [x for x in clauses[i] if x != f"~{literal}"]
            if len(new_clause) == 1:
                unit_clauses[new_clause[0]] = True
                queue.append(new_clause[0])
            else:
                clauses[i] = new_clause
    
    return n - len(unit_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    if seed % 2 == 0:
        n_max = 30
    else:
        n_max = 40
    
    instances_tested = 0
    total_metric_value = 0.0
    min_order_values = []
    resolution_widths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            literals, clauses = tseitin_formula(graph)
            if literals is None or clauses is None:
                continue
            
            min_order = len(literals)  # Simplified for demonstration purposes
            resolution_width_value = resolution_width(clauses)
            
            instances_tested += 1
            total_metric_value += min_order * resolution_width_value
            min_order_values.append(min_order)
            resolution_widths.append(resolution_width_value)
    
    if instances_tested == 0:
        return {
            "metric_name": "min_order * resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in min_order_values) / instances_tested)
    correlation_coefficient = sum(x * y for x, y in zip(min_order_values, resolution_widths)) / (instances_tested * sum(x**2 for x in min_order_values)**0.5 * sum(y**2 for y in resolution_widths)**0.5)
    
    return {
        "metric_name": "min_order * resolution_width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.5 and all(x >= -0.5 for x in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and all(r["metric_value"] >= -0.5 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unsupported_metric")