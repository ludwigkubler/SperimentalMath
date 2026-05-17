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

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scalar_multiply(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_trace(A):
    return sum(A[i][i] for i in range(len(A)))

def matrix_determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in A[1:]]
        det += ((-1) ** col) * A[0][col] * matrix_determinant(minor)
    return det

def matrix_inverse(A):
    n = len(A)
    I = [[float(i == j) for j in range(n)] for i in range(n)]
    for col in range(n):
        diag = A[col][col]
        if diag == 0:
            raise ValueError("Matrix is singular")
        for i in range(n):
            A[col][i] /= diag
            I[col][i] /= diag
        for i in range(n):
            if i != col and A[i][col] != 0:
                factor = A[i][col]
                for j in range(n):
                    A[i][j] -= factor * A[col][j]
                    I[i][j] -= factor * I[col][j]
    return I

def matrix_power(A, power):
    n = len(A)
    result = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(power):
        result = matrix_multiply(result, A)
    return result

def matrix_eigen(A):
    n = len(A)
    if n == 1:
        return [A[0][0]], [[1.0]]
    # Power iteration for dominant eigenvalue
    b_k = [1.0 for _ in range(n)]
    for _ in range(100):
        b_k1 = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x**2 for x in b_k1))
        b_k = [x / norm for x in b_k1]
    eigenvalue = sum(b_k[i] * sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n))
    eigenvector = b_k
    return [eigenvalue], [eigenvector]

def generate_erdos_renyi(n, p):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                graph[i][j] = graph[j][i] = 1
    return graph

def generate_regular_graph(n, d):
    if d >= n or d % 2 != 0:
        raise ValueError("Invalid degree for regular graph")
    graph = [[0 for _ in range(n)] for _ in range(n)]
    vertices = list(range(n))
    for i in range(0, n, d):
        block = vertices[i:i+d]
        for j in range(len(block)):
            for k in range(j+1, len(block)):
                graph[block[j]][block[k]] = graph[block[k]][block[j]] = 1
    return graph

def generate_complete_graph(n):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            graph[i][j] = graph[j][i] = 1
    return graph

def generate_balanced_bipartite(n, p):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    half = n // 2
    for i in range(half):
        for j in range(half, n):
            if random.random() < p:
                graph[i][j] = graph[j][i] = 1
    return graph

def generate_planted_bisection(n, noise):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    half = n // 2
    for i in range(half):
        for j in range(half, n):
            graph[i][j] = graph[j][i] = 1
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < noise:
                graph[i][j] = 1 - graph[i][j]
                graph[j][i] = graph[i][j]
    return graph

def combinatorial_laplacian(graph):
    n = len(graph)
    D = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        D[i][i] = sum(graph[i])
    A = [[float(graph[i][j]) for j in range(n)] for i in range(n)]
    L = matrix_subtract(D, A)
    return L

def max_cut_ratio(graph):
    n = len(graph)
    max_cut = 0
    for mask in range(1, 1 << n):
        cut = 0
        for i in range(n):
            for j in range(i+1, n):
                if ((mask >> i) & 1) != ((mask >> j) & 1):
                    cut += graph[i][j]
        if cut > max_cut:
            max_cut = cut
    edge_count = sum(sum(row) for row in graph) // 2
    if edge_count == 0:
        return 0.0
    return max_cut / edge_count

def spectral_pseudo_moment_matrix(graph):
    L = combinatorial_laplacian(graph)
    n = len(L)
    eigenvalues, eigenvectors = matrix_eigen(L)
    v2 = eigenvectors[1] if len(eigenvectors) > 1 else [1.0 / math.sqrt(n)] * n
    v3 = eigenvectors[2] if len(eigenvectors) > 2 else [1.0 / math.sqrt(n)] * n
    Z = max(abs(v2[i] * v2[j] + v3[i] * v3[j]) for i in range(n) for j in range(n))
    if Z == 0:
        Z = 1.0
    M = [[(v2[i] * v2[j] + v3[i] * v3[j]) / Z for j in range(n)] for i in range(n)]
    return M

def tp2_defect(graph):
    M = spectral_pseudo_moment_matrix(graph)
    n = len(M)
    defect = 0
    for i, j in itertools.combinations(range(n), 2):
        for k, l in itertools.combinations(range(n), 2):
            minor = [[M[i][k], M[i][l]], [M[j][k], M[j][l]]]
            det = matrix_determinant(minor)
            if det < -1.0 / (n ** 3):
                defect += 1
    total = math.comb(n, 2) ** 2
    if total == 0:
        return 0.0
    return defect / total

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 14, 18, 22]
    families = [
        ("erdos_renyi", lambda n: generate_erdos_renyi(n, 0.5)),
        ("regular", lambda n: generate_regular_graph(n, 3)),
        ("complete", generate_complete_graph),
        ("balanced_bipartite", lambda n: generate_balanced_bipartite(n, 0.5)),
        ("planted_bisection", lambda n: generate_planted_bisection(n, 0.1))
    ]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0
    for n in n_values:
        for family_name, generator in families:
            graph = generator(n)
            r = max_cut_ratio(graph)
            delta = tp2_defect(graph)
            metric_values.append(delta)
            instances_tested += 1
            if n >= 12 and r <= 0.55 and delta < 0.10:
                conjecture_holds = False
                counterexample = f"n={n}, family={family_name}, r={r}, delta={delta}"
                break
            if r >= 0.879 and delta > 0.5 / math.sqrt(n):
                conjecture_holds = False
                counterexample = f"n={n}, family={family_name}, r={r}, delta={delta}"
                break
        if not conjecture_holds:
            break
    if len(metric_values) == 0:
        return {
            "metric_name": "tp2_defect",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    mean_delta = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "tp2_defect",
        "metric_value": mean_delta,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = []
    counterexamples = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        conjecture_holds_counts.append(result["conjecture_holds"])
        if not result["conjecture_holds"]:
            counterexamples.append((seed, result["counterexample"]))
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(conjecture_holds_counts) / len(conjecture_holds_counts) if conjecture_holds_counts else 0.0
    if counterexamples:
        first_failing_seed, first_counterexample = counterexamples[0]
        print(f'RESULT: FALSIFIED counterexample="{first_counterexample}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')