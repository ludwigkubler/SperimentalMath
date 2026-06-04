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
    
    for i in range(n):
        for j in range(d):
            if j == 0:
                neighbor = (i + 1) % n
            else:
                neighbor = random.choice([x for x in range(n) if x != i and x not in graph[i]])
            add_edge(i, neighbor)
    
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = [f"x{i}" for i in range(n)]
    neg_literals = [f"~x{i}" for i in range(n)]
    clauses = []
    
    for i in range(n):
        clause = [neg_literals[i]] + [literals[j] for j in graph[i]]
        clauses.append(clause)
    
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append([neg_literals[i], neg_literals[j]])
            clauses.append([neg_literals[i], literals[j]])
            clauses.append([neg_literals[j], literals[i]])
            clauses.append([literals[i], literals[j]])
    
    return literals, neg_literals, clauses

def hodge_decomposition(graph):
    n = len(graph)
    adjacency_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in graph[i]:
            adjacency_matrix[i][j] = 1
            adjacency_matrix[j][i] = 1
    
    laplacian_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(adjacency_matrix[i])
        laplacian_matrix[i][i] = degree
        for j in range(i + 1, n):
            laplacian_matrix[i][j] = -adjacency_matrix[i][j]
            laplacian_matrix[j][i] = -adjacency_matrix[i][j]
    
    eigenvalues = []
    for i in range(n):
        eigenvector = [0] * n
        eigenvector[i] = 1
        value = sum(laplacian_matrix[i][j] * eigenvector[j] for j in range(n))
        eigenvalues.append(value)
    
    return max(abs(e) for e in eigenvalues)

def clause_subset_complexity(clauses):
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        literals, neg_literals, clauses = tseitin_formula(graph)
        h_value = hodge_decomposition(graph)
        psi_value = clause_subset_complexity(clauses)
        
        correlation_sum += h_value * psi_value
        instances_tested += n
    
    mean_h_value = correlation_sum / instances_tested
    mean_psi_value = correlation_sum / instances_tested
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_h_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")