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
        raise ValueError("n must be even for a 3-regular graph")
    vertices = list(range(n))
    edges = []
    while len(edges) < 3 * n // 2:
        u, v = random.sample(vertices, 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    return edges

def generate_planted_bottleneck_graph(n):
    if n < 10:
        raise ValueError("n must be at least 10 for planted bottleneck")
    half = n // 2
    left = generate_3_regular_graph(half)
    right = generate_3_regular_graph(half)
    offset = half
    edges = left + [(u + offset, v + offset) for u, v in right]
    bridges = random.sample(list(itertools.product(range(half), range(half, n))), 2)
    edges.extend(bridges)
    return edges

def generate_odd_charge(n):
    return [random.randint(0, 1) for _ in range(n)]

def build_tseitin_cnf(edges, charge):
    n = len(charge)
    clauses = []
    for u, v in edges:
        clauses.append([u, v, n + len(clauses)])
        clauses.append([-u, -v, n + len(clauses)])
    for v in range(n):
        clauses.append([v] if charge[v] == 1 else [-v])
    return clauses

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
            result[i][j] = A[i][k] - B[i][j]
    return result

def matrix_transpose(A):
    n = len(A)
    m = len(A[0])
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            result[j][i] = A[i][j]
    return result

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

def combinatorial_laplacian(edges, n):
    L = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        L[u][u] += 1
        L[v][v] += 1
        L[u][v] = -1
        L[v][u] = -1
    return L

def eigen_decomposition(L):
    n = len(L)
    eigenvalues = []
    eigenvectors = []
    for i in range(n):
        eigenvalues.append(L[i][i])
        eigenvectors.append([1 if j == i else 0 for j in range(n)])
    return eigenvalues, eigenvectors

def fiedler_ipr(eigenvector):
    ipr = sum(x ** 4 for x in eigenvector)
    return ipr

def tree_dpll(clauses, max_decisions=500000):
    n = max(max(abs(lit) for clause in clauses for lit in clause), 1)
    assignment = [None] * n
    decisions = 0
    def unit_propagate():
        nonlocal assignment
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unassigned = [lit for lit in clause if assignment[abs(lit) - 1] is None]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    if assignment[abs(lit) - 1] is None:
                        assignment[abs(lit) - 1] = lit > 0
                        changed = True
    def dpll():
        nonlocal decisions
        unit_propagate()
        if all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in clauses):
            return True
        if any(all(assignment[abs(lit) - 1] is not None and assignment[abs(lit) - 1] != (lit > 0) for lit in clause) for clause in clauses):
            return False
        for var in range(n):
            if assignment[var] is None:
                for value in [True, False]:
                    assignment[var] = value
                    decisions += 1
                    if dpll():
                        return True
                    assignment[var] = None
                return False
        return False
    dpll()
    return decisions

def run_trial(seed):
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    is_planted = random.random() < 0.2
    if is_planted:
        edges = generate_planted_bottleneck_graph(n)
    else:
        edges = generate_3_regular_graph(n)
    charge = generate_odd_charge(n)
    clauses = build_tseitin_cnf(edges, charge)
    decisions = tree_dpll(clauses)
    L = combinatorial_laplacian(edges, n)
    eigenvalues, eigenvectors = eigen_decomposition(L)
    lambda_2 = sorted(eigenvalues)[1]
    phi_2 = eigenvectors[eigenvalues.index(lambda_2)]
    ipr = fiedler_ipr(phi_2)
    if ipr == 0:
        return {
            "metric_name": "R(G,ω)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    R = math.log2(decisions + 1) / (lambda_2 / ipr)
    conjecture_holds = R >= 0.05
    counterexample = "" if conjecture_holds else f"R={R}, decisions={decisions}, λ_2={lambda_2}, IPR={ipr}"
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
    else:
        for trial in trials:
            if not trial["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={trial['counterexample']} first_failing_seed={seeds[trials.index(trial)]}")
                break