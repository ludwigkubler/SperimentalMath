# auto-injected by SEC sandbox
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
import collections
import fractions
import json

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_scalar_mult(a, s):
    return [[a[i][j] * s for j in range(len(a[0]))] for i in range(len(a))]

def matrix_sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_transpose(a):
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]

def matrix_determinant(a):
    n = len(a)
    if n == 1:
        return a[0][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in a[1:]]
        det += ((-1) ** col) * a[0][col] * matrix_determinant(minor)
    return det

def gaussian_elimination(a):
    n = len(a)
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(a[k][i]) > abs(a[max_row][i]):
                max_row = k
        a[i], a[max_row] = a[max_row], a[i]
        for k in range(i+1, n):
            c = -a[k][i] / a[i][i]
            for j in range(i, n+1):
                if i == j:
                    a[k][j] = 0
                else:
                    a[k][j] += c * a[i][j]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = a[i][n] / a[i][i]
        for k in range(i-1, -1, -1):
            a[k][n] -= a[k][i] * x[i]
    return x

def generate_3_regular_graph(n):
    if n % 2 != 0:
        return None
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    remaining_vertices = vertices.copy()
    while remaining_vertices:
        v1 = remaining_vertices.pop()
        v2 = random.choice(remaining_vertices)
        edges.append((v1, v2))
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def is_connected(adj):
    n = len(adj)
    visited = [False] * n
    stack = [0]
    visited[0] = True
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
    return all(visited)

def generate_random_3_regular_graph(n):
    while True:
        adj = generate_3_regular_graph(n)
        if adj and is_connected(adj):
            return adj

def generate_random_omega(n):
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[random.randint(0, n-1)] ^= 1
    return omega

def build_adjacency_matrix(adj):
    n = len(adj)
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in adj[i]:
            a[i][j] = 1
    return a

def compute_ihara_entropy(a, n):
    identity = [[fractions.Fraction(11, 9) if i == j else 0 for j in range(n)] for i in range(n)]
    a_frac = [[fractions.Fraction(x, 3) for x in row] for row in a]
    matrix = matrix_sub(identity, a_frac)
    det = matrix_determinant(matrix)
    if det <= 0:
        return None
    h = (1 / n) * math.log(det)
    return h

def build_tseitin_cnf(adj, omega):
    n = len(adj)
    clauses = []
    for i in range(n):
        neighbors = adj[i]
        for j in range(len(neighbors)):
            for k in range(j+1, len(neighbors)):
                u, v = neighbors[j], neighbors[k]
                clauses.append([-i-1, -u-1, -v-1])
                clauses.append([i-1, u-1, v-1])
                clauses.append([i-1, -u-1, -v-1])
                clauses.append([-i-1, u-1, -v-1])
                clauses.append([-i-1, -u-1, v-1])
                clauses.append([i-1, u-1, -v-1])
                clauses.append([i-1, -u-1, v-1])
                clauses.append([-i-1, u-1, v-1])
    for i in range(n):
        if omega[i] == 1:
            clauses.append([i-1])
        else:
            clauses.append([-i-1])
    return clauses

def dpll_solver(clauses, assignment, n):
    if not clauses:
        return 1
    for clause in clauses:
        if all(lit < 0 and -lit-1 in assignment for lit in clause):
            return 0
    for clause in clauses:
        if len(clause) == 1:
            lit = clause[0]
            if lit > 0:
                if lit-1 in assignment:
                    continue
                new_assignment = assignment.copy()
                new_assignment.add(lit-1)
                new_clauses = [c for c in clauses if lit-1 not in c]
                new_clauses = [[x for x in c if x != -lit-1] for c in new_clauses]
                return dpll_solver(new_clauses, new_assignment, n)
            else:
                if -lit-1 in assignment:
                    continue
                new_assignment = assignment.copy()
                new_assignment.add(-lit-1)
                new_clauses = [c for c in clauses if -lit-1 not in c]
                new_clauses = [[x for x in c if x != lit-1] for c in new_clauses]
                return dpll_solver(new_clauses, new_assignment, n)
    for var in range(n):
        if var not in assignment and -var-1 not in assignment:
            new_assignment1 = assignment.copy()
            new_assignment1.add(var)
            new_clauses1 = [c for c in clauses if var not in c]
            new_clauses1 = [[x for x in c if x != -var-1] for c in new_clauses1]
            count1 = dpll_solver(new_clauses1, new_assignment1, n)
            new_assignment2 = assignment.copy()
            new_assignment2.add(-var-1)
            new_clauses2 = [c for c in clauses if -var-1 not in c]
            new_clauses2 = [[x for x in c if x != var+1] for c in new_clauses2]
            count2 = dpll_solver(new_clauses2, new_assignment2, n)
            return count1 + count2
    return 0

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        adj = generate_random_3_regular_graph(n)
        omega = generate_random_omega(n)
        a = build_adjacency_matrix(adj)
        h = compute_ihara_entropy(a, n)
        if h is None:
            continue
        clauses = build_tseitin_cnf(adj, omega)
        leaves = dpll_solver(clauses, set(), n)
        if leaves == 0:
            continue
        log_leaves = math.log2(leaves)
        lower_bound = (1/20) * n * h - 1
        upper_bound = 20 * n * h + math.log2(n) + 1
        if log_leaves < lower_bound or log_leaves > upper_bound:
            conjecture_holds = False
            counterexample = f"n={n}, seed={seed}, log_leaves={log_leaves}, lower_bound={lower_bound}, upper_bound={upper_bound}"
            break
        metric_values.append(log_leaves)
        instances_tested += 1
    if conjecture_holds and len(metric_values) >= 30:
        return {
            "metric_name": "log2(leaves)",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "log2(leaves)",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexample if counterexample else "mapping_undefined"
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    metric_values = [r["metric_value"] for r in results if r["metric_value"] != 0.0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        if counterexamples:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=no_counterexamples")