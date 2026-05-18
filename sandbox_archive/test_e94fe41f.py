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

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    vertices = list(range(n))
    edges = []
    while len(edges) < 3 * n // 2:
        u, v = random.sample(vertices, 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    return edges

def generate_odd_charge(n, seed):
    random.seed(seed)
    return [random.randint(0, 1) for _ in range(n)]

def build_tseitin_cnf(G, omega, n):
    clauses = []
    for u in range(n):
        neighbors = [v for (v, w) in G if w == u] + [v for (w, v) in G if w == u]
        clause = [u] + neighbors
        clauses.append(clause)
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                clauses.append([-u, -neighbors[i], -neighbors[j]])
    for u in range(n):
        if omega[u] == 1:
            clauses.append([u])
    return clauses

def matrix_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_subtract(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] - B[i][j]
    return result

def matrix_transpose(A):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[j][i]
    return result

def matrix_vector_multiply(A, v):
    n = len(A)
    result = [0] * n
    for i in range(n):
        for j in range(n):
            result[i] += A[i][j] * v[j]
    return result

def power_iteration(A, num_iterations=100):
    n = len(A)
    b = [random.random() for _ in range(n)]
    for _ in range(num_iterations):
        b = matrix_vector_multiply(A, b)
        norm = math.sqrt(sum(x**2 for x in b))
        if norm == 0:
            break
        b = [x / norm for x in b]
    return b

def compute_laplacian(G, n):
    L = [[0] * n for _ in range(n)]
    for u in range(n):
        degree = sum(1 for (v, w) in G if w == u) + sum(1 for (w, v) in G if w == u)
        L[u][u] = degree
        for (v, w) in G:
            if w == u:
                L[u][v] = -1
        for (w, v) in G:
            if w == u:
                L[u][v] = -1
    return L

def compute_eigenvalues(L):
    n = len(L)
    eigenvalues = []
    for _ in range(n):
        v = power_iteration(L)
        eigenvalue = sum(L[i][j] * v[j] for i in range(n) for j in range(n)) / sum(v[j] * v[j] for j in range(n))
        eigenvalues.append(eigenvalue)
        L = matrix_subtract(L, [[eigenvalue * v[i] * v[j] for j in range(n)] for i in range(n)])
    return sorted(eigenvalues)

def compute_ipr(phi):
    return sum(x**4 for x in phi)

def tree_dpll(clauses, max_decisions=500000):
    decisions = 0
    assignment = {}
    def unit_propagate():
        nonlocal assignment
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unassigned = [lit for lit in clause if abs(lit) not in assignment]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    if abs(lit) not in assignment:
                        assignment[abs(lit)] = lit > 0
                        changed = True
    unit_propagate()
    def dpll():
        nonlocal decisions
        if decisions >= max_decisions:
            return max_decisions
        for clause in clauses:
            if all(abs(lit) in assignment and (lit < 0) == assignment[abs(lit)] for lit in clause):
                return decisions
        for clause in clauses:
            unassigned = [lit for lit in clause if abs(lit) not in assignment]
            if len(unassigned) == 1:
                lit = unassigned[0]
                if abs(lit) not in assignment:
                    assignment[abs(lit)] = lit > 0
                    decisions += 1
                    result = dpll()
                    if result is not None:
                        return result
                    del assignment[abs(lit)]
                    assignment[abs(lit)] = lit < 0
                    decisions += 1
                    result = dpll()
                    if result is not None:
                        return result
                    del assignment[abs(lit)]
                    return None
        for var in range(1, len(clauses) + 1):
            if var not in assignment:
                assignment[var] = True
                decisions += 1
                result = dpll()
                if result is not None:
                    return result
                del assignment[var]
                assignment[var] = False
                decisions += 1
                result = dpll()
                if result is not None:
                    return result
                del assignment[var]
                return None
        return decisions
    return dpll()

def run_trial(seed):
    n_values = [8, 10, 12, 14, 16]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        G = generate_3_regular_graph(n, seed)
        omega = generate_odd_charge(n, seed)
        clauses = build_tseitin_cnf(G, omega, n)
        decisions = tree_dpll(clauses)
        L = compute_laplacian(G, n)
        eigenvalues = compute_eigenvalues(L)
        lambda_2 = eigenvalues[1]
        phi_2 = power_iteration(L)
        ipr = compute_ipr(phi_2)

        if lambda_2 == 0 or ipr == 0:
            continue

        R = math.log2(decisions) / (lambda_2 / ipr)
        metric_values.append(R)
        instances_tested += 1

        if R < 0.05:
            conjecture_holds = False
            counterexample = f"n={n}, decisions={decisions}, lambda_2={lambda_2}, ipr={ipr}"

    return {
        "metric_name": "R(G,ω)",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = seeds[next(i for i, trial in enumerate(trials) if not trial["conjecture_holds"])]
        counterexample = trials[next(i for i, trial in enumerate(trials) if not trial["conjecture_holds"])]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")