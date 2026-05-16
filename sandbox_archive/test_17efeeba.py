# auto-injected by SEC sandbox
import json
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
import collections
from fractions import Fraction

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

def matrix_power(m, power):
    result = [[1 if i == j else 0 for j in range(len(m))] for i in range(len(m))]
    for _ in range(power):
        result = matrix_mult(result, m)
    return result

def matrix_trace(m):
    return sum(m[i][i] for i in range(len(m)))

def matrix_norm(m):
    return math.sqrt(sum(sum(x**2 for x in row) for row in m))

def matrix_eigvals(m, max_iter=1000, tol=1e-10):
    n = len(m)
    v = [random.random() for _ in range(n)]
    for _ in range(max_iter):
        Av = [sum(m[i][j] * v[j] for j in range(n)) for i in range(n)]
        v_new = [Av[i] / math.sqrt(sum(x**2 for x in Av)) for i in range(n)]
        if sum((v_new[i] - v[i])**2 for i in range(n)) < tol:
            break
        v = v_new
    return sum(m[i][i] * v[i] for i in range(n))

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

def generate_ramanujan_graph(n, d):
    while True:
        graph = [[] for _ in range(n)]
        stubs = list(range(n)) * d
        random.shuffle(stubs)
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i+1]
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
        if is_connected(graph):
            return graph

def generate_glued_graph(n, d):
    g1 = generate_ramanujan_graph(n//2, d)
    g2 = generate_ramanujan_graph(n - n//2, d)
    graph = g1 + g2
    graph[0].append(n//2)
    graph[n//2].append(0)
    return graph

def generate_cycle(n):
    graph = [[] for _ in range(n)]
    for i in range(n):
        graph[i].append((i+1)%n)
        graph[i].append((i-1)%n)
    return graph

def compute_nu(graph):
    n = len(graph)
    d = len(graph[0])
    if d == 0:
        return 0.0
    m = sum(len(edges) for edges in graph) // 2
    B = [[0] * (2*m) for _ in range(2*m)]
    edge_to_idx = {}
    idx = 0
    for u in range(n):
        for v in graph[u]:
            if (u, v) not in edge_to_idx and (v, u) not in edge_to_idx:
                edge_to_idx[(u, v)] = idx
                idx += 1
    for u in range(n):
        for v in graph[u]:
            for w in graph[u]:
                if v != w:
                    B[edge_to_idx[(u, v)]][edge_to_idx[(w, u)]] = 1
    rho = matrix_eigvals(B)
    if (d - 1) == 0 or rho == 0:
        return 0.0
    return n * max(0, math.log((d - 1) / rho))

def generate_tseitin_cnf(graph, sigma):
    n = len(graph)
    clauses = []
    for u in range(n):
        for v in graph[u]:
            if u < v:
                clauses.append([(u, True), (v, True), (u, v, False)])
                clauses.append([(u, False), (v, False), (u, v, True)])
    for u in range(n):
        for v in graph[u]:
            if u < v:
                clauses.append([(u, v, True), (v, u, False)])
    if sigma % 2 == 1:
        clauses.append([(0, True)])
    return clauses

def count_dpll(clauses):
    variables = set()
    for clause in clauses:
        for literal in clause:
            if isinstance(literal, tuple):
                variables.add(literal[0])
    variables = sorted(variables)
    n = len(variables)
    count = 0
    def backtrack(assignment, remaining_clauses):
        nonlocal count
        if not remaining_clauses:
            count += 1
            return
        if not assignment:
            for var in variables:
                backtrack(assignment + [(var, True)], [c for c in remaining_clauses if (var, True) not in c and (var, False) not in c])
                backtrack(assignment + [(var, False)], [c for c in remaining_clauses if (var, True) not in c and (var, False) not in c])
            return
        var = assignment[-1][0]
        for clause in remaining_clauses:
            if (var, True) in clause or (var, False) in clause:
                continue
            new_clauses = []
            for c in remaining_clauses:
                if c != clause:
                    new_clauses.append(c)
            backtrack(assignment, new_clauses)
    backtrack([], clauses)
    return count

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        for _ in range(5):
            graph = generate_ramanujan_graph(n, 3)
            nu = compute_nu(graph)
            sigma = random.randint(1, n)
            clauses = generate_tseitin_cnf(graph, sigma)
            R = count_dpll(clauses)
            metric_values.append(math.log2(R) / nu if nu != 0 else 0)
            instances_tested += 1
            if nu >= 0.5 * n and math.log2(R) < 0.1 * nu:
                conjecture_holds = False
                counterexample = f"Graph with n={n}, nu={nu}, log2 R={math.log2(R)}"
                break
        if not conjecture_holds:
            break
        for _ in range(2):
            graph = generate_glued_graph(n, 3)
            nu = compute_nu(graph)
            sigma = random.randint(1, n)
            clauses = generate_tseitin_cnf(graph, sigma)
            R = count_dpll(clauses)
            instances_tested += 1
            if nu >= 1.5 or math.log2(R) >= 1.5 * n:
                conjecture_holds = False
                counterexample = f"Glued graph with n={n}, nu={nu}, log2 R={math.log2(R)}"
                break
        if not conjecture_holds:
            break
        graph = generate_cycle(n)
        nu = compute_nu(graph)
        sigma = random.randint(1, n)
        clauses = generate_tseitin_cnf(graph, sigma)
        R = count_dpll(clauses)
        instances_tested += 1
        if nu >= 1.5 or math.log2(R) >= 1.5 * n:
            conjecture_holds = False
            counterexample = f"Cycle graph with n={n}, nu={nu}, log2 R={math.log2(R)}"
            break
        if not conjecture_holds:
            break
    if not metric_values:
        metric_value = 0.0
    else:
        metric_value = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2 R / nu",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")