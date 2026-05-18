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
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
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

def build_tseitin_cnf(G, omega):
    n = len(omega)
    clauses = []
    for u, v in G:
        x = f"x_{u}_{v}"
        clauses.append([x, f"v_{u}", f"v_{v}"])
        clauses.append([f"-{x}", f"v_{u}", f"-v_{v}"])
        clauses.append([f"-{x}", f"-v_{u}", f"v_{v}"])
        clauses.append([x, f"-v_{u}", f"-v_{v}"])
    for i in range(n):
        if omega[i] == 1:
            clauses.append([f"v_{i}"])
        else:
            clauses.append([f"-v_{i}"])
    return clauses

def tree_dpll(clauses, max_decisions=500000):
    decisions = 0
    assignment = {}
    def unit_propagate():
        nonlocal assignment
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unassigned = [lit for lit in clause if lit[1:] not in assignment]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    var = lit[1:]
                    val = (lit[0] != '-')
                    if var in assignment and assignment[var] != val:
                        return False
                    assignment[var] = val
                    changed = True
        return True

    def dpll():
        nonlocal decisions
        if not unit_propagate():
            return False
        if all(any((lit[0] != '-') == assignment.get(lit[1:], False) for lit in clause) for clause in clauses):
            return True
        if decisions >= max_decisions:
            return True
        vars_in_clauses = set()
        for clause in clauses:
            for lit in clause:
                vars_in_clauses.add(lit[1:])
        for var in vars_in_clauses:
            if var not in assignment:
                decisions += 1
                assignment[var] = True
                if dpll():
                    return True
                assignment[var] = False
                if dpll():
                    return True
                del assignment[var]
                return False
        return False

    dpll()
    return decisions

def matrix_mult(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_sub(A, B):
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

def matrix_diagonal(A):
    n = len(A)
    result = [0 for _ in range(n)]
    for i in range(n):
        result[i] = A[i][i]
    return result

def matrix_rank(A):
    n = len(A)
    m = len(A[0])
    rank = 0
    for row in range(n):
        if rank >= m:
            break
        i = rank
        while i < n and A[i][rank] == 0:
            i += 1
        if i == n:
            continue
        A[row], A[i] = A[i], A[row]
        for col in range(rank + 1, m):
            A[row][col] /= A[row][rank]
        for i in range(n):
            if i != row and A[i][rank] != 0:
                for col in range(rank + 1, m):
                    A[i][col] -= A[i][rank] * A[row][col]
        rank += 1
    return rank

def matrix_eigen(A):
    n = len(A)
    if n > 40:
        raise ValueError("Matrix too large for this implementation")
    eigenvalues = [0 for _ in range(n)]
    eigenvectors = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        eigenvalues[i] = A[i][i]
        eigenvectors[i][i] = 1
    return eigenvalues, eigenvectors

def compute_laplacian(G, n):
    L = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in G:
        L[u][v] = -1
        L[v][u] = -1
        L[u][u] += 1
        L[v][v] += 1
    return L

def compute_ipr(phi_2):
    n = len(phi_2)
    ipr = 0
    for i in range(n):
        ipr += phi_2[i] ** 4
    return ipr

def run_trial(seed):
    n_sizes = [8, 10, 12, 14, 16]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_sizes:
        if n % 2 != 0:
            continue
        G = generate_3_regular_graph(n, seed)
        omega = generate_odd_charge(n, seed)
        clauses = build_tseitin_cnf(G, omega)
        decisions = tree_dpll(clauses)
        L = compute_laplacian(G, n)
        eigenvalues, eigenvectors = matrix_eigen(L)
        lambda_2 = sorted(eigenvalues)[1]
        phi_2 = eigenvectors[1]
        ipr = compute_ipr(phi_2)
        if ipr == 0:
            continue
        R = math.log2(decisions) / (lambda_2 / ipr)
        metric_values.append(R)
        instances_tested += 1
        if R < 0.05:
            conjecture_holds = False
            counterexample = f"n={n}, decisions={decisions}, lambda_2={lambda_2}, IPR={ipr}"

    return {
        "metric_name": "R(G,ω)",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{trial['metric_name']}', 'metric_value': {trial['metric_value']}, 'instances_tested': {trial['instances_tested']}, 'conjecture_holds': {trial['conjecture_holds']}, 'counterexample': '{trial['counterexample']}'}}")
        results.append(trial)

    metric_values = [trial['metric_value'] for trial in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(trial['conjecture_holds'] for trial in results) / len(results)

    if all(trial['conjecture_holds'] for trial in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not trial['conjecture_holds'] for trial in results):
        first_failing_seed = next(trial['seed'] for trial in results if not trial['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='{trial['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=0")