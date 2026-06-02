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

def generate_d_regular_graph(d, n):
    if d * n % 2 != 0:
        return None
    
    graph = [[] for _ in range(n)]
    edges_added = 0
    
    def add_edge(u, v):
        nonlocal edges_added
        if u == v or v in graph[u] or u in graph[v]:
            return False
        graph[u].append(v)
        graph[v].append(u)
        edges_added += 1
        return True
    
    while edges_added < d * n // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if add_edge(u, v):
            pass
        else:
            continue
    
    return graph

def adjacency_matrix(graph, n):
    matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            matrix[u][v] = 1
            matrix[v][u] = 1
    return matrix

def spectral_radius(matrix):
    n = len(matrix)
    eigenvalues = []
    
    def det(A, k):
        if k == 0:
            return 1
        det_val = 0
        for col in range(k):
            A[0][col] = 0
            sub_matrix = [row[:col] + row[col+1:] for row in A[1:]]
            det_val += (-1) ** col * A[0][col] * det(sub_matrix, k - 1)
        return det_val
    
    def power_method(A, max_iter=100):
        n = len(A)
        x = [Fraction(1, n)] * n
        for _ in range(max_iter):
            y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            norm_y = sum(y[i] ** 2 for i in range(n)) ** Fraction(1, 2)
            x = [y[i] / norm_y for i in range(n)]
        return max(abs(x[i]) for i in range(n))
    
    eigenvalues.append(power_method(matrix))
    return eigenvalues[0]

def tseitin_formula(graph):
    n = len(graph)
    literals = {i: f'x{i}' for i in range(n)}
    clauses = []
    
    def add_clause(literals, clause):
        clauses.append(clause)
    
    for u in range(n):
        if not graph[u]:
            continue
        disjunctive_clauses = [f'-{literals[u]}']
        for v in graph[u]:
            disjunctive_clauses.append(f'{literals[v]}')
        add_clause(literals, disjunctive_clauses)
    
    return clauses

def dpll_solver(clauses):
    def is_satisfiable(clauses, assignment={}):
        if not clauses:
            return True
        literal = next(iter(clauses[0]))
        pos_literal = literal.lstrip('-')
        if pos_literal in assignment and assignment[pos_literal] == (literal.startswith('-')):
            return False
        new_assignment = assignment.copy()
        new_assignment[pos_literal] = not literal.startswith('-')
        if is_satisfiable([c for c in clauses if literal not in c and pos_literal not in c], new_assignment):
            return True
        new_assignment.pop(pos_literal, None)
        if is_satisfiable([c for c in clauses if literal not in c and pos_literal not in c], new_assignment):
            return True
        return False
    
    return is_satisfiable(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d = 3
    n_max = 40
    instances_tested = 0
    correlation_sum = 0.0
    h_values = []
    w_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            graph = generate_d_regular_graph(d, n)
            if graph is None:
                continue
            
            h_G = spectral_radius(adjacency_matrix(graph, n))
            phi_G = tseitin_formula(graph)
            
            if not phi_G:
                continue
            
            proof_depths = [dpll_solver(phi_G) for _ in range(30)]
            avg_proof_depth = sum(proof_depths) / len(proof_depths)
            
            h_values.append(h_G)
            w_values.append(avg_proof_depth)
            instances_tested += 1
    
    if not instances_tested:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    correlation = sum((h_values[i] - mean_h) * (w_values[i] - mean_w) for i in range(instances_tested)) / instances_tested
    mean_h = sum(h_values) / instances_tested
    mean_w = sum(w_values) / instances_tested
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.7) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.5 or not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.5 or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")