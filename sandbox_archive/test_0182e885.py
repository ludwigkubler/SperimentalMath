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

def matrix_eigen(matrix):
    n = len(matrix)
    if n == 1:
        return [matrix[0][0]], [[1.0]]

    # Initialize with identity matrix
    eigenvectors = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        eigenvectors[i][i] = 1.0

    # Power iteration to find dominant eigenvector
    b_k = [1.0 for _ in range(n)]
    for _ in range(100):
        b_k1 = matrix_multiply(matrix, [b_k])[0]
        norm = math.sqrt(sum(x**2 for x in b_k1))
        if norm == 0:
            break
        b_k = [x / norm for x in b_k1]

    # Rayleigh quotient for eigenvalue
    eigenvalue = sum(b_k[i] * sum(matrix[i][j] * b_k[j] for j in range(n)) for i in range(n))

    # Deflate the matrix
    deflated = [[0.0 for _ in range(n-1)] for _ in range(n-1)]
    for i in range(n-1):
        for j in range(n-1):
            deflated[i][j] = matrix[i+1][j+1] - (matrix[i+1][0] * matrix[0][j+1]) / (eigenvalue - matrix[0][0])

    # Recursively find eigenvalues of deflated matrix
    eigenvalues_rest, eigenvectors_rest = matrix_eigen(deflated)

    eigenvalues = [eigenvalue] + eigenvalues_rest
    eigenvectors = [[b_k[i]] + [0.0 for _ in range(n-1)] for i in range(n)]
    for i in range(n-1):
        for j in range(n-1):
            eigenvectors[i+1][j+1] = eigenvectors_rest[i][j]

    return eigenvalues, eigenvectors

def combinatorial_laplacian(graph):
    n = len(graph)
    degree = [sum(graph[i]) for i in range(n)]
    laplacian = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        laplacian[i][i] = degree[i]
        for j in range(n):
            if graph[i][j]:
                laplacian[i][j] = -1.0
    return laplacian

def spectral_pseudo_moment_matrix(graph):
    n = len(graph)
    if n < 2:
        return [[1.0]]

    L = combinatorial_laplacian(graph)
    eigenvalues, eigenvectors = matrix_eigen(L)

    # Get second and third eigenvectors (unit norm)
    v2 = eigenvectors[1] if len(eigenvectors) > 1 else [1.0 / math.sqrt(n) for _ in range(n)]
    v3 = eigenvectors[2] if len(eigenvectors) > 2 else [0.0 for _ in range(n)]

    # Normalize eigenvectors
    norm_v2 = math.sqrt(sum(x**2 for x in v2))
    norm_v3 = math.sqrt(sum(x**2 for x in v3))
    if norm_v2 == 0:
        norm_v2 = 1.0
    if norm_v3 == 0:
        norm_v3 = 1.0
    v2 = [x / norm_v2 for x in v2]
    v3 = [x / norm_v3 for x in v3]

    # Compute M_G
    M = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            M[i][j] = (v2[i] * v2[j] + v3[i] * v3[j])

    # Normalize by Z
    Z = max(abs(M[i][j]) for i in range(n) for j in range(n))
    if Z == 0:
        Z = 1.0
    M = [[x / Z for x in row] for row in M]

    return M

def tp2_defect(graph):
    n = len(graph)
    if n < 2:
        return 0.0

    M = spectral_pseudo_moment_matrix(graph)
    count = 0
    total = 0

    for i, j, k, l in itertools.product(range(n), repeat=4):
        if i < j and k < l:
            minor = M[i][k] * M[j][l] - M[i][l] * M[j][k]
            if minor < -1.0 / (n**3):
                count += 1
            total += 1

    if total == 0:
        return 0.0
    return count / total

def max_cut_ratio(graph):
    n = len(graph)
    max_cut = 0
    total_edges = sum(sum(row) for row in graph) // 2

    for mask in range(1, 1 << n):
        cut = 0
        for i in range(n):
            for j in range(i+1, n):
                if ((mask >> i) & 1) != ((mask >> j) & 1) and graph[i][j]:
                    cut += 1
        if cut > max_cut:
            max_cut = cut

    if total_edges == 0:
        return 0.0
    return max_cut / total_edges

def generate_erdos_renyi(n, p):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                graph[i][j] = 1
                graph[j][i] = 1
    return graph

def generate_regular(n, d):
    if d >= n or d % 2 != 0:
        return generate_erdos_renyi(n, 0.5)

    graph = [[0 for _ in range(n)] for _ in range(n)]
    vertices = list(range(n))
    for i in range(n):
        neighbors = random.sample(vertices, d)
        for j in neighbors:
            if i != j:
                graph[i][j] = 1
                graph[j][i] = 1
    return graph

def generate_complete(n):
    graph = [[1 if i != j else 0 for j in range(n)] for i in range(n)]
    return graph

def generate_balanced_bipartite(n, p):
    if n % 2 != 0:
        n -= 1
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n//2):
        for j in range(n//2, n):
            if random.random() < p:
                graph[i][j] = 1
                graph[j][i] = 1
    return graph

def generate_planted_bisection(n, noise):
    if n % 2 != 0:
        n -= 1
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n//2):
        for j in range(n//2, n):
            if random.random() < 1.0 - noise:
                graph[i][j] = 1
                graph[j][i] = 1
    return graph

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 14, 18, 22]
    families = [
        ("erdos_renyi", lambda n: generate_erdos_renyi(n, 0.5)),
        ("regular", lambda n: generate_regular(n, 3)),
        ("complete", generate_complete),
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
            delta = tp2_defect(graph)
            r = max_cut_ratio(graph)

            if r >= 0.879 and delta > 0.5 / math.sqrt(n):
                conjecture_holds = False
                counterexample = f"n={n}, family={family_name}, r={r}, delta={delta}"
                break
            elif n >= 12 and r <= 0.55 and delta < 0.10:
                conjecture_holds = False
                counterexample = f"n={n}, family={family_name}, r={r}, delta={delta}"
                break

            metric_values.append(delta)
            instances_tested += 1

        if not conjecture_holds:
            break

    if len(metric_values) == 0:
        metric_values = [0.0]

    return {
        "metric_name": "TP_2 defect",
        "metric_value": sum(metric_values) / len(metric_values),
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
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    if len(metric_values) > 0:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    else:
        mean = 0.0
        std = 0.0

    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean:.4f} std={std:.4f} support_fraction={support_fraction:.4f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        first_counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")