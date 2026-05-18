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

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for 3-regular graph")
    vertices = list(range(n))
    edges = []
    remaining_degrees = {v: 3 for v in vertices}
    while any(d > 0 for d in remaining_degrees.values()):
        u = random.choice([v for v in vertices if remaining_degrees[v] > 0])
        v = random.choice([v for v in vertices if remaining_degrees[v] > 0 and v != u and (u, v) not in edges and (v, u) not in edges])
        edges.append((u, v))
        remaining_degrees[u] -= 1
        remaining_degrees[v] -= 1
    return edges

def generate_planted_bottleneck_graph(n):
    if n < 10:
        raise ValueError("n must be at least 10 for planted bottleneck")
    k = n // 2
    left_vertices = list(range(k))
    right_vertices = list(range(k, n))
    left_edges = generate_3_regular_graph(k)
    right_edges = generate_3_regular_graph(k)
    bridge_edges = [(random.choice(left_vertices), random.choice(right_vertices)) for _ in range(2)]
    edges = left_edges + right_edges + bridge_edges
    return edges

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_subtract(A, B):
    n = len(A)
    m = len(A[0])
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = A[i][j] - B[i][j]
    return result

def matrix_transpose(A):
    n = len(A)
    m = len(A[0])
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            result[j][i] = A[i][j]
    return result

def matrix_trace(A):
    n = len(A)
    trace = 0
    for i in range(n):
        trace += A[i][i]
    return trace

def matrix_determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in A[1:]]
        det += ((-1) ** col) * A[0][col] * matrix_determinant(minor)
    return det

def matrix_inverse(A):
    n = len(A)
    det = matrix_determinant(A)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    adjugate = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in (A[:i] + A[i+1:])]
            adjugate[j][i] = ((-1) ** (i + j)) * matrix_determinant(minor)
    inverse = [[adjugate[i][j] / det for j in range(n)] for i in range(n)]
    return inverse

def matrix_eigen(A):
    n = len(A)
    eigenvalues = []
    eigenvectors = []
    for _ in range(n):
        x = [random.random() for _ in range(n)]
        for _ in range(100):
            Ax = matrix_multiply(A, [x])
            norm = math.sqrt(sum(xi ** 2 for xi in x))
            x = [xi / norm for xi in x]
        eigenvalue = sum(Ax[i] * x[i] for i in range(n))
        eigenvalues.append(eigenvalue)
        eigenvectors.append(x)
    return eigenvalues, eigenvectors

def compute_laplacian(edges, n):
    L = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        L[u][v] = -1
        L[v][u] = -1
        L[u][u] += 1
        L[v][v] += 1
    return L

def compute_fiedler_info(L):
    eigenvalues, eigenvectors = matrix_eigen(L)
    sorted_indices = sorted(range(len(eigenvalues)), key=lambda i: eigenvalues[i])
    lambda_2 = eigenvalues[sorted_indices[1]]
    phi_2 = eigenvectors[sorted_indices[1]]
    IPR = sum(phi_2[i] ** 4 for i in range(len(phi_2)))
    return lambda_2, IPR

def generate_tseitin_formula(edges, omega):
    clauses = []
    for u, v in edges:
        clauses.append([(u, 1), (v, 1), (u, v, 1)])
        clauses.append([(u, 0), (v, 0), (u, v, 0)])
    for v in omega:
        clauses.append([(v, omega[v])])
    return clauses

def tree_dpll(clauses, max_decisions=500000):
    assignments = {}
    decisions = 0
    def unit_propagate():
        nonlocal assignments
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unassigned = [lit for lit in clause if lit[0] not in assignments]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    if len(lit) == 2:
                        var, val = lit
                        if var not in assignments:
                            assignments[var] = val
                            changed = True
                    else:
                        var1, var2, val = lit
                        if var1 in assignments and var2 in assignments:
                            if assignments[var1] == val and assignments[var2] == val:
                                assignments[(var1, var2)] = val
                                changed = True
    def backtrack():
        nonlocal assignments, decisions
        for var in list(assignments.keys()):
            if isinstance(var, tuple):
                del assignments[var]
        for var in list(assignments.keys()):
            if not isinstance(var, tuple):
                del assignments[var]
                break
    unit_propagate()
    while len(assignments) < len(set(lit[0] for clause in clauses for lit in clause if len(lit) == 2)):
        if decisions >= max_decisions:
            return max_decisions
        decisions += 1
        var = random.choice([lit[0] for clause in clauses for lit in clause if len(lit) == 2 and lit[0] not in assignments])
        assignments[var] = random.choice([0, 1])
        unit_propagate()
        satisfied = any(all(lit[0] in assignments and (len(lit) == 2 and assignments[lit[0]] == lit[1] or len(lit) == 3 and assignments[lit[0]] == lit[2]) for lit in clause) for clause in clauses)
        if not satisfied:
            backtrack()
    return decisions

def run_trial(seed):
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    edges = generate_3_regular_graph(n)
    omega = {v: random.choice([0, 1]) for v in range(n)}
    L = compute_laplacian(edges, n)
    lambda_2, IPR = compute_fiedler_info(L)
    if IPR == 0:
        IPR = 1
    clauses = generate_tseitin_formula(edges, omega)
    decisions = tree_dpll(clauses)
    R = math.log2(decisions) / (lambda_2 / IPR) if lambda_2 != 0 and IPR != 0 else 0
    conjecture_holds = R >= 0.05
    counterexample = f"R={R}, decisions={decisions}, λ_2={lambda_2}, IPR={IPR}" if not conjecture_holds else ""
    return {
        "metric_name": "R(G,ω)",
        "metric_value": R,
        "instances_tested": 1,
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
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(trial["conjecture_holds"] for trial in trials) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = seeds[next(i for i, trial in enumerate(trials) if not trial["conjecture_holds"])]
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")