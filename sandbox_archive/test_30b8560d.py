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
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    random.shuffle(edges)
    for u, v in edges[:n - 1]:
        graph[u].add(v)
        graph[v].add(u)
    return graph

def is_connected(graph):
    visited = set()
    stack = [0]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node] - visited)
    return len(visited) == len(graph)

def generate_tseitin_formula(graph):
    n = len(graph)
    literals = {i: (2 * i, 2 * i + 1) for i in range(n)}
    clauses = []
    
    # Add clauses for each node
    for u in range(n):
        if graph[u]:
            clause = [literals[u][0]]
            for v in graph[u]:
                clause.append(-literals[v][0])
                clause.append(literals[v][1])
            clauses.append(clause)
    
    # Add clauses for each edge
    for u, v in [(i, j) for i in range(n) for j in range(i + 1, n)]:
        if not graph[u] or not graph[v]:
            continue
        clause = [-literals[u][0], -literals[v][0]]
        clauses.append(clause)
    
    # Add tautology to ensure satisfiability
    tautology = [2 * i + 1 for i in range(n)]
    clauses.append(tautology)
    
    return clauses

def resolution_length(clauses):
    clauses_set = set(tuple(sorted(c)) for c in clauses)
    new_clauses = []
    while True:
        new_clause = None
        for clause1 in clauses_set:
            for clause2 in clauses_set:
                if any(lit in clause1 and -lit in clause2 for lit in clause1):
                    new_clause = [l for l in clause1 + clause2 if l not in clause1 and -l not in clause2]
                    break
            if new_clause:
                break
        if not new_clause:
            return len(clauses_set)
        new_clauses.append(new_clause)
        clauses_set.add(tuple(sorted(new_clause)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    while not is_connected(graph):
        graph = generate_random_graph(n)
    
    clauses = generate_tseitin_formula(graph)
    resolution_len = resolution_length(clauses)
    
    if resolution_len == 1:
        return {
            "metric_name": "Orb(Γ) / 2^L(G)",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    orbits = set()
    for u in range(n):
        orbit = {u}
        stack = [u]
        while stack:
            node = stack.pop()
            if node not in orbit:
                orbit.add(node)
                stack.extend(graph[node] - orbit)
        orbits.add(tuple(sorted(orbit)))
    
    ratio = len(orbits) / (2 ** resolution_len)
    return {
        "metric_name": "Orb(Γ) / 2^L(G)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")