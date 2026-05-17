# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def matrix_mult(a, b):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_sub(a, b):
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]

def matrix_scale(a, scalar):
    n = len(a)
    return [[a[i][j] * scalar for j in range(n)] for i in range(n)]

def matrix_det(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in matrix[1:]]
        det += ((-1) ** col) * matrix[0][col] * matrix_det(minor)
    return det

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    vertices = list(range(n))
    adj = defaultdict(list)
    remaining_vertices = vertices.copy()
    random.shuffle(remaining_vertices)
    while remaining_vertices:
        v1 = remaining_vertices.pop()
        for _ in range(3):
            if not remaining_vertices:
                break
            v2 = random.choice(remaining_vertices)
            adj[v1].append(v2)
            adj[v2].append(v1)
            remaining_vertices.remove(v2)
    return adj

def generate_random_3_regular_graph(n):
    while True:
        adj = generate_3_regular_graph(n)
        if len(adj) == n and all(len(adj[v]) == 3 for v in adj):
            return adj

def is_connected(adj):
    if not adj:
        return False
    visited = set()
    stack = [next(iter(adj))]
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            stack.extend(adj[v])
    return len(visited) == len(adj)

def generate_connected_3_regular_graph(n):
    while True:
        adj = generate_random_3_regular_graph(n)
        if is_connected(adj):
            return adj

def generate_omega(n):
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[0] = 1 - omega[0]
    return omega

def build_adjacency_matrix(adj, n):
    matrix = [[0] * n for _ in range(n)]
    for v in adj:
        for u in adj[v]:
            matrix[v][u] = 1
    return matrix

def compute_ihara_entropy(adj, n):
    A = build_adjacency_matrix(adj, n)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    term1 = matrix_scale(I, 11/9)
    term2 = matrix_scale(A, 1/3)
    matrix = matrix_sub(term1, term2)
    det = matrix_det(matrix)
    if det <= 0:
        return float('nan')
    return (1/n) * math.log(det)

def dpll(clauses, assignment, n):
    if all(any(literal in assignment for literal in clause) for clause in clauses):
        return 1
    unit_clause = next((clause for clause in clauses if len(clause) == 1 and not any(literal in assignment for literal in clause)), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        return dpll(clauses, new_assignment, n)
    for var in range(1, n+1):
        if var not in assignment and -var not in assignment:
            new_assignment = assignment.copy()
            new_assignment[var] = True
            result = dpll(clauses, new_assignment, n)
            new_assignment[var] = False
            result += dpll(clauses, new_assignment, n)
            return result
    return 0

def generate_tseitin_cnf(adj, omega, n):
    clauses = []
    for v in adj:
        neighbors = adj[v]
        for i in range(3):
            for j in range(i+1, 3):
                u, w = neighbors[i], neighbors[j]
                clauses.append([-v, -u, -w])
                clauses.append([v, u, w])
                clauses.append([-v, u, -w])
                clauses.append([v, -u, w])
    for v in range(n):
        clauses.append([-v if omega[v] == 0 else v])
    return clauses

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        adj = generate_connected_3_regular_graph(n)
        omega = generate_omega(n)
        A = build_adjacency_matrix(adj, n)
        h = compute_ihara_entropy(adj, n)
        if math.isnan(h):
            continue
        clauses = generate_tseitin_cnf(adj, omega, n)
        leaves = dpll(clauses, {}, n)
        log_leaves = math.log2(leaves) if leaves > 0 else 0
        lower_bound = (1/20) * n * h - 1
        upper_bound = 20 * n * h + math.log2(n) + 1
        if log_leaves < lower_bound or log_leaves > upper_bound:
            conjecture_holds = False
            counterexample = f"n={n}, seed={seed}, log_leaves={log_leaves}, lower_bound={lower_bound}, upper_bound={upper_bound}"
            break
        metric_values.append(log_leaves)
        instances_tested += 1

    return {
        "metric_name": "log2(DPLL leaves)",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")