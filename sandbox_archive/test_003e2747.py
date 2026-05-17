# auto-injected by SEC sandbox
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
import json
from collections import defaultdict

def matrix_mult(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def matrix_sub(A, B):
    return [[a - b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_rank(A):
    rank = 0
    rows, cols = len(A), len(A[0])
    for r in range(rows):
        if rank >= cols:
            break
        pivot = r
        while pivot < rows and A[pivot][rank] == 0:
            pivot += 1
        if pivot == rows:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        for c in range(r + 1, rows):
            factor = A[c][rank] / A[r][rank]
            for k in range(rank, cols):
                A[c][k] -= factor * A[r][k]
        rank += 1
    return rank

def generate_3_regular_graph(n):
    if n % 2 != 0:
        return None
    edges = []
    stubs = [2] * n
    while sum(stubs) > 0:
        u = random.choice([i for i, s in enumerate(stubs) if s > 0])
        v = random.choice([i for i, s in enumerate(stubs) if s > 0 and i != u and (u, i) not in edges and (i, u) not in edges])
        edges.append((u, v))
        stubs[u] -= 1
        stubs[v] -= 1
    return edges

def generate_two_block_bottleneck(n):
    if n % 2 != 0:
        return None
    half = n // 2
    left_edges = generate_3_regular_graph(half)
    right_edges = [(u + half, v + half) for u, v in generate_3_regular_graph(half)]
    bottleneck_edges = [(0, half), (1, half + 1)]
    return left_edges + right_edges + bottleneck_edges

def generate_cycle(n):
    return [(i, (i + 1) % n) for i in range(n)]

def generate_theta_graph(n):
    if n < 6:
        return None
    hubs = [0, 1]
    paths = []
    remaining = n - 2
    for _ in range(3):
        path_length = random.randint(1, remaining - 2)
        paths.append((path_length, random.randint(0, 1)))
        remaining -= path_length
    edges = []
    current = 2
    for length, hub in paths:
        for i in range(length):
            edges.append((current + i, current + i + 1))
        edges.append((current, hubs[hub]))
        current += length
    return edges

def generate_prism_graph(n):
    if n % 2 != 0:
        return None
    half = n // 2
    cycle_edges = [(i, (i + 1) % half) for i in range(half)]
    prism_edges = [(i, i + half) for i in range(half)]
    return cycle_edges + prism_edges

def generate_graph(n, category):
    if category == 1:
        return generate_3_regular_graph(n)
    elif category == 2:
        return generate_two_block_bottleneck(n)
    elif category == 3:
        return generate_cycle(n)
    elif category == 4:
        return generate_theta_graph(n)
    elif category == 5:
        return generate_prism_graph(n)
    else:
        return None

def compute_laplacian(edges, n):
    D = [[0] * n for _ in range(n)]
    A = [[0] * n for _ in range(n)]
    for u, v in edges:
        D[u][u] += 1
        D[v][v] += 1
        A[u][v] = A[v][u] = 1
    L = matrix_sub(D, A)
    return L

def compute_eigenvalues(L):
    n = len(L)
    eigenvalues = []
    for _ in range(n):
        x = [random.random() for _ in range(n)]
        for _ in range(100):
            y = matrix_mult(L, [x])[0]
            norm = math.sqrt(sum(y_i ** 2 for y_i in y))
            if norm == 0:
                break
            x = [y_i / norm for y_i in y]
        eigenvalues.append(sum(L[i][j] * x[i] * x[j] for i in range(n) for j in range(n)))
    return sorted(eigenvalues)

def compute_nu(G, n, d_max):
    L = compute_laplacian(G, n)
    eigenvalues = compute_eigenvalues(L)
    lambda_2 = eigenvalues[1]
    b_1 = len(G) - n + 1
    nu = (lambda_2 * b_1) / d_max
    return nu

def generate_charge(n):
    omega = [0] * n
    odd_indices = [i for i in range(n) if i % 2 == 1]
    for i in random.sample(odd_indices, len(odd_indices) // 2):
        omega[i] = 1
    return omega

def tseitin_cnf(G, omega, n):
    clauses = []
    for u, v in G:
        clauses.append([u, v, n])
        clauses.append([-u, -v, n])
        clauses.append([-u, n])
        clauses.append([-v, n])
        n += 1
    for i in range(len(omega)):
        if omega[i] == 1:
            clauses.append([i])
        else:
            clauses.append([-i])
    return clauses, n

def dpll(clauses, assignment, n):
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        literal = unit_clauses.pop()[0]
        if -literal in assignment:
            return None
        assignment[literal] = True
        new_clauses = []
        for c in clauses:
            if literal in c:
                continue
            new_c = [l for l in c if l != -literal]
            if not new_c:
                return None
            if len(new_c) == 1 and new_c not in unit_clauses:
                unit_clauses.append(new_c)
            new_clauses.append(new_c)
        clauses = new_clauses
        unit_clauses = [c for c in clauses if len(c) == 1]
    if not clauses:
        return assignment
    literal = next(iter(clauses[0]))
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[literal] = value
        result = dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment, n)
        if result is not None:
            return result
    return None

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18]
    categories = [1, 2, 3, 4, 5]
    metric_values = []
    conjecture_holds_list = []
    counterexamples = []
    instances_tested = 0

    for n in n_values:
        for category in categories:
            G = generate_graph(n, category)
            if G is None:
                continue
            omega = generate_charge(n)
            d_max = max(sum(1 for u, v in G if u == i or v == i) for i in range(n))
            nu = compute_nu(G, n, d_max)
            clauses, num_vars = tseitin_cnf(G, omega, n)
            assignment = dpll(clauses, {}, num_vars)
            N = len(assignment) if assignment is not None else 0
            metric_values.append(math.log2(N) if N > 0 else 0)
            conjecture_holds = N >= 2 ** (0.5 * nu) if nu >= 5 else True
            conjecture_holds_list.append(conjecture_holds)
            if not conjecture_holds and nu >= 5:
                counterexamples.append(f"n={n}, category={category}, nu={nu}, N={N}")
            instances_tested += 1

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    support_fraction = sum(conjecture_holds_list) / len(conjecture_holds_list) if conjecture_holds_list else 0
    counterexample = counterexamples[0] if counterexamples else ""

    return {
        "metric_name": "log2(N)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": all(conjecture_holds_list),
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results) if results else 0

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_counterexample = next(r for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample['counterexample']}\" first_failing_seed={first_counterexample['seed']}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")