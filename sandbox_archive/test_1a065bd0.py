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
    
    adj_matrix = [[0] * n for _ in range(n)]
    edges_added = 0
    
    while edges_added < (n * d) // 2:
        u, v = random.sample(range(n), 2)
        if adj_matrix[u][v] == 0 and u != v:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
            edges_added += 1
    
    return adj_matrix

def tseitin_formula(graph):
    n = len(graph)
    literals = list(range(1, n + 1))
    clauses = []
    
    for i in range(n):
        clause = [literals[i]]
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                clause.append(-literals[j])
        clauses.append(clause)
    
    return literals, clauses

def hodge_decomposition(graph):
    n = len(graph)
    laplacian = [[0] * n for _ in range(n)]
    
    for i in range(n):
        degree = sum(graph[i][j] for j in range(n))
        laplacian[i][i] = degree
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                laplacian[i][j] = -1
                laplacian[j][i] = -1
    
    eigenvalues = []
    
    for _ in range(n):
        max_eigenvalue = None
        max_vector = [0] * n
        
        for i in range(100):  # Power iteration method
            vector = [random.uniform(-1, 1) for _ in range(n)]
            vector /= sum(x**2 for x in vector)**0.5
            
            new_vector = [sum(laplacian[i][j] * vector[j] for j in range(n)) for i in range(n)]
            new_vector /= sum(x**2 for x in new_vector)**0.5
            
            if max_eigenvalue is None or abs(sum(vector[j] * new_vector[j] for j in range(n))) > abs(max_eigenvalue):
                max_eigenvalue = sum(vector[j] * new_vector[j] for j in range(n))
                max_vector = new_vector
        
        eigenvalues.append(max_eigenvalue)
    
    return min(eigenvalues)

def clause_subset_complexity(clauses):
    return len(clauses) ** 0.5

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
    
    return cov_xy / (std_x * std_y)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)
        literals, clauses = tseitin_formula(graph)
        h_value = hodge_decomposition(graph)
        psi_value = clause_subset_complexity(clauses)
        
        results.append((h_value, psi_value))
    
    if len(results) < 16:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n <= 40),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    h_values = [r[0] for r in results]
    psi_values = [r[1] for r in results]
    correlation_coefficient = pearson_correlation(h_values, psi_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n <= 40),
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient={result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_instances")