# auto-injected by SEC sandbox
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
import json

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

def jacobi_rotation(A, max_iterations=30):
    n = len(A)
    V = [[0.0 if i != j else 1.0 for j in range(n)] for i in range(n)]
    for _ in range(max_iterations):
        max_off_diag = 0.0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(A[i][j]) > max_off_diag:
                    max_off_diag = abs(A[i][j])
                    p, q = i, j
        if max_off_diag < 1e-10:
            break
        if A[p][p] == A[q][q]:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan(2 * A[p][q] / (A[p][p] - A[q][q]))
        c = math.cos(theta)
        s = math.sin(theta)
        for i in range(n):
            new_p = c * A[p][i] - s * A[q][i]
            new_q = s * A[p][i] + c * A[q][i]
            A[p][i] = new_p
            A[q][i] = new_q
        for i in range(n):
            new_p = c * A[i][p] - s * A[i][q]
            new_q = s * A[i][p] + c * A[i][q]
            A[i][p] = new_p
            A[i][q] = new_q
        for i in range(n):
            new_p = c * V[i][p] - s * V[i][q]
            new_q = s * V[i][p] + c * V[i][q]
            V[i][p] = new_p
            V[i][q] = new_q
    eigenvalues = [A[i][i] for i in range(n)]
    return eigenvalues, V

def compute_laplacian_eigenvalues(adj_matrix):
    n = len(adj_matrix)
    degree_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        degree_matrix[i][i] = sum(adj_matrix[i])
    laplacian = matrix_subtract(degree_matrix, adj_matrix)
    eigenvalues, _ = jacobi_rotation(laplacian)
    eigenvalues.sort()
    return [e for e in eigenvalues if abs(e) > 1e-10]

def compute_capacity(eigenvalues):
    if len(eigenvalues) < 2:
        return 0.0
    max_eig = max(eigenvalues)
    if max_eig == 0:
        return 0.0
    rescaled = [e / max_eig for e in eigenvalues if e > 0]
    if len(rescaled) < 2:
        return 0.0
    product = 1.0
    for i in range(len(rescaled)):
        for j in range(i + 1, len(rescaled)):
            product *= abs(rescaled[i] - rescaled[j])
    denominator = (len(rescaled) - 1) * (len(rescaled) - 2)
    if denominator == 0:
        return 0.0
    return product ** (2.0 / denominator)

def generate_random_3_regular(n):
    if n % 2 != 0:
        return None
    edges = []
    stubs = list(range(n)) * 3
    random.shuffle(stubs)
    while stubs:
        u = stubs.pop()
        v = stubs.pop()
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    return adj_matrix

def generate_erdos_renyi(n, p):
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1
    return adj_matrix

def generate_complete_bipartite(n):
    k = n // 2
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(k):
        for j in range(k, n):
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
    return adj_matrix

def generate_random_union_of_cliques(n):
    a = random.randint(2, n - 2)
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(a):
        for j in range(i + 1, a):
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
    for i in range(a, n):
        for j in range(i + 1, n):
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
    u = random.randint(0, a - 1)
    v = random.randint(a, n - 1)
    adj_matrix[u][v] = 1
    adj_matrix[v][u] = 1
    return adj_matrix

def generate_cycle_with_chord(n):
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        adj_matrix[i][(i + 1) % n] = 1
        adj_matrix[(i + 1) % n][i] = 1
    u = random.randint(0, n - 1)
    v = random.randint(0, n - 1)
    if u != v and abs(u - v) > 1 and abs(u - v) < n - 1:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    return adj_matrix

def is_connected(adj_matrix):
    n = len(adj_matrix)
    visited = [False] * n
    stack = [0]
    visited[0] = True
    while stack:
        u = stack.pop()
        for v in range(n):
            if adj_matrix[u][v] and not visited[v]:
                visited[v] = True
                stack.append(v)
    return all(visited)

def compute_max_cut(adj_matrix):
    n = len(adj_matrix)
    max_cut_size = 0
    for mask in range(1, 1 << n):
        cut_size = 0
        for u in range(n):
            for v in range(u + 1, n):
                if ((mask >> u) & 1) != ((mask >> v) & 1) and adj_matrix[u][v]:
                    cut_size += 1
        if cut_size > max_cut_size:
            max_cut_size = cut_size
    return max_cut_size

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 12, 16]
    ensemble_generators = [
        generate_random_3_regular,
        lambda n: generate_erdos_renyi(n, 0.3),
        generate_complete_bipartite,
        generate_random_union_of_cliques,
        generate_cycle_with_chord
    ]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        for generator in ensemble_generators:
            for _ in range(5):
                adj_matrix = generator(n)
                if adj_matrix is None or not is_connected(adj_matrix):
                    continue
                eigenvalues = compute_laplacian_eigenvalues(adj_matrix)
                if len(eigenvalues) < 2:
                    continue
                cap = compute_capacity(eigenvalues)
                max_cut = compute_max_cut(adj_matrix)
                if max_cut == 0:
                    continue
                gap = n * eigenvalues[-1] / (4 * max_cut) - 1
                if gap > 1 * cap + 0.01:
                    conjecture_holds = False
                    counterexample = f"n={n}, gap={gap}, cap={cap}, eigenvalues={eigenvalues}, max_cut={max_cut}"
                    break
                metric_values.append(gap - cap)
                instances_tested += 1
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break
    if conjecture_holds and len(metric_values) > 0:
        mean_metric = sum(metric_values) / len(metric_values)
        std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    else:
        mean_metric = 0.0
        std_metric = 0.0
    return {
        "metric_name": "gap_minus_cap",
        "metric_value": mean_metric,
        "metric_std": std_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
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
    total_instances = sum(r["instances_tested"] for r in results)
    if total_instances == 0:
        print("RESULT: INCONCLUSIVE reason=no_instances_tested")
        sys.exit(0)
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}")
    else:
        falsified = any(r["counterexample"] for r in results)
        if falsified:
            first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
            first_counterexample = next(r["counterexample"] for r in results if r["counterexample"])
            print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")