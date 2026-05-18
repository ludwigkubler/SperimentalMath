# auto-injected by SEC sandbox
import itertools
import json
import os
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import time
from collections import deque, defaultdict
from fractions import Fraction

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

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scalar_mult(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_trace(A):
    return sum(A[i][i] for i in range(min(len(A), len(A[0]))))

def matrix_norm(A):
    return math.sqrt(sum(sum(a**2 for a in row) for row in A))

def matrix_inverse(A):
    n = len(A)
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        diag_row = max(range(col, n), key=lambda r: abs(A[r][col]))
        A[col], A[diag_row] = A[diag_row], A[col]
        I[col], I[diag_row] = I[diag_row], I[col]
        if A[col][col] == 0:
            raise ValueError("Matrix is not invertible")
        for i in range(col + 1, n):
            factor = Fraction(A[i][col], A[col][col])
            for j in range(col, n):
                A[i][j] -= factor * A[col][j]
            for j in range(n):
                I[i][j] -= factor * I[col][j]
    for col in reversed(range(n)):
        for i in reversed(range(col)):
            factor = Fraction(A[i][col], A[col][col])
            for j in range(n):
                A[i][j] -= factor * A[col][j]
                I[i][j] -= factor * I[col][j]
    for i in range(n):
        factor = Fraction(1, A[i][i])
        for j in range(n):
            I[i][j] *= factor
    return I

def is_connected(adj):
    n = len(adj)
    visited = [False] * n
    stack = [0]
    visited[0] = True
    count = 1
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
                count += 1
    return count == n

def girth(adj):
    n = len(adj)
    min_girth = float('inf')
    for u in range(n):
        visited = [-1] * n
        queue = deque([(u, 0)])
        visited[u] = 0
        while queue:
            v, dist = queue.popleft()
            for w in adj[v]:
                if visited[w] == -1:
                    visited[w] = dist + 1
                    queue.append((w, dist + 1))
                elif w != u and visited[w] >= dist:
                    cycle_length = visited[w] + dist + 1
                    if cycle_length < min_girth:
                        min_girth = cycle_length
    return min_girth if min_girth != float('inf') else 0

def spectral_gap(adj):
    n = len(adj)
    D = [[0]*n for _ in range(n)]
    for i in range(n):
        D[i][i] = len(adj[i])
    L = matrix_sub(D, adj)
    try:
        L_inv = matrix_inverse(L)
        eigs = [matrix_trace(matrix_mult(L, L_inv)) / n]
        return 1 - eigs[0]
    except:
        return 0

def sample_3_regular_graph(n, seed):
    random.seed(seed)
    while True:
        edges = []
        stubs = list(range(n)) * 3
        random.shuffle(stubs)
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i+1]
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        if is_connected(adj) and girth(adj) >= 4 and spectral_gap(adj) >= 0.4:
            return adj

def sample_odd_charge(n, seed):
    random.seed(seed)
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[random.randint(0, n-1)] ^= 1
    return omega

def find_simple_paths(adj, omega, K=80):
    n = len(adj)
    paths = []
    charged_vertices = [v for v in range(n) if omega[v] == 1]
    for u in charged_vertices:
        for v in charged_vertices:
            if u != v:
                visited = [False] * n
                queue = deque([(u, [u])])
                visited[u] = True
                count = 0
                while queue and count < K:
                    current, path = queue.popleft()
                    for neighbor in adj[current]:
                        if neighbor == v:
                            paths.append(path + [neighbor])
                            count += 1
                        elif not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append((neighbor, path + [neighbor]))
    return paths

def compute_M3(adj, omega, paths, max_iter=1500):
    m = len(adj) * 3 // 2
    rho = [Fraction(1, m) for _ in range(m)]
    lambda_val = 1
    for _ in range(max_iter):
        grad = [3 * rho[i]**2 for i in range(m)]
        for path in paths:
            path_edges = set()
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                if u > v:
                    u, v = v, u
                edge_idx = (u * (2*m - u - 1) // 2 + v - u - 1) // 2
                path_edges.add(edge_idx)
            sum_rho = sum(rho[i] for i in path_edges)
            if sum_rho < 1:
                for i in path_edges:
                    grad[i] += 2 * lambda_val * (1 - sum_rho)
        step_size = 0.01
        new_rho = [max(0, rho[i] - step_size * grad[i]) for i in range(m)]
        if sum((new_rho[i] - rho[i])**2 for i in range(m)) < 1e-6:
            break
        rho = new_rho
        lambda_val *= 1.1
    return sum(rho[i]**3 for i in range(m))

def tseitin_tree_resolution(adj, omega, max_nodes=500000):
    n = len(adj)
    clauses = []
    for u in range(n):
        neighbors = adj[u]
        for i in range(len(neighbors)):
            for j in range(i+1, len(neighbors)):
                v, w = neighbors[i], neighbors[j]
                clauses.append((u, v, w))
    variables = [f'x_{u}_{v}' for u in range(n) for v in adj[u]]
    assignments = {}
    nodes_explored = 0

    def backtrack():
        nonlocal nodes_explored
        if nodes_explored >= max_nodes:
            return float('inf')
        nodes_explored += 1
        if all(omega[u] == sum(1 for v in adj[u] if assignments.get(f'x_{u}_{v}', 0)) % 2 for u in range(n)):
            return 0
        for clause in clauses:
            u, v, w = clause
            x_uv = assignments.get(f'x_{u}_{v}', None)
            x_uw = assignments.get(f'x_{u}_{w}', None)
            if x_uv is not None and x_uw is not None and x_uv != x_uw:
                continue
            if x_uv is None:
                for val in [0, 1]:
                    assignments[f'x_{u}_{v}'] = val
                    result = backtrack()
                    if result != float('inf'):
                        return result + 1
                    del assignments[f'x_{u}_{v}']
            if x_uw is None:
                for val in [0, 1]:
                    assignments[f'x_{u}_{w}'] = val
                    result = backtrack()
                    if result != float('inf'):
                        return result + 1
                    del assignments[f'x_{u}_{w}']
        return float('inf')

    start_time = time.time()
    result = backtrack()
    elapsed = time.time() - start_time
    if elapsed > 230:
        return float('inf')
    return result

def run_trial(seed):
    n = random.choice([8, 10, 12, 14, 16])
    adj = sample_3_regular_graph(n, seed)
    omega = sample_odd_charge(n, seed)
    paths = find_simple_paths(adj, omega)
    M3 = compute_M3(adj, omega, paths)
    t_star = tseitin_tree_resolution(adj, omega)
    metric_value = math.log2(t_star) / (n * M3) if M3 > 0 else float('inf')
    metric_value2 = n**(2/3) * M3
    conjecture_holds = metric_value >= 0.05 and metric_value2 >= 0.05
    counterexample = f"n={n}, log2(t*)/(n*M3)={metric_value}, n^(2/3)*M3={metric_value2}" if not conjecture_holds else ""
    return {
        "metric_name": "log2(t*)/(n*M3)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
        "n": n,
        "M3": M3,
        "t_star": t_star
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["conjecture_holds"]]
    metric_values2 = [trial["n"]**(2/3) * trial["M3"] for trial in trials if trial["conjecture_holds"]]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values)) if metric_values else 0
    mean_metric2 = sum(metric_values2) / len(metric_values2) if metric_values2 else 0
    std_metric2 = math.sqrt(sum((x - mean_metric2)**2 for x in metric_values2) / len(metric_values2)) if metric_values2 else 0
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={trials[first_failing_seed]['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=0")