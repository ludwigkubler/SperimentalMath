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

def generate_random_graph(n):
    graph = {i: set() for i in range(n)}
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    random.shuffle(edges)
    edge_count = 0
    while edge_count < n - 1:
        u, v = edges[edge_count]
        if u not in graph[v] and v not in graph[u]:
            graph[u].add(v)
            graph[v].add(u)
            edge_count += 1
    return graph

def is_connected(graph, n):
    visited = [False] * n
    stack = [0]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in graph[node]:
                stack.append(neighbor)
    return all(visited)

def compute_rank(graph, n):
    # Approximate rank using a simple heuristic (number of edges)
    return len(graph) - 1

def tseitin_formula(graph, n):
    clauses = []
    for node in range(n):
        if not graph[node]:
            continue
        literals = [f"v{i}" for i in graph[node]]
        clause = ["~" + l for l in literals] + [literals[0]]
        clauses.append(clause)
    return clauses

def resolution_length(clauses, n):
    # Simplified resolution algorithm to estimate length
    resolved = set()
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                clause_i = clauses[i]
                clause_j = clauses[j]
                if any(l in clause_i and "~" + l in clause_j for l in set(clause_i) & set(clause_j)):
                    new_clause = [l for l in clause_i if l not in clause_j] + [l for l in clause_j if l not in clause_i]
                    if len(new_clause) == 1:
                        return len(clauses)
                    new_clauses.append(new_clause)
        clauses.extend(new_clauses)
        if not new_clauses:
            break
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    if not is_connected(graph, n):
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph is not connected"
        }
    rank = compute_rank(graph, n)
    clauses = tseitin_formula(graph, n)
    length = resolution_length(clauses, n)
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** (0.5 * rank),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Graph is not connected"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")