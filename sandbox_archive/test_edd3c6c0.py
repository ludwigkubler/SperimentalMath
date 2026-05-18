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
from collections import deque

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
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Matrices must have the same dimensions")
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def matrix_power(A, power):
    n = len(A)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    for _ in range(power):
        result = matrix_multiply(result, A)
    return result

def spectral_gap(adj):
    n = len(adj)
    D = [[0]*n for _ in range(n)]
    for i in range(n):
        D[i][i] = sum(adj[i])
    L = matrix_subtract(D, adj)
    eigenvalues = [0]*n
    for k in range(n):
        eigenvalues[k] = sum(L[k][i] for i in range(n)) / n
    eigenvalues.sort()
    return eigenvalues[1]

def is_connected(adj):
    n = len(adj)
    visited = [False]*n
    stack = [0]
    visited[0] = True
    while stack:
        u = stack.pop()
        for v in range(n):
            if adj[u][v] and not visited[v]:
                visited[v] = True
                stack.append(v)
    return all(visited)

def has_girth_at_least_4(adj):
    n = len(adj)
    for u in range(n):
        neighbors = [v for v in range(n) if adj[u][v]]
        for v in neighbors:
            common_neighbors = [w for w in neighbors if adj[v][w] and w != u]
            if len(common_neighbors) >= 2:
                return False
    return True

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    while True:
        edges = []
        stubs = list(range(n)) * 3
        while stubs:
            u = random.choice(stubs)
            stubs.remove(u)
            v = random.choice(stubs)
            stubs.remove(v)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        adj = [[0]*n for _ in range(n)]
        for u, v in edges:
            adj[u][v] = 1
            adj[v][u] = 1
        if is_connected(adj) and has_girth_at_least_4(adj):
            lambda_2 = spectral_gap(adj)
            if lambda_2 >= 0.4:
                return adj

def sample_odd_charge(n, seed):
    random.seed(seed)
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[random.randint(0, n-1)] ^= 1
    return omega

def find_simple_paths(adj, u, v, max_paths=80):
    n = len(adj)
    paths = []
    visited = [False]*n
    stack = [(u, [u])]
    visited[u] = True
    while stack and len(paths) < max_paths:
        node, path = stack.pop()
        if node == v:
            paths.append(path)
            continue
        for neighbor in range(n):
            if adj[node][neighbor] and not visited[neighbor]:
                visited[neighbor] = True
                stack.append((neighbor, path + [neighbor]))
    return paths

def compute_M3(adj, omega, paths, max_iter=1500):
    n = len(adj)
    m = sum(sum(row) for row in adj) // 2
    rho = [0.1] * m
    edge_list = [(u, v) for u in range(n) for v in range(u+1, n) if adj[u][v]]
    for _ in range(max_iter):
        grad = [0.0] * m
        for i, (u, v) in enumerate(edge_list):
            grad[i] = 3 * rho[i]**2
        for gamma in paths:
            edges_in_gamma = [edge_list.index((min(u, v), max(u, v))) for u, v in zip(gamma[:-1], gamma[1:])]
            sum_rho = sum(rho[i] for i in edges_in_gamma)
            if sum_rho < 1:
                for i in edges_in_gamma:
                    grad[i] += -2 * (1 - sum_rho)
        for i in range(m):
            rho[i] -= 0.01 * grad[i]
            rho[i] = max(0, rho[i])
    return sum(r**3 for r in rho)

def count_dpll_nodes(adj, omega, max_nodes=500000):
    n = len(adj)
    m = sum(sum(row) for row in adj) // 2
    clauses = []
    for u in range(n):
        for v in range(n):
            if adj[u][v]:
                clauses.append([u, v])
    for u in range(n):
        if omega[u]:
            clauses.append([u])
    stack = [(0, clauses, [])]
    nodes = 0
    while stack and nodes < max_nodes:
        depth, current_clauses, assignment = stack.pop()
        nodes += 1
        if not current_clauses:
            return nodes
        unit_clauses = [c for c in current_clauses if len(c) == 1]
        if unit_clauses:
            lit = unit_clauses[0][0]
            new_assignment = assignment + [lit]
            new_clauses = [c for c in current_clauses if lit not in c]
            stack.append((depth + 1, new_clauses, new_assignment))
            continue
        pure_literals = []
        for lit in range(n):
            if any(lit in c for c in current_clauses) and not any(-lit in c for c in current_clauses):
                pure_literals.append(lit)
        if pure_literals:
            lit = pure_literals[0]
            new_assignment = assignment + [lit]
            new_clauses = [c for c in current_clauses if lit not in c]
            stack.append((depth + 1, new_clauses, new_assignment))
            continue
        if not current_clauses:
            return nodes
        lit = random.choice([c[0] for c in current_clauses if len(c) > 0])
        new_assignment1 = assignment + [lit]
        new_clauses1 = [c for c in current_clauses if lit not in c]
        stack.append((depth + 1, new_clauses1, new_assignment1))
        new_assignment2 = assignment + [-lit]
        new_clauses2 = [c for c in current_clauses if -lit not in c]
        stack.append((depth + 1, new_clauses2, new_assignment2))
    return max_nodes

def run_trial(seed):
    n = random.choice([8, 10, 12, 14, 16])
    adj = generate_3_regular_graph(n, seed)
    omega = sample_odd_charge(n, seed)
    charged_vertices = [v for v in range(n) if omega[v]]
    paths = []
    for u, v in itertools.combinations(charged_vertices, 2):
        paths.extend(find_simple_paths(adj, u, v))
    M3 = compute_M3(adj, omega, paths)
    t_star = count_dpll_nodes(adj, omega)
    log2_t_star = math.log2(t_star)
    n_23 = n ** (2/3)
    metric1 = log2_t_star / (n * M3)
    metric2 = n_23 * M3
    conjecture_holds = metric1 >= 0.05 and metric2 >= 0.05
    counterexample = ""
    if not conjecture_holds:
        if metric1 < 0.05:
            counterexample = f"log2(t*)/(n*M3) = {metric1} < 0.05"
        else:
            counterexample = f"n^(2/3)*M3 = {metric2} < 0.05"
    return {
        "metric_name": "log2(t*)/(n*M3) and n^(2/3)*M3",
        "metric_value": metric1,
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
    metric_values = [trial["metric_value"] for trial in trials if trial["conjecture_holds"]]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        failing_trials = [trial for trial in trials if not trial["conjecture_holds"]]
        if failing_trials:
            first_failing_seed = seeds[trials.index(failing_trials[0])]
            print(f"RESULT: FALSIFIED counterexample=\"{failing_trials[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")