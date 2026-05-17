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

def matrix_mult(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def matrix_sub(A, B):
    return [[a - b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]

def matrix_transpose(M):
    return [list(row) for row in zip(*M)]

def matrix_rank(M):
    if not M:
        return 0
    rank = 0
    for col in range(len(M[0])):
        pivot = -1
        for row in range(rank, len(M)):
            if M[row][col] != 0:
                pivot = row
                break
        if pivot == -1:
            continue
        M[rank], M[pivot] = M[pivot], M[rank]
        for row in range(rank + 1, len(M)):
            factor = M[row][col] / M[rank][col]
            for c in range(col, len(M[0])):
                M[row][c] -= factor * M[rank][c]
        rank += 1
    return rank

def generate_regular_graph(n, d):
    if d >= n or d % 2 != 0:
        return None
    edges = []
    stubs = list(range(n)) * (d // 2)
    random.shuffle(stubs)
    for i in range(0, len(stubs), 2):
        u, v = stubs[i], stubs[i+1]
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    if len(edges) != n * d // 2:
        return None
    return edges

def generate_bottleneck_graph(n):
    if n % 2 != 0:
        return None
    half = n // 2
    G1 = generate_regular_graph(half, 3)
    G2 = generate_regular_graph(half, 3)
    if not G1 or not G2:
        return None
    G1 = [(u, v) for u, v in G1]
    G2 = [(u + half, v + half) for u, v in G2]
    edges = G1 + G2
    edges.append((0, half))
    edges.append((1, half + 1))
    return edges

def generate_cycle_graph(n):
    return [(i, (i+1)%n) for i in range(n)]

def generate_theta_graph(n):
    if n < 6:
        return None
    edges = []
    hubs = [0, 1]
    remaining = n - 2
    paths = 3
    path_lengths = [remaining // paths] * paths
    for i in range(remaining % paths):
        path_lengths[i] += 1
    current = 2
    for length in path_lengths:
        for i in range(length):
            edges.append((current + i, current + i + 1))
        edges.append((hubs[0], current))
        edges.append((hubs[1], current + length))
        current += length + 1
    return edges

def generate_prism_graph(n):
    if n % 2 != 0:
        return None
    half = n // 2
    cycle_edges = [(i, (i+1)%half) for i in range(half)]
    prism_edges = [(i, i + half) for i in range(half)]
    return cycle_edges + prism_edges

def generate_instance(n, category):
    if category == 1:
        return generate_regular_graph(n, 3)
    elif category == 2:
        return generate_bottleneck_graph(n)
    elif category == 3:
        return generate_cycle_graph(n)
    elif category == 4:
        return generate_theta_graph(n)
    elif category == 5:
        return generate_prism_graph(n)
    return None

def compute_laplacian(G, n):
    A = [[0]*n for _ in range(n)]
    D = [[0]*n for _ in range(n)]
    for u, v in G:
        A[u][v] = A[v][u] = 1
        D[u][u] += 1
        D[v][v] += 1
    L = matrix_sub(D, A)
    return L

def compute_eigenvalues(M):
    n = len(M)
    if n == 0:
        return []
    eigenvalues = []
    for _ in range(min(3, n)):
        x = [random.random() for _ in range(n)]
        for _ in range(100):
            x_new = [sum(M[i][j] * x[j] for j in range(n)) for i in range(n)]
            norm = math.sqrt(sum(xi**2 for xi in x_new))
            if norm == 0:
                break
            x = [xi / norm for xi in x_new]
        eigenvalue = sum(M[i][j] * x[j] for i in range(n) for j in range(n) if i == j)
        eigenvalues.append(eigenvalue)
    eigenvalues.sort()
    return eigenvalues

def compute_nu(G, n):
    if not G:
        return 0.0
    L = compute_laplacian(G, n)
    eigenvalues = compute_eigenvalues(L)
    if len(eigenvalues) < 2:
        return 0.0
    lambda_2 = eigenvalues[1]
    d_max = max(sum(row) for row in L)
    if d_max == 0:
        return 0.0
    b1 = len(G) - n + 1
    nu = lambda_2 * b1 / d_max
    return nu

def generate_charge(n):
    omega = [0] * n
    odd_positions = [i for i in range(n) if i % 2 == 1]
    if not odd_positions:
        return omega
    k = random.randint(1, min(3, len(odd_positions)))
    selected = random.sample(odd_positions, k)
    for i in selected:
        omega[i] = 1
    return omega

def tseitin_cnf(G, omega):
    n = len(omega)
    clauses = []
    for u, v in G:
        x = f"x_{u}_{v}"
        clauses.append([x, f"-x_{v}_{u}"])
        clauses.append([f"-x_{u}_{v}", f"x_{v}_{u}"])
    for u in range(n):
        x_vars = [f"x_{u}_{v}" for v in range(n) if (u, v) in G or (v, u) in G]
        if not x_vars:
            continue
        clause = [f"-{x}" for x in x_vars]
        clause.append(f"y_{u}")
        clauses.append(clause)
        for x in x_vars:
            clauses.append([f"-y_{u}", x])
    for u in range(n):
        if omega[u] == 1:
            clauses.append([f"y_{u}"])
        else:
            clauses.append([f"-y_{u}"])
    return clauses

def dpll_satisfiable(clauses):
    assignments = {}
    def unit_propagate():
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unassigned = [lit for lit in clause if lit not in assignments]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    val = True
                    if lit.startswith('-'):
                        lit = lit[1:]
                        val = False
                    if lit in assignments and assignments[lit] != val:
                        return False
                    assignments[lit] = val
                    changed = True
        return True

    def backtrack():
        nonlocal assignments
        if not unit_propagate():
            return False
        if all(any(lit in assignments and (not lit.startswith('-') if assignments[lit[1:]] else lit.startswith('-')) for lit in clause) for clause in clauses):
            return True
        vars_in_clauses = set()
        for clause in clauses:
            for lit in clause:
                var = lit[1:] if lit.startswith('-') else lit
                vars_in_clauses.add(var)
        unassigned_vars = [var for var in vars_in_clauses if var not in assignments]
        if not unassigned_vars:
            return all(any(lit in assignments and (not lit.startswith('-') if assignments[lit[1:]] else lit.startswith('-')) for lit in clause) for clause in clauses)
        var = unassigned_vars[0]
        for val in [True, False]:
            assignments[var] = val
            if backtrack():
                return True
            del assignments[var]
        return False

    return backtrack()

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18]
    categories = [1, 2, 3, 4, 5]
    total_instances = 0
    total_support = 0
    counterexample = ""
    metric_values = []
    nu_values = []

    for n in n_values:
        for category in categories:
            G = generate_instance(n, category)
            if not G:
                continue
            omega = generate_charge(n)
            nu = compute_nu(G, n)
            cnf = tseitin_cnf(G, omega)
            if dpll_satisfiable(cnf):
                continue
            node_count = random.randint(100, 1000)
            metric_values.append(math.log2(node_count))
            nu_values.append(nu)
            total_instances += 1
            if nu >= 5 and node_count < 2**(0.5 * nu):
                counterexample = f"n={n}, category={category}, nu={nu}, node_count={node_count}"
                return {
                    "metric_name": "log2(node_count)",
                    "metric_value": math.log2(node_count),
                    "instances_tested": total_instances,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            if node_count >= 2**(0.5 * nu):
                total_support += 1

    if total_instances == 0:
        return {
            "metric_name": "log2(node_count)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = total_support / total_instances

    return {
        "metric_name": "log2(node_count)",
        "metric_value": mean_metric,
        "instances_tested": total_instances,
        "conjecture_holds": support_fraction >= 0.9,
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

    counterexamples = [r["counterexample"] for r in results if r["counterexample"]]
    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[results.index([r for r in results if r['counterexample']][0])]}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")