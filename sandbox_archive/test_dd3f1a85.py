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
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_norm(A):
    return max(sum(abs(x) for x in row) for row in A)

def power_iteration(A, num_iterations=100):
    n = len(A)
    b = [random.random() for _ in range(n)]
    for _ in range(num_iterations):
        b = [sum(A[i][j] * b[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x**2 for x in b))
        b = [x / norm for x in b]
    return sum(b[i] * sum(A[i][j] * b[j] for j in range(n)) for i in range(n))

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

def generate_3_regular_graph(n):
    while True:
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for _ in range(3):
                j = random.randint(0, n-1)
                while j == i or (i, j) in edges or (j, i) in edges:
                    j = random.randint(0, n-1)
                graph[i].append(j)
                graph[j].append(i)
                edges.add((i, j))
        if is_connected(graph):
            return graph

def generate_glued_graph(n):
    graph1 = generate_3_regular_graph(n)
    graph2 = generate_3_regular_graph(n)
    graph = graph1 + graph2
    graph[0].append(n)
    graph[n].append(0)
    return graph

def generate_cycle(n):
    graph = [[] for _ in range(n)]
    for i in range(n):
        graph[i].append((i-1) % n)
        graph[i].append((i+1) % n)
    return graph

def build_B_matrix(graph):
    n = len(graph)
    m = sum(len(neighbors) for neighbors in graph) // 2
    edge_to_idx = {}
    idx_to_edge = []
    idx = 0
    for u in range(n):
        for v in graph[u]:
            if (u, v) not in edge_to_idx and (v, u) not in edge_to_idx:
                edge_to_idx[(u, v)] = idx
                idx_to_edge.append((u, v))
                idx += 1
    B = [[0 for _ in range(2*m)] for _ in range(2*m)]
    for u in range(n):
        for v in graph[u]:
            for w in graph[u]:
                if w != v:
                    if (u, v) in edge_to_idx and (w, u) in edge_to_idx:
                        B[edge_to_idx[(u, v)]][edge_to_idx[(w, u)]] = 1
    return B, edge_to_idx, idx_to_edge

def compute_nu(graph):
    B, edge_to_idx, idx_to_edge = build_B_matrix(graph)
    rho = power_iteration(B)
    d = 3
    n = len(graph)
    nu = n * max(0, math.log((d-1)/rho))
    return nu

def count_dpll(cnf, assignment=None, visited=None):
    if assignment is None:
        assignment = {}
    if visited is None:
        visited = set()
    if len(cnf) == 0:
        return 1, visited
    clause = cnf[0]
    for literal in clause:
        var = abs(literal)
        if var not in assignment:
            new_assignment = assignment.copy()
            new_assignment[var] = (literal > 0)
            new_cnf = [c for c in cnf if not (-literal in c)]
            for c in new_cnf:
                if literal in c:
                    c.remove(literal)
            count, new_visited = count_dpll(new_cnf, new_assignment, visited)
            visited.update(new_visited)
            if count > 0:
                return count, visited
    return 0, visited

def generate_tseitin_cnf(graph, sigma):
    n = len(graph)
    cnf = []
    for u in range(n):
        for v in graph[u]:
            if u < v:
                var = n + len(cnf) + 1
                cnf.append([u+1, v+1, -var])
                cnf.append([-(u+1), var])
                cnf.append([-(v+1), var])
    total_charge = sum(sigma.values())
    if total_charge % 2 != 1:
        var = n + len(cnf) + 1
        cnf.append([var])
        sigma[var] = 1
    return cnf

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            # Generate Ramanujan-like graph
            graph = generate_3_regular_graph(n)
            nu = compute_nu(graph)
            sigma = {i: random.choice([-1, 1]) for i in range(1, n+1)}
            cnf = generate_tseitin_cnf(graph, sigma)
            count, _ = count_dpll(cnf)
            R = math.log2(count)
            metric_values.append(R / nu if nu > 0 else float('inf'))
            instances_tested += 1

            # Generate glued graph
            graph = generate_glued_graph(n)
            nu = compute_nu(graph)
            sigma = {i: random.choice([-1, 1]) for i in range(1, 2*n+1)}
            cnf = generate_tseitin_cnf(graph, sigma)
            count, _ = count_dpll(cnf)
            R = math.log2(count)
            if nu >= 1.5 or R >= 1.5 * n:
                conjecture_holds = False
                counterexample = f"Glued graph with n={n}, nu={nu}, R={R}"
                break

            # Generate cycle
            graph = generate_cycle(n)
            nu = compute_nu(graph)
            sigma = {i: random.choice([-1, 1]) for i in range(1, n+1)}
            cnf = generate_tseitin_cnf(graph, sigma)
            count, _ = count_dpll(cnf)
            R = math.log2(count)
            if nu >= 1.5 or R >= 1.5 * n:
                conjecture_holds = False
                counterexample = f"Cycle with n={n}, nu={nu}, R={R}"
                break

            if not conjecture_holds:
                break

        if not conjecture_holds:
            break

    if len(metric_values) == 0:
        return {
            "metric_name": "log2 R / nu",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
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
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    if len(metric_values) == 0:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
    else:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
            first_failing_seed = seeds[results.index([r for r in results if not r["conjecture_holds"]][0])]
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")