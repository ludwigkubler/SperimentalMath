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
        return None
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    remaining = n
    while remaining > 0:
        u = random.choice(vertices)
        v = random.choice(vertices)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
            remaining -= 2
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if len(edges) != 3 * n // 2:
        return None
    return adj

def generate_odd_omega(n):
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[0] = 1 - omega[0]
    return omega

def build_adjacency_matrix(adj, n):
    matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            matrix[u][v] = 1
    return matrix

def compute_ihara_entropy(A, n):
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    scaled_I = matrix_scale(I, 11/9)
    scaled_A = matrix_scale(A, 1/3)
    M = matrix_sub(scaled_I, scaled_A)
    det_M = matrix_det(M)
    if det_M <= 0:
        return None
    H = (1/n) * math.log(det_M)
    return H

def build_tseitin_cnf(adj, omega, n):
    cnf = []
    for u in range(n):
        neighbors = adj[u]
        for v in neighbors:
            if u < v:
                cnf.append([u, v, n + len(cnf)])
                cnf.append([-u, -v, n + len(cnf)])
    for u in range(n):
        cnf.append([u, -u, n + len(cnf), omega[u]])
    return cnf

def dpll_solver(cnf, assignment, leaves):
    if not cnf:
        leaves[0] += 1
        return True
    for clause in cnf:
        if all(lit == False for lit in clause):
            return False
    unit_clause = None
    for clause in cnf:
        if len(clause) == 1:
            unit_clause = clause[0]
            break
    if unit_clause is not None:
        new_assignment = assignment.copy()
        new_assignment[abs(unit_clause)] = unit_clause > 0
        new_cnf = []
        for c in cnf:
            if unit_clause not in c:
                new_cnf.append([lit for lit in c if lit != -unit_clause])
        return dpll_solver(new_cnf, new_assignment, leaves)
    for var in range(1, len(assignment) + 1):
        if var not in assignment:
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                new_cnf = []
                for c in cnf:
                    if var not in [abs(lit) for lit in c]:
                        new_cnf.append(c)
                    elif (val and var in c) or (not val and -var in c):
                        new_cnf.append([lit for lit in c if lit != var and lit != -var])
                if dpll_solver(new_cnf, new_assignment, leaves):
                    return True
            return False
    return False

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(30 // len(n_values)):
            adj = None
            while adj is None:
                adj = generate_3_regular_graph(n)
            omega = generate_odd_omega(n)
            A = build_adjacency_matrix(adj, n)
            H = compute_ihara_entropy(A, n)
            if H is None:
                continue
            cnf = build_tseitin_cnf(adj, omega, n)
            leaves = [0]
            assignment = {}
            dpll_solver(cnf, assignment, leaves)
            log_leaves = math.log2(leaves[0])
            lower_bound = (1/20) * n * H - 1
            upper_bound = 20 * n * H + math.log2(n) + 1
            if log_leaves < lower_bound or log_leaves > upper_bound:
                conjecture_holds = False
                counterexample = f"n={n}, H={H}, log_leaves={log_leaves}, lower_bound={lower_bound}, upper_bound={upper_bound}"
                break
            metric_values.append(log_leaves)
            instances_tested += 1
        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "log2(leaves)",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2(leaves)",
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
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] != 0.0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")