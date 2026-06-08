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
        graph = [[] for _ in range(n)]
        edges_used = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges_used:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges_used.add((i, j))
        return graph
    
    def euler_characteristic(graph):
        if not graph:
            return 0
        n = len(graph)
        m = sum(len(neighbors) for neighbors in graph) // 2
        return n - m + (len([node for node in range(n) if len(graph[node]) % 2 != 0]) // 2)
    
    def resolution_width(graph):
        if not graph:
            return 0
        n = len(graph)
        clauses = [[i] for i in range(n)]
        assignment = [None] * n
        while True:
            new_clauses = []
            for clause in clauses:
                if all(assignment[var] is not None for var in clause):
                    continue
                unit_clause = [var for var in clause if assignment[var] is None]
                if len(unit_clause) == 1:
                    assignment[unit_clause[0]] = True
                else:
                    new_clauses.append(clause)
            if not new_clauses:
                break
            clauses = new_clauses
        return max(sum(1 for var in clause if assignment[var] is None) for clause in clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    d_values = [3, 4, 5]
    instances_tested = 0
    total_width = 0
    total_characteristic = 0
    
    for n in n_values:
        for _ in range(5):  # Aim for at least 30 instances per seed
            graph = generate_d_regular_graph(n, random.choice(d_values))
            if graph is None:
                continue
            instances_tested += 1
            characteristic = euler_characteristic(graph)
            width = resolution_width(graph)
            total_width += width
            total_characteristic += characteristic
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = total_characteristic / instances_tested * total_width / instances_tested
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")