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
    n = len(A)
    m = len(B[0])
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_norm(A):
    return max(sum(abs(x) for x in row) for row in A)

def power_iteration(A, max_iter=100, tol=1e-6):
    n = len(A)
    b = [random.random() for _ in range(n)]
    b_norm = math.sqrt(sum(x**2 for x in b))
    b = [x / b_norm for x in b]

    for _ in range(max_iter):
        b_new = [0.0] * n
        for i in range(n):
            for j in range(n):
                b_new[i] += A[i][j] * b[j]

        b_new_norm = math.sqrt(sum(x**2 for x in b_new))
        b_new = [x / b_new_norm for x in b_new]

        if sum((b_new[i] - b[i])**2 for i in range(n)) < tol:
            break

        b = b_new

    eigenvalue = sum(b[i] * sum(A[i][j] * b[j] for j in range(n)) for i in range(n))
    return eigenvalue

def is_connected(graph):
    n = len(graph)
    visited = [False] * n
    stack = [0]
    visited[0] = True

    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)

    return all(visited)

def generate_regular_graph(n, d):
    if d >= n:
        raise ValueError("Degree must be less than number of vertices")

    while True:
        graph = defaultdict(list)
        edges = []

        for i in range(n):
            for j in range(i + 1, n):
                edges.append((i, j))

        random.shuffle(edges)

        for i in range(n):
            graph[i] = []

        for i in range(n):
            for j in range(d // 2):
                u, v = edges.pop()
                graph[u].append(v)
                graph[v].append(u)

        if is_connected(graph):
            return graph

def generate_glued_graph(n):
    g1 = generate_regular_graph(n // 2, 3)
    g2 = generate_regular_graph(n // 2, 3)

    graph = defaultdict(list)
    for i in range(n // 2):
        graph[i] = g1[i]
    for i in range(n // 2, n):
        graph[i] = [x + n // 2 for x in g2[i - n // 2]]

    graph[0].append(n // 2)
    graph[n // 2].append(0)

    return graph

def generate_cycle(n):
    graph = defaultdict(list)
    for i in range(n):
        graph[i].append((i + 1) % n)
        graph[i].append((i - 1) % n)
    return graph

def build_non_backtracking_matrix(graph):
    n = len(graph)
    d = len(graph[0])
    m = n * d

    B = [[0 for _ in range(m)] for _ in range(m)]

    for v in range(n):
        for i in range(d):
            u = graph[v][i]
            for j in range(d):
                if graph[u][j] != v:
                    B[v * d + i][u * d + j] = 1

    return B

def compute_nu(graph, B):
    n = len(graph)
    d = len(graph[0])
    rho = power_iteration(B)
    nu = n * max(0, math.log((d - 1) / rho))
    return nu

def generate_tseitin_cnf(graph, sigma):
    n = len(graph)
    d = len(graph[0])
    cnf = []

    for v in range(n):
        for i in range(d):
            u = graph[v][i]
            if u > v:
                cnf.append([(v, i), (u, i), (v, (i + 1) % d), (u, (i + 1) % d)])

    for v in range(n):
        for i in range(d):
            cnf.append([(v, i), (v, (i + 1) % d)])

    return cnf

def count_dpll(cnf):
    n = len(cnf)
    visited = set()

    def dfs(assignment):
        if len(assignment) == n:
            return 1

        for clause in cnf:
            satisfied = False
            for lit in clause:
                if lit in assignment:
                    satisfied = True
                    break
            if not satisfied:
                return 0

        count = 0
        for lit in cnf[len(assignment)]:
            if lit not in assignment:
                new_assignment = assignment + (lit,)
                if new_assignment not in visited:
                    visited.add(new_assignment)
                    count += dfs(new_assignment)
        return count

    return dfs(tuple())

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            graph = generate_regular_graph(n, 3)
            B = build_non_backtracking_matrix(graph)
            nu = compute_nu(graph, B)
            sigma = random.randint(1, n)
            cnf = generate_tseitin_cnf(graph, sigma)
            R = count_dpll(cnf)
            log2_R = math.log2(R) if R > 0 else 0
            metric_values.append(log2_R)
            instances_tested += 1

            if log2_R < 0.1 * nu and nu >= 0.5 * n:
                conjecture_holds = False
                counterexample = f"Found counterexample with n={n}, nu={nu}, log2_R={log2_R}"

        for _ in range(2):
            graph = generate_glued_graph(n)
            B = build_non_backtracking_matrix(graph)
            nu = compute_nu(graph, B)
            sigma = random.randint(1, n)
            cnf = generate_tseitin_cnf(graph, sigma)
            R = count_dpll(cnf)
            log2_R = math.log2(R) if R > 0 else 0
            metric_values.append(log2_R)
            instances_tested += 1

            if nu >= 1.5 or log2_R >= 1.5 * n:
                conjecture_holds = False
                counterexample = f"Found counterexample with n={n}, nu={nu}, log2_R={log2_R}"

        for _ in range(1):
            graph = generate_cycle(n)
            B = build_non_backtracking_matrix(graph)
            nu = compute_nu(graph, B)
            sigma = random.randint(1, n)
            cnf = generate_tseitin_cnf(graph, sigma)
            R = count_dpll(cnf)
            log2_R = math.log2(R) if R > 0 else 0
            metric_values.append(log2_R)
            instances_tested += 1

            if nu >= 1.5 or log2_R >= 1.5 * n:
                conjecture_holds = False
                counterexample = f"Found counterexample with n={n}, nu={nu}, log2_R={log2_R}"

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))

    return {
        "metric_name": "log2_R",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
        "std_metric": std_metric
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")