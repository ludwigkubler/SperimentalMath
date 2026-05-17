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

def matrix_scale(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_norm(A):
    return math.sqrt(sum(sum(a**2 for a in row) for row in A))

def matrix_identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def matrix_power(A, power):
    result = matrix_identity(len(A))
    for _ in range(power):
        result = matrix_multiply(result, A)
    return result

def matrix_trace(A):
    return sum(A[i][i] for i in range(len(A)))

def matrix_determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0.0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in A[1:]]
        det += ((-1)**col) * A[0][col] * matrix_determinant(minor)
    return det

def matrix_inverse(A):
    n = len(A)
    inverse = [[0.0 for _ in range(n)] for _ in range(n)]
    det = matrix_determinant(A)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in (A[:i] + A[i+1:])]
            inverse[j][i] = ((-1)**(i+j)) * matrix_determinant(minor) / det
    return inverse

def matrix_eigen(A, max_iter=1000, tol=1e-10):
    n = len(A)
    eigenvectors = matrix_identity(n)
    for _ in range(max_iter):
        Q, R = qr_decomposition(A)
        A = matrix_multiply(R, Q)
        eigenvectors = matrix_multiply(eigenvectors, Q)
        if matrix_norm(matrix_subtract(A, matrix_scale(matrix_identity(n), A[0][0]))) < tol:
            break
    eigenvalues = [A[i][i] for i in range(n)]
    return eigenvalues, eigenvectors

def qr_decomposition(A):
    n = len(A)
    Q = [[0.0 for _ in range(n)] for _ in range(n)]
    R = [[0.0 for _ in range(n)] for _ in range(n)]
    for k in range(n):
        R[k][k] = math.sqrt(sum(A[i][k]**2 for i in range(k, n)))
        Q[k][k] = 1.0
        for i in range(k+1, n):
            Q[i][k] = A[i][k] / R[k][k]
            for j in range(k+1, n):
                R[k][j] += Q[i][k] * A[i][j]
    return Q, R

def generate_erdos_renyi(n, p):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                graph[i][j] = graph[j][i] = 1
    return graph

def generate_random_regular(n, d):
    if n * d % 2 != 0:
        raise ValueError("n * d must be even")
    graph = [[0 for _ in range(n)] for _ in range(n)]
    edges = []
    for i in range(n):
        for _ in range(d):
            edges.append(i)
    random.shuffle(edges)
    for i in range(0, len(edges), 2):
        u, v = edges[i], edges[i+1]
        if u != v and graph[u][v] == 0:
            graph[u][v] = graph[v][u] = 1
    return graph

def generate_complete_graph(n):
    return [[1 if i != j else 0 for j in range(n)] for i in range(n)]

def generate_random_bipartite(n, p):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n//2):
        for j in range(n//2, n):
            if random.random() < p:
                graph[i][j] = graph[j][i] = 1
    return graph

def generate_planted_bisection(n, noise):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n//2):
        for j in range(n//2, n):
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
    A = [[float(x) for x in row] for row in graph]
    for i in range(n):
        D[i][i] = sum(A[i])
    L = matrix_subtract(D, A)
    return L

def max_cut_ratio(graph):
    n = len(graph)
    max_cut = 0
    for mask in range(1 << n):
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
    eigenvalues, eigenvectors = matrix_eigen(L)
    sorted_indices = sorted(range(len(eigenvalues)), key=lambda i: eigenvalues[i])
    v2 = [eigenvectors[i][sorted_indices[1]] for i in range(len(graph))]
    v3 = [eigenvectors[i][sorted_indices[2]] for i in range(len(graph))]
    Z = max(abs(v2[i]*v2[j] + v3[i]*v3[j]) for i in range(len(graph)) for j in range(len(graph)))
    if Z == 0:
        Z = 1.0
    M = [[(v2[i]*v2[j] + v3[i]*v3[j]) / Z for j in range(len(graph))] for i in range(len(graph))]
    return M

def tp2_defect(graph):
    n = len(graph)
    M = spectral_pseudo_moment_matrix(graph)
    defect = 0
    for i, j in itertools.combinations(range(n), 2):
        for k, l in itertools.combinations(range(n), 2):
            minor = [[M[i][k], M[i][l]], [M[j][k], M[j][l]]]
            det = matrix_determinant(minor)
            if det < -1.0 / (n**3):
                defect += 1
    total = math.comb(n, 2)**2
    return defect / total if total > 0 else 0.0

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 14, 18, 22]
    families = [
        ('erdos_renyi', lambda n: generate_erdos_renyi(n, 0.5)),
        ('random_regular', lambda n: generate_random_regular(n, 3) if n % 2 == 0 else generate_random_regular(n, 2)),
        ('complete', generate_complete_graph),
        ('random_bipartite', lambda n: generate_random_bipartite(n, 0.5)),
        ('planted_bisection', lambda n: generate_planted_bisection(n, 0.1))
    ]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        for family_name, family_generator in families:
            graph = family_generator(n)
            r = max_cut_ratio(graph)
            delta = tp2_defect(graph)
            metric_values.append(delta)
            instances_tested += 1

            if r >= 0.879 and delta > 0.5 / math.sqrt(n):
                conjecture_holds = False
                counterexample = f"Graph with r={r} and delta={delta} violates condition (i)"
                break
            if n >= 12 and r <= 0.55 and delta < 0.10:
                conjecture_holds = False
                counterexample = f"Graph with r={r} and delta={delta} violates condition (ii)"
                break
        if not conjecture_holds:
            break

    if len(metric_values) == 0:
        return {
            "metric_name": "TP_2 defect",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }

    mean_delta = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "TP_2 defect",
        "metric_value": mean_delta,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        trials.append(result)
        print(f"TRIAL: {result}")

    if not trials:
        print("RESULT: INCONCLUSIVE reason=no_trials")
        sys.exit(0)

    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] is not None]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_metric_values")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")