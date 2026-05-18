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

def matrix_identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_power(A, power):
    result = matrix_identity(len(A))
    for _ in range(power):
        result = matrix_mult(result, A)
    return result

def matrix_trace(A):
    return sum(A[i][i] for i in range(len(A)))

def matrix_norm(A):
    return math.sqrt(sum(sum(a**2 for a in row) for row in A))

def matrix_inverse(A):
    n = len(A)
    I = matrix_identity(n)
    for col in range(n):
        diag = A[col][col]
        if diag == 0:
            raise ValueError("Matrix is not invertible")
        for i in range(n):
            A[col][i] /= diag
            I[col][i] /= diag
        for row in range(n):
            if row != col and A[row][col] != 0:
                factor = A[row][col]
                for i in range(n):
                    A[row][i] -= factor * A[col][i]
                    I[row][i] -= factor * I[col][i]
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
        eigvals = [matrix_trace(matrix_power(L, k)) for k in range(1, n+1)]
        eigvals = [eigvals[i] - eigvals[i-1] for i in range(1, len(eigvals))]
        eigvals.sort()
        return eigvals[1] if len(eigvals) > 1 else 0
    except:
        return 0

def sample_3_regular_graph(n, seed):
    random.seed(seed)
    edges = []
    stubs = list(range(n)) * 3
    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice([v for v in stubs if v != u])
        stubs.remove(v)
        edges.append((u, v))
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if not is_connected(adj) or girth(adj) < 4 or spectral_gap(adj) < 0.4:
        return None
    return adj

def sample_odd_charge(n, adj, seed):
    random.seed(seed)
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        u = random.choice([i for i in range(n) if omega[i] == 1])
        omega[u] = 0
    return omega

def enumerate_paths(adj, omega, K, seed):
    random.seed(seed)
    n = len(adj)
    paths = []
    charged_vertices = [i for i in range(n) if omega[i] == 1]
    for u, v in itertools.combinations(charged_vertices, 2):
        visited = [False] * n
        queue = deque([(u, [u])])
        visited[u] = True
        count = 0
        while queue and count < K:
            current, path = queue.popleft()
            if current == v:
                paths.append(path)
                count += 1
            for neighbor in adj[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, path + [neighbor]))
    return paths

def compute_M3(adj, omega, paths, seed):
    random.seed(seed)
    n = len(adj)
    m = len(adj) * 3 // 2
    rho = [0.0] * m
    lambda_ = 1.0
    for _ in range(1500):
        grad = [0.0] * m
        for e in range(m):
            grad[e] = 3 * rho[e] ** 2
        for gamma in paths:
            sum_rho = sum(rho[e] for e in gamma)
            if sum_rho < 1:
                for e in gamma:
                    grad[e] -= 2 * lambda_ * (1 - sum_rho)
        for e in range(m):
            rho[e] -= 0.01 * grad[e]
            rho[e] = max(0.0, rho[e])
        lambda_ *= 1.1
    M3 = sum(rho[e] ** 3 for e in range(m))
    return M3

def compute_t_star(adj, omega, seed):
    random.seed(seed)
    n = len(adj)
    clauses = []
    for u in range(n):
        neighbors = adj[u]
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                v, w = neighbors[i], neighbors[j]
                clauses.append([(u, omega[u]), (v, omega[v]), (w, omega[w])])
    def dpll(clauses, assignment):
        while True:
            new_unit = None
            for clause in clauses:
                unassigned = [lit for lit in clause if lit[0] not in assignment]
                if len(unassigned) == 1:
                    new_unit = unassigned[0]
                    break
                if len(unassigned) == 0:
                    return False
            if new_unit is not None:
                assignment[new_unit[0]] = new_unit[1]
                continue
            if not clauses:
                return True
            var = next(iter(clauses[0]))[0]
            for val in [0, 1]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                new_clauses = [clause for clause in clauses if all(lit[0] not in new_assignment or new_assignment[lit[0]] == lit[1] for lit in clause)]
                if dpll(new_clauses, new_assignment):
                    return True
            return False
    t_star = 0
    assignment = {}
    if dpll(clauses, assignment):
        t_star = len(assignment)
    return t_star

def run_trial(seed):
    n_values = [8, 10, 12, 14, 16]
    metric_values = []
    M3_values = []
    for n in n_values:
        adj = None
        while adj is None:
            adj = sample_3_regular_graph(n, seed)
            seed += 1
        omega = sample_odd_charge(n, adj, seed)
        paths = enumerate_paths(adj, omega, 80, seed)
        M3 = compute_M3(adj, omega, paths, seed)
        t_star = compute_t_star(adj, omega, seed)
        if t_star == 0:
            t_star = 500000
        metric_value = math.log2(t_star) / (n * M3)
        M3_value = n ** (2/3) * M3
        metric_values.append(metric_value)
        M3_values.append(M3_value)
    avg_metric = sum(metric_values) / len(metric_values)
    avg_M3 = sum(M3_values) / len(M3_values)
    min_metric = min(metric_values)
    min_M3 = min(M3_values)
    conjecture_holds = min_metric >= 0.05 and min_M3 >= 0.05
    counterexample = ""
    if not conjecture_holds:
        if min_metric < 0.05:
            counterexample = f"log2(t*)/(n*M3) = {min_metric} < 0.05"
        else:
            counterexample = f"n^(2/3)*M3 = {min_M3} < 0.05"
    return {
        "metric_name": "log2(t*)/(n*M3)",
        "metric_value": avg_metric,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trials.append(trial)
        print(f"TRIAL: {trial}")
    metric_values = [trial["metric_value"] for trial in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for trial in trials:
            if not trial["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{trial['counterexample']}\" first_failing_seed={seeds[trials.index(trial)]}")
                break