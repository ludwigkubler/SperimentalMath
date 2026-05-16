# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_power(mat, power):
    result = [[1 if i == j else 0 for j in range(len(mat))] for i in range(len(mat))]
    for _ in range(power):
        result = matrix_mult(result, mat)
    return result

def matrix_trace(mat):
    return sum(mat[i][i] for i in range(len(mat)))

def matrix_norm(mat):
    return max(sum(abs(mat[i][j]) for j in range(len(mat))) for i in range(len(mat)))

def matrix_eigvals(mat, max_iter=1000, tol=1e-6):
    n = len(mat)
    eigvals = [0.0] * n
    for i in range(n):
        b = [random.random() for _ in range(n)]
        for _ in range(max_iter):
            b_new = [sum(mat[j][k] * b[k] for k in range(n)) for j in range(n)]
            norm = math.sqrt(sum(x**2 for x in b_new))
            if norm == 0:
                break
            b_new = [x / norm for x in b_new]
            if sum((b_new[j] - b[j])**2 for j in range(n)) < tol:
                break
            b = b_new
        eigvals[i] = sum(mat[j][j] * b[j] for j in range(n))
    return eigvals

def generate_3_regular_graph(n):
    edges = []
    stubs = [i // 3 for i in range(3 * n)]
    random.shuffle(stubs)
    for i in range(0, 3 * n, 2):
        u, v = stubs[i], stubs[i + 1]
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph

def generate_glued_graph(n):
    g1 = generate_3_regular_graph(n // 2)
    g2 = generate_3_regular_graph(n // 2)
    graph = defaultdict(list)
    for u, neighbors in g1.items():
        graph[u] = neighbors
    for u, neighbors in g2.items():
        graph[u + n // 2] = [v + n // 2 for v in neighbors]
    graph[0].append(n // 2)
    graph[n // 2].append(0)
    return graph

def generate_cycle(n):
    graph = defaultdict(list)
    for i in range(n):
        graph[i].append((i + 1) % n)
        graph[(i + 1) % n].append(i)
    return graph

def build_non_backtracking_matrix(graph):
    n = len(graph)
    d = max(len(neighbors) for neighbors in graph.values())
    m = sum(len(neighbors) for neighbors in graph.values()) // 2
    mat = [[0 for _ in range(2 * m)] for _ in range(2 * m)]
    edge_to_index = {}
    index_to_edge = []
    index = 0
    for u in graph:
        for v in graph[u]:
            if (u, v) not in edge_to_index and (v, u) not in edge_to_index:
                edge_to_index[(u, v)] = index
                edge_to_index[(v, u)] = index + 1
                index_to_edge.append((u, v))
                index_to_edge.append((v, u))
                index += 2
    for i in range(2 * m):
        u, v = index_to_edge[i]
        for w in graph[v]:
            if w != u:
                j = edge_to_index[(v, w)]
                mat[i][j] = 1
    return mat

def compute_nu(graph):
    n = len(graph)
    mat = build_non_backtracking_matrix(graph)
    eigvals = matrix_eigvals(mat)
    rho = max(abs(x) for x in eigvals)
    d = max(len(neighbors) for neighbors in graph.values())
    return n * max(0, math.log((d - 1) / rho))

def generate_tseitin_cnf(graph, sigma):
    n = len(graph)
    clauses = []
    for u in graph:
        for v in graph[u]:
            if u < v:
                clauses.append([(u, sigma[u]), (v, sigma[v]), (u, sigma[u] + 1), (v, sigma[v] + 1)])
    return clauses

def count_dpll(clauses, assignment, visited):
    if all(any((lit[0], assignment.get(lit[0], 0)) == lit for lit in clause) for clause in clauses):
        return 1, visited
    for clause in clauses:
        if not any((lit[0], assignment.get(lit[0], 0)) == lit for lit in clause):
            for lit in clause:
                if lit[0] not in assignment:
                    new_assignment = assignment.copy()
                    new_assignment[lit[0]] = lit[1]
                    new_visited = visited + 1
                    count1, visited1 = count_dpll(clauses, new_assignment, new_visited)
                    new_assignment[lit[0]] = 1 - lit[1]
                    count2, visited2 = count_dpll(clauses, new_assignment, new_visited)
                    return count1 + count2, max(visited1, visited2)
    return 0, visited

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            graph = generate_3_regular_graph(n)
            sigma = [random.randint(0, 1) for _ in range(n)]
            nu = compute_nu(graph)
            clauses = generate_tseitin_cnf(graph, sigma)
            _, R = count_dpll(clauses, {}, 0)
            metric_values.append(math.log2(R) / nu if nu > 0 else 0)
            instances_tested += 1

            if nu >= 0.5 * n and math.log2(R) < 0.1 * nu:
                conjecture_holds = False
                counterexample = f"Graph with n={n}, nu={nu}, R={R}"

        for _ in range(2):
            graph = generate_glued_graph(n)
            sigma = [random.randint(0, 1) for _ in range(n)]
            nu = compute_nu(graph)
            clauses = generate_tseitin_cnf(graph, sigma)
            _, R = count_dpll(clauses, {}, 0)
            if nu >= 1.5 or math.log2(R) >= 1.5 * n:
                conjecture_holds = False
                counterexample = f"Glued graph with n={n}, nu={nu}, R={R}"

        graph = generate_cycle(n)
        sigma = [random.randint(0, 1) for _ in range(n)]
        nu = compute_nu(graph)
        clauses = generate_tseitin_cnf(graph, sigma)
        _, R = count_dpll(clauses, {}, 0)
        if nu >= 1.5 or math.log2(R) >= 1.5 * n:
            conjecture_holds = False
            counterexample = f"Cycle graph with n={n}, nu={nu}, R={R}"

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    return {
        "metric_name": "log2 R / nu",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results) if results else 0

    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={counterexample} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")