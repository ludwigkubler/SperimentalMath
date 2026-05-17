# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_scale(a, scalar):
    return [[a[i][j] * scalar for j in range(len(a[0]))] for i in range(len(a))]

def matrix_identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

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
        return None
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    adj = [[0] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] += 1
        adj[v][u] += 1
    if any(sum(row) != 3 for row in adj):
        return None
    return adj

def generate_odd_omega(n):
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[random.randint(0, n-1)] ^= 1
    return omega

def build_tseitin_cnf(adj, omega):
    n = len(adj)
    clauses = []
    for u in range(n):
        neighbors = [v for v in range(n) if adj[u][v] == 1]
        for v in neighbors:
            if v > u:
                clauses.append([u, v, n + len(clauses)])
                clauses.append([-u, -v, n + len(clauses)])
    for u in range(n):
        clauses.append([u] if omega[u] == 1 else [-u])
    return clauses

def unit_propagate(clauses, assignment):
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            unassigned = [lit for lit in clause if abs(lit) not in assignment]
            if len(unassigned) == 1:
                lit = unassigned[0]
                val = lit > 0
                if abs(lit) not in assignment:
                    assignment[abs(lit)] = val
                    changed = True
    return clauses, assignment

def dpll(clauses, assignment, variables):
    clauses, assignment = unit_propagate(clauses, assignment)
    if any(len(clause) == 0 for clause in clauses):
        return 0
    if not any(clause for clause in clauses if any(abs(lit) not in assignment for lit in clause)):
        return 1
    for var in variables:
        if var not in assignment:
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                new_clauses = [clause for clause in clauses if not any(lit == var if val else lit == -var for lit in clause)]
                result = dpll(new_clauses, new_assignment, variables)
                if result > 0:
                    return result
            return 0
    return 0

def compute_ihara_entropy(adj):
    n = len(adj)
    a = matrix_scale(adj, Fraction(1, 3))
    i = matrix_scale(matrix_identity(n), Fraction(11, 9))
    matrix = matrix_sub(i, a)
    det = matrix_det(matrix)
    if det <= 0:
        return 0.0
    h = (1.0 / n) * math.log(det)
    return h

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(30):
            adj = None
            while adj is None:
                adj = generate_3_regular_graph(n)
            omega = generate_odd_omega(n)
            clauses = build_tseitin_cnf(adj, omega)
            variables = list(range(n))
            assignment = {}
            leaves = dpll(clauses, assignment, variables)
            if leaves == 0:
                continue
            log_leaves = math.log2(leaves)
            h = compute_ihara_entropy(adj)
            if h <= 0:
                continue
            lower_bound = (1/20) * n * h - 1
            upper_bound = 20 * n * h + math.log2(n) + 1
            if log_leaves < lower_bound or log_leaves > upper_bound:
                conjecture_holds = False
                counterexample = f"n={n}, seed={seed}, log_leaves={log_leaves}, h={h}, lower_bound={lower_bound}, upper_bound={upper_bound}"
                break
            metric_values.append(log_leaves)
            instances_tested += 1
        if not conjecture_holds:
            break

    if instances_tested == 0:
        return {
            "metric_name": "log2_leaves",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2_leaves",
        "metric_value": mean_metric,
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

    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")