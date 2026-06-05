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

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(2*n)]
    clauses = []
    
    # Generate clauses for the OR gates
    for i in range(n):
        clause = f"({variables[i]} v {variables[n+i+1]})"
        clauses.append(clause)
    
    # Generate clauses for the AND gates
    for i in range(n):
        clause = f"~{variables[2*n+i]} -> ({variables[i]} ^ ~{variables[n+i+1]})"
        clauses.append(clause)
    
    # Generate the final clause
    final_clause = 'v'.join(variables[:n])
    clauses.append(final_clause)
    
    return clauses

def generate_random_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    while len(edges_added) < (n * d) // 2:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
    
    return graph

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def compute_sheaf_order(graph):
    n = len(graph)
    identity_matrix = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    
    # Compute the adjacency matrix
    adj_matrix = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            adj_matrix[u][v] = Fraction(1, 1)
            adj_matrix[v][u] = Fraction(1, 1)
    
    # Compute the (n+1)th power of the adjacency matrix
    result_matrix = identity_matrix[:]
    for _ in range(n):
        new_matrix = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    new_matrix[i][j] += adj_matrix[i][k] * result_matrix[k][j]
        result_matrix = new_matrix
    
    # Compute the minimal order of sheaves
    min_sheaf_order = 0
    for row in result_matrix:
        if any(x != Fraction(0, 1) for x in row):
            min_sheaf_order += 1
    
    return min_sheaf_order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_graph(n, d=3)
        clauses = generate_tseitin_formula(n)
        
        min_sheaf_order = compute_sheaf_order(graph)
        resolution_width = len(clauses)  # Simplified for testing purposes
        
        if resolution_width == 0:
            return {
                "metric_name": "ratio",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "resolution_width_zero"
            }
        
        ratio = Fraction(min_sheaf_order, resolution_width)
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    std_dev = (sum((x - mean_ratio)**2 for x in results) / len(results))**0.5
    
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": 6,
        "n_max": max(n_values),
        "conjecture_holds": abs(mean_ratio - n) < 0.1 * n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_dev = (sum((x - mean_value)**2 for x in results) / len(results))**0.5
    support_fraction = len(results) / len(seeds)
    
    if all(trial_result["conjecture_holds"] for trial_result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_ratio_outside_threshold' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")