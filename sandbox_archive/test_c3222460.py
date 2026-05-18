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

    stubs = list(range(n)) * 3
    edges = set()
    vertices = set(range(n))

    while stubs:
        u = stubs.pop()
        if not stubs:
            break
        v = random.choice([s for s in stubs if s != u])
        stubs.remove(v)
        edges.add(frozenset({u, v}))

    if len(edges) != 3 * n // 2:
        return generate_3_regular_graph(n)

    return vertices, edges

def generate_odd_charge(n, vertices):
    charge = {v: random.randint(0, 1) for v in vertices}
    if sum(charge.values()) % 2 == 0:
        v = random.choice(list(vertices))
        charge[v] = 1 - charge[v]
    return charge

def build_bfs_gauge(vertices, edges, charge, root):
    psi = {e: 0 for e in edges}
    visited = {root}
    queue = [root]

    while queue:
        u = queue.pop(0)
        for v in vertices:
            e = frozenset({u, v})
            if e in edges and v not in visited:
                psi[e] = (charge[v] + sum(psi[frozenset({u, w})] for w in vertices if frozenset({u, w}) in edges and w != v)) % 2
                visited.add(v)
                queue.append(v)

    return psi

def matrix_multiply(A, B):
    n = len(A)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_subtract(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def matrix_transpose(A):
    n = len(A)
    return [[A[j][i] for j in range(n)] for i in range(n)]

def matrix_power_iteration(A, max_iter=100, tol=1e-6):
    n = len(A)
    b = [random.random() for _ in range(n)]
    for _ in range(max_iter):
        b_new = matrix_multiply(A, [b])[0]
        norm = math.sqrt(sum(x**2 for x in b_new))
        b_new = [x / norm for x in b_new]
        if sum((b_new[i] - b[i])**2 for i in range(n)) < tol:
            break
        b = b_new
    return sum(b[i] * matrix_multiply(A, [b])[0][i] for i in range(n))

def compute_signed_laplacian(vertices, edges, psi):
    n = len(vertices)
    D = [[0.0 for _ in range(n)] for _ in range(n)]
    A = [[0.0 for _ in range(n)] for _ in range(n)]

    for v in vertices:
        D[v][v] = sum(1 for e in edges if v in e)

    for e in edges:
        u, v = e
        sigma = (-1) ** psi[e]
        A[u][v] = sigma
        A[v][u] = sigma

    L = matrix_subtract(D, A)
    return L

def compute_mu(L):
    n = len(L)
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    alpha = 1.0
    L_alpha = [[alpha * I[i][j] - L[i][j] for j in range(n)] for i in range(n)]
    mu = matrix_power_iteration(L_alpha)
    return mu

def count_dpll(clauses, assignment, depth=0, max_depth=30):
    if depth > max_depth:
        return float('inf')

    if not clauses:
        return 1

    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        lit = next(iter(unit_clauses[0]))
        new_assignment = assignment.copy()
        new_assignment[lit] = True
        new_clauses = [c for c in clauses if lit not in c]
        return count_dpll(new_clauses, new_assignment, depth + 1, max_depth)

    pure_literals = set()
    for c in clauses:
        for lit in c:
            if all(lit not in other_c for other_c in clauses if other_c != c):
                pure_literals.add(lit)

    if pure_literals:
        lit = pure_literals.pop()
        new_assignment = assignment.copy()
        new_assignment[lit] = True
        new_clauses = [c for c in clauses if lit not in c]
        return count_dpll(new_clauses, new_assignment, depth + 1, max_depth)

    lit = next(iter(next(iter(clauses))))
    count = 0
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[lit] = val
        new_clauses = [c for c in clauses if lit not in c or (val and -lit in c) or (not val and lit in c)]
        count += count_dpll(new_clauses, new_assignment, depth + 1, max_depth)

    return count

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        vertices, edges = generate_3_regular_graph(n)
        charge = generate_odd_charge(n, vertices)
        root = random.choice(list(vertices))
        psi = build_bfs_gauge(vertices, edges, charge, root)
        L = compute_signed_laplacian(vertices, edges, psi)
        mu = compute_mu(L)

        clauses = []
        for e in edges:
            u, v = e
            clauses.append({u, -v})
            clauses.append({-u, v})

        for v in vertices:
            if charge[v] == 1:
                clauses.append({v})

        t_star = count_dpll(clauses, {})

        if t_star == float('inf'):
            continue

        metric_value = math.log2(t_star) / (mu * n)
        metric_values.append(metric_value)
        instances_tested += 1

        if metric_value < 0.05:
            conjecture_holds = False
            counterexample = f"n={n}, mu={mu}, t_star={t_star}, metric_value={metric_value}"

    if not metric_values:
        return {
            "metric_name": "log2(t_star)/(mu*n)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    avg_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2(t_star)/(mu*n)",
        "metric_value": avg_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    total_metric = 0.0
    total_squared = 0.0
    support_count = 0
    total_instances = 0
    counterexample_found = False
    first_failing_seed = None

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

        total_metric += result["metric_value"]
        total_squared += result["metric_value"] ** 2
        total_instances += result["instances_tested"]

        if result["conjecture_holds"]:
            support_count += 1
        elif not counterexample_found:
            counterexample_found = True
            first_failing_seed = seed

    if total_instances == 0:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = total_metric / len(seeds)
    std = math.sqrt((total_squared / len(seeds)) - (mean ** 2))
    support_fraction = support_count / len(seeds)

    if counterexample_found:
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")