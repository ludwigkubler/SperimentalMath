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
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    remaining_vertices = vertices.copy()
    while remaining_vertices:
        u = remaining_vertices.pop()
        v = random.choice(remaining_vertices)
        edges.append((u, v))
        remaining_vertices.remove(v)
    return edges

def generate_expander_block(n, seed):
    random.seed(seed)
    m = n // 2
    edges = generate_3_regular_graph(m, seed)
    edges.extend(generate_3_regular_graph(m, seed + 1))
    edges.append((m-1, m))
    return edges

def generate_prism_graph(n, seed):
    random.seed(seed)
    edges = []
    for i in range(n):
        edges.append((i, (i+1)%n))
        edges.append((i, (i+2)%n))
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

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scalar_multiply(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_power(A, power):
    result = [[1 if i == j else 0 for j in range(len(A))] for i in range(len(A))]
    for _ in range(power):
        result = matrix_multiply(result, A)
    return result

def matrix_trace(A):
    return sum(A[i][i] for i in range(len(A)))

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
    return matrix_scalar_multiply(adjugate, 1 / det)

def matrix_eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]
    eigenvalues = []
    for _ in range(100):
        x = [random.random() for _ in range(n)]
        for _ in range(100):
            x = matrix_multiply(A, [x])[0]
            norm = math.sqrt(sum(xi ** 2 for xi in x))
            x = [xi / norm for xi in x]
        eigenvalue = matrix_trace(matrix_multiply(A, [x])[0][0] / x[0])
        eigenvalues.append(eigenvalue)
    return sorted(eigenvalues, key=abs, reverse=True)

def compute_phase_gap(edges, n):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    D = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        D[i][i] = len(adj[i])
    A = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        A[u][v] = 1
        A[v][u] = 1
    D_inv = matrix_inverse(D)
    P = matrix_multiply(D_inv, A)
    eigenvalues = matrix_eigenvalues(P)
    lambda_2 = eigenvalues[1]
    delta_Q = 2 * math.asin(math.sqrt(1 - abs(lambda_2)))
    nu = int(n * delta_Q)
    return nu

def generate_odd_charge(n, seed):
    random.seed(seed)
    return [random.choice([-1, 1]) for _ in range(n)]

def tseitin_refutation(edges, charge, max_nodes=2**22):
    n = len(charge)
    clauses = []
    for u, v in edges:
        clauses.append([(u, 1), (v, 1), (n + u, -1)])
        clauses.append([(u, 1), (v, -1), (n + u, 1)])
        clauses.append([(u, -1), (v, 1), (n + u, 1)])
        clauses.append([(u, -1), (v, -1), (n + u, -1)])
    for i in range(n):
        clauses.append([(i, charge[i]), (n + i, charge[i])])
    nodes_explored = 0
    for _ in range(max_nodes):
        nodes_explored += 1
        if not clauses:
            return nodes_explored
        clause = random.choice(clauses)
        if len(clause) == 1:
            literal = clause[0]
            for c in clauses[:]:
                if literal in c:
                    clauses.remove(c)
                elif (-literal[0], -literal[1]) in c:
                    c.remove((-literal[0], -literal[1]))
                    if len(c) == 1:
                        clauses.append(c)
    return nodes_explored

def run_trial(seed):
    n_values = [12, 16, 20]
    regimes = ['A', 'B', 'C']
    results = []
    for n in n_values:
        for regime in regimes:
            if regime == 'A':
                edges = generate_3_regular_graph(n, seed)
            elif regime == 'B':
                edges = generate_expander_block(n, seed)
            elif regime == 'C':
                edges = generate_prism_graph(n, seed)
            charge = generate_odd_charge(n, seed)
            nu = compute_phase_gap(edges, n)
            t_star = tseitin_refutation(edges, charge)
            log2_t_star = math.log2(t_star) if t_star > 0 else 0
            conjecture_holds = (log2_t_star >= nu / 8 - 5) and ((regime == 'A') or (nu <= 16))
            counterexample = ""
            if not conjecture_holds:
                counterexample = f"n={n}, regime={regime}, nu={nu}, t*={t_star}"
            results.append({
                "n": n,
                "regime": regime,
                "nu": nu,
                "t_star": t_star,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    metric_values = [r["nu"] for r in results]
    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    instances_tested = len(results)
    all_hold = all(r["conjecture_holds"] for r in results)
    counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
    return {
        "metric_name": "nu",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": all_hold,
        "counterexample": counterexamples[0] if counterexamples else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trial["seed"] = seed
        print(f"TRIAL: {trial}")
        trials.append(trial)
    metric_values = [t["metric_value"] for t in trials]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = (sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials) if trials else 0
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((t["seed"] for t in trials if not t["conjecture_holds"]), None)
        counterexample = next((t["counterexample"] for t in trials if not t["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")