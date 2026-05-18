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

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_norm(A):
    return max(sum(abs(x) for x in row) for row in A)

def matrix_inverse(A):
    n = len(A)
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = col
        for row in range(col + 1, n):
            if abs(A[row][col]) > abs(A[pivot][col]):
                pivot = row
        if A[pivot][col] == 0:
            raise ValueError("Matrix is not invertible")
        A[col], A[pivot] = A[pivot], A[col]
        I[col], I[pivot] = I[pivot], I[col]
        for row in range(col + 1, n):
            factor = Fraction(A[row][col], A[col][col])
            for c in range(col, n):
                A[row][c] -= factor * A[col][c]
            for c in range(n):
                I[row][c] -= factor * I[col][c]
    for col in reversed(range(n)):
        for row in range(col):
            factor = Fraction(A[row][col], A[col][col])
            for c in range(col, n):
                A[row][c] -= factor * A[col][c]
            for c in range(n):
                I[row][c] -= factor * I[col][c]
    for row in range(n):
        factor = Fraction(1, A[row][row])
        for col in range(n):
            I[row][col] *= factor
    return I

def sample_3_regular_graph(n, seed):
    random.seed(seed)
    stubs = list(range(n)) * 3
    adj = [[] for _ in range(n)]
    while stubs:
        u = stubs.pop()
        if not stubs:
            break
        v = random.choice([v for v in stubs if v != u])
        stubs.remove(v)
        adj[u].append(v)
        adj[v].append(u)
    return adj

def is_connected(adj):
    n = len(adj)
    visited = [False] * n
    queue = deque([0])
    visited[0] = True
    count = 1
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                count += 1
                queue.append(v)
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
                elif visited[w] >= dist + 1:
                    cycle_length = visited[v] + visited[w] + 1
                    if cycle_length < min_girth:
                        min_girth = cycle_length
    return min_girth

def spectral_gap(adj):
    n = len(adj)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = len(adj[i])
    L = matrix_subtract(D, adj)
    try:
        L_inv = matrix_inverse(L)
    except ValueError:
        return 0
    M = matrix_mult(L_inv, D)
    eigenvalues = [sum(M[i][j] for j in range(n)) for i in range(n)]
    eigenvalues.sort(reverse=True)
    return eigenvalues[1]

def sample_odd_charge(n, seed):
    random.seed(seed + 1)
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[random.randint(0, n - 1)] ^= 1
    return omega

def enumerate_paths(adj, omega, K):
    n = len(adj)
    paths = []
    for u in range(n):
        if omega[u] == 0:
            continue
        for v in range(u + 1, n):
            if omega[v] == 0:
                continue
            visited = [False] * n
            queue = deque([(u, [u])])
            visited[u] = True
            while queue and len(paths) < K:
                current, path = queue.popleft()
                if current == v:
                    paths.append(path)
                    continue
                for neighbor in adj[current]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append((neighbor, path + [neighbor]))
    return paths

def compute_M3(adj, omega, paths):
    n = len(adj)
    m = sum(len(row) for row in adj) // 2
    rho = [Fraction(1, m) for _ in range(m)]
    edge_to_index = {}
    index = 0
    for u in range(n):
        for v in adj[u]:
            if u < v:
                edge_to_index[(u, v)] = index
                index += 1
    for _ in range(1500):
        gradient = [0] * m
        for path in paths:
            path_edges = set()
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                if u > v:
                    u, v = v, u
                path_edges.add(edge_to_index[(u, v)])
            sum_rho = sum(rho[e] for e in path_edges)
            if sum_rho < 1:
                for e in path_edges:
                    gradient[e] += 1
        for e in range(m):
            gradient[e] += 3 * rho[e] ** 2
        step_size = 0.01
        for e in range(m):
            rho[e] -= step_size * gradient[e]
            if rho[e] < 0:
                rho[e] = 0
    M3 = sum(rho[e] ** 3 for e in range(m))
    return float(M3)

def tseitin_tree_resolution(adj, omega, max_nodes=500000):
    n = len(adj)
    clauses = []
    for u in range(n):
        for v in adj[u]:
            if u < v:
                clauses.append([(u, 1), (v, 1)])
    for u in range(n):
        clauses.append([(u, omega[u])])
    nodes = 0
    stack = [clauses]
    while stack and nodes < max_nodes:
        current = stack.pop()
        nodes += 1
        if not current:
            return nodes
        clause = current[0]
        if len(clause) == 1:
            literal = clause[0]
            new_clauses = []
            for c in current[1:]:
                if literal in c:
                    continue
                new_clause = [l for l in c if l != (-literal[0], 1 - literal[1])]
                if not new_clause:
                    return nodes
                new_clauses.append(new_clause)
            stack.append(new_clauses)
        else:
            for i in range(len(clause)):
                literal = clause[i]
                new_clauses = []
                for c in current[1:]:
                    if literal in c:
                        continue
                    new_clause = [l for l in c if l != (-literal[0], 1 - literal[1])]
                    if not new_clause:
                        return nodes
                    new_clauses.append(new_clause)
                stack.append(new_clauses)
    return max_nodes

def run_trial(seed):
    n = random.choice([8, 10, 12, 14, 16])
    adj = sample_3_regular_graph(n, seed)
    if not is_connected(adj):
        return {
            "metric_name": "log2(t*)/(n*M3)",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph not connected"
        }
    if girth(adj) < 4:
        return {
            "metric_name": "log2(t*)/(n*M3)",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Girth < 4"
        }
    lambda_2 = spectral_gap(adj)
    if lambda_2 < 0.4:
        return {
            "metric_name": "log2(t*)/(n*M3)",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Spectral gap < 0.4"
        }
    omega = sample_odd_charge(n, seed)
    paths = enumerate_paths(adj, omega, 80)
    M3 = compute_M3(adj, omega, paths)
    t_star = tseitin_tree_resolution(adj, omega)
    if t_star >= 500000:
        return {
            "metric_name": "log2(t*)/(n*M3)",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Timeout in t* computation"
        }
    log2_t_star = math.log2(t_star)
    ratio = log2_t_star / (n * M3)
    n_23_ratio = n ** (2/3) * M3
    if ratio < 0.05 or n_23_ratio < 0.05:
        return {
            "metric_name": "log2(t*)/(n*M3)",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Ratio {ratio} or n^(2/3)*M3 {n_23_ratio} < 0.05"
        }
    return {
        "metric_name": "log2(t*)/(n*M3)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)
    metric_values = [trial["metric_value"] for trial in trials if trial["conjecture_holds"]]
    n_23_values = [trial["instances_tested"] ** (2/3) * trial["metric_value"] for trial in trials if trial["conjecture_holds"]]
    if not metric_values or not n_23_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
    else:
        mean_ratio = sum(metric_values) / len(metric_values)
        std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in metric_values) / len(metric_values))
        mean_n_23 = sum(n_23_values) / len(n_23_values)
        std_n_23 = math.sqrt(sum((x - mean_n_23) ** 2 for x in n_23_values) / len(n_23_values))
        support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
        if support_fraction >= 0.8 and min(metric_values) >= 0.05 and min(n_23_values) >= 0.05:
            print(f"RESULT: SUPPORTED mean={mean_ratio:.4f} std={std_ratio:.4f} support_fraction={support_fraction:.4f}")
        else:
            for trial in trials:
                if not trial["conjecture_holds"]:
                    print(f"RESULT: FALSIFIED counterexample=\"{trial['counterexample']}\" first_failing_seed={seeds[trials.index(trial)]}")
                    break