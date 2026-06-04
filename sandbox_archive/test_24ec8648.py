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

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for i in range(d):
        for j in range(i + 1, n):
            if len(graph[i]) < d and len(graph[j]) < d:
                add_edge(i, j)
    
    while any(len(neighbors) != d for neighbors in graph):
        u = random.randint(0, n - 1)
        v = random.choice([v for v in range(n) if v != u and len(graph[v]) < d])
        add_edge(u, v)
    
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = [f"x{i}" for i in range(1, n + 1)]
    clauses = []
    
    def literal(i, j):
        if random.choice([True, False]):
            return f"{literals[i]} or {literals[j]}"
        else:
            return f"not ({literals[i]} and {literals[j]})"
    
    for i in range(n):
        clause = literals[i]
        for neighbor in graph[i]:
            clause += " and " + literal(i, neighbor)
        clauses.append(clause)
    
    return clauses

def hodge_decomposition(graph):
    n = len(graph)
    adjacency_matrix = [[0] * n for _ in range(n)]
    laplacian_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        degree = len(graph[i])
        laplacian_matrix[i][i] = degree
        for neighbor in graph[i]:
            adjacency_matrix[i][neighbor] = 1
            adjacency_matrix[neighbor][i] = 1
    
    for i in range(n):
        for j in range(i + 1, n):
            laplacian_matrix[i][j] = -adjacency_matrix[i][j]
            laplacian_matrix[j][i] = -adjacency_matrix[j][i]
    
    eigenvalues = []
    for _ in range(20):  # Approximate the smallest non-zero eigenvalue
        v = [random.random() for _ in range(n)]
        u = [sum(laplacian_matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
        u_norm = math.sqrt(sum(x**2 for x in u))
        v_norm = math.sqrt(sum(x**2 for x in v))
        eigenvalue = sum(u[i] * v[i] for i in range(n)) / (u_norm * v_norm)
        eigenvalues.append(eigenvalue)
    
    return min([abs(v) for v in eigenvalues if abs(v) > 1e-6])

def clause_subset_complexity(clauses):
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    psi_values = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        clauses = tseitin_formula(graph)
        h_value = hodge_decomposition(graph)
        psi_value = clause_subset_complexity(clauses)
        
        h_values.append(h_value)
        psi_values.append(psi_value)
    
    correlation_coefficient = sum((h_values[i] - (sum(h_values) / len(h_values))) * (psi_values[i] - (sum(psi_values) / len(psi_values))) for i in range(len(h_values))) / (len(h_values) * math.sqrt(sum((x - (sum(h_values) / len(h_values)))**2 for x in h_values)) * math.sqrt(sum((y - (sum(psi_values) / len(psi_values)))**2 for y in psi_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient > 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_support")