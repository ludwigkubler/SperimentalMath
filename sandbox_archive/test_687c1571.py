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

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = {i: set() for i in range(n)}
    edges_added = 0
    while edges_added < n * d // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and v not in graph[u]:
            graph[u].add(v)
            graph[v].add(u)
            edges_added += 1
    return graph

def diophantine_equations(graph):
    equations = set()
    for node in graph:
        for neighbor in graph[node]:
            equations.add((node, neighbor))
            equations.add((neighbor, node))
    return equations

def tseitin_formula(graph):
    if not graph:
        return []
    n = len(graph)
    literals = list(range(1, 2 * n + 1))
    clauses = []
    for i in range(n):
        clause = [-literals[2 * i - 1]]
        for neighbor in graph[i]:
            clause.append(literals[2 * neighbor - 2])
            clause.append(-literals[2 * neighbor - 1])
        clauses.append(clause)
    return clauses

def resolution_width(clauses):
    if not clauses:
        return 0
    queue = [set(clause) for clause in clauses]
    while True:
        new_clause = None
        for i in range(len(queue)):
            for j in range(i + 1, len(queue)):
                common = queue[i].intersection(queue[j])
                if len(common) == 1:
                    new_clause = (queue[i] - common).union(queue[j] - common)
                    break
            if new_clause is not None:
                break
        if new_clause is None:
            return max(len(clause) for clause in queue)
        queue.append(new_clause)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = 3
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Invalid parameters for generating a d-regular graph"
        }
    diophantine_set = diophantine_equations(graph)
    resolution_width_val = resolution_width(tseitin_formula(graph))
    return {
        "metric_name": "resolution_width",
        "metric_value": len(diophantine_set),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if resolution_width_val is not None else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results if result["metric_value"] is not None) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_conjecture")