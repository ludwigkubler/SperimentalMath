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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def is_expander(G, epsilon=0.1):
    n = len(G)
    d = sum(len(neighbors) for neighbors in G.values()) / (2 * n)
    if d <= 0:
        return False
    lambda_max = max(abs(eigenvalue) for eigenvalue in compute_eigenvalues(G))
    return lambda_max >= (1 + epsilon) * d

def compute_eigenvalues(G):
    # Power iteration method to approximate largest eigenvalue
    n = len(G)
    A = [[0]*n for _ in range(n)]
    for u, neighbors in G.items():
        degree_u = len(neighbors)
        for v in neighbors:
            A[u][v] += 1 / degree_u
            A[v][u] += 1 / degree_u
    
    x = [Fraction(1, n) for _ in range(n)]
    max_iter = 1000
    for _ in range(max_iter):
        x_new = matrix_multiplication(A, x)
        norm = sum(x_new[i]**2 for i in range(n))**0.5
        x = [x_new[i] / norm for i in range(n)]
    
    lambda_max = max(abs(sum(x[i] * A[i][j] for j in range(n))) for i in range(n))
    return [lambda_max]

def tseitin_formula(G):
    n = len(G)
    clauses = []
    variables = {}
    for u, neighbors in G.items():
        if not neighbors:
            continue
        var_u = f"x{u}"
        variables[u] = var_u
        clause = [-int(var_u)]
        for v in neighbors:
            var_v = f"x{v}"
            clauses.append([int(var_u), int(var_v)])
            clauses.append([-int(var_u), -int(var_v)])
            clauses.append([int(var_v)])
        clauses.append(clause)
    return clauses, variables

def dpll(clauses, assignment):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        var = abs(literal) - 1
        new_assignment = assignment.copy()
        new_assignment[var] = literal > 0
        return dpll([c for c in clauses if not (literal in c or -literal in c)], new_assignment)
    pure_literal = next((v for v, count in Counter([l for c in clauses for l in c]).items() if count % 2 != 0), None)
    if pure_literal is not None:
        var = abs(pure_literal) - 1
        new_assignment = assignment.copy()
        new_assignment[var] = pure_literal > 0
        return dpll([c for c in clauses if not (pure_literal in c or -pure_literal in c)], new_assignment)
    literal = next((l for l, _ in Counter([l for c in clauses for l in c]).items() if l > 0), None)
    var = abs(literal) - 1
    return dpll(clauses, assignment | {var: True}) or dpll(clauses, assignment | {var: False})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = {}
    for i in range(n):
        neighbors = [j for j in range(n) if j != i and random.random() < 0.3]
        G[i] = neighbors
    
    clique_complex_barcode_lengths = []
    for u in range(n):
        subgraph = {v: set(G[v]) & set(G[u]) for v in G if v != u}
        barcode_length = len(compute_eigenvalues(subgraph))
        clique_complex_barcode_lengths.append(barcode_length)
    
    max_barcode_length = max(clique_complex_barcode_lengths)
    is_expander_graph = is_expander(G)
    resolution_length = 0
    for _ in range(10):  # Simulate 10 refutations
        clauses, variables = tseitin_formula(G)
        assignment = {}
        if dpll(clauses, assignment):
            continue
        resolution_length += 1
    
    c = 0.2
    conjecture_holds = resolution_length >= 2**(c * max_barcode_length)
    counterexample = "" if conjecture_holds else f"Graph with n={n}, A={G}"
    
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_length,
        "instances_tested": len(clique_complex_barcode_lengths),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")