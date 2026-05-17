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
    eigenvalues = [0.0] * n
    eigenvectors = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        if i == 0:
            eigenvalues[i] = matrix[0][0]
            eigenvectors[i][0] = 1.0
        else:
            deflated = [[0.0 for _ in range(n-i)] for _ in range(n-i)]
            for j in range(n-i):
                for k in range(n-i):
                    deflated[j][k] = matrix[j+1][k+1] - (matrix[j+1][0] * matrix[0][k+1]) / (eigenvalues[i-1] - matrix[0][0] + 1e-10)

            eigenvalues[i] = deflated[0][0]
            eigenvectors[i][i] = 1.0

    return eigenvalues, eigenvectors

def combinatorial_laplacian(graph):
    n = len(graph)
    D = [[0.0 for _ in range(n)] for _ in range(n)]
    A = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        D[i][i] = sum(graph[i])
        for j in range(n):
            if graph[i][j] == 1:
                A[i][j] = -1.0

    L = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            L[i][j] = D[i][j] + A[i][j]

    return L

def spectral_pseudo_moment_matrix(graph):
    L = combinatorial_laplacian(graph)
    eigenvalues, eigenvectors = matrix_eigen(L)

    v2 = eigenvectors[1]
    v3 = eigenvectors[2]

    n = len(graph)
    Z = max(abs(v2[i]*v2[j] + v3[i]*v3[j]) for i in range(n) for j in range(n))

    M = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            M[i][j] = (v2[i]*v2[j] + v3[i]*v3[j]) / Z

    return M

def tp2_defect(graph):
    M = spectral_pseudo_moment_matrix(graph)
    n = len(graph)
    count = 0
    total = 0

    for i, j, k, l in itertools.product(range(n), repeat=4):
        if i < j and k < l:
            minor = M[i][k]*M[j][l] - M[i][l]*M[j][k]
            if minor < -1.0/n**3:
                count += 1
            total += 1

    delta = count / total
    return delta

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

    edges = sum(sum(row) for row in graph) // 2
    if edges == 0:
        return 0.0
    return max_cut / edges

def generate_graph(n, family, seed):
    random.seed(seed)
    graph = [[0 for _ in range(n)] for _ in range(n)]

    if family == "erdos_renyi":
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    graph[i][j] = 1
                    graph[j][i] = 1
    elif family == "random_3_regular":
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                edges.append((i, j))
        random.shuffle(edges)
        for i in range(n // 2):
            u, v = edges[i]
            graph[u][v] = 1
            graph[v][u] = 1
    elif family == "complete":
        for i in range(n):
            for j in range(i+1, n):
                graph[i][j] = 1
                graph[j][i] = 1
    elif family == "balanced_bipartite":
        for i in range(n // 2):
            for j in range(n // 2, n):
                if random.random() < 0.5:
                    graph[i][j] = 1
                    graph[j][i] = 1
    elif family == "planted_bisection":
        for i in range(n // 2):
            for j in range(n // 2, n):
                if random.random() < 0.9:
                    graph[i][j] = 1
                    graph[j][i] = 1

    return graph

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 14, 18, 22]
    families = ["erdos_renyi", "random_3_regular", "complete", "balanced_bipartite", "planted_bisection"]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for family in families:
            graph = generate_graph(n, family, seed)
            delta = tp2_defect(graph)
            r = max_cut_ratio(graph)
            metric_values.append(delta)
            instances_tested += 1

            if r >= 0.879 and delta > 0.5 / math.sqrt(n):
                conjecture_holds = False
                counterexample = f"n={n}, family={family}, r={r}, delta={delta}"
                break
            elif n >= 12 and r <= 0.55 and delta < 0.10:
                conjecture_holds = False
                counterexample = f"n={n}, family={family}, r={r}, delta={delta}"
                break

        if not conjecture_holds:
            break

    if len(metric_values) == 0:
        metric_value = 0.0
    else:
        metric_value = sum(metric_values) / len(metric_values)

    return {
        "metric_name": "TP_2 defect",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    total_trials = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        total_trials += 1

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = conjecture_holds_counts / total_trials if total_trials > 0 else 0.0

    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexamples = [result["counterexample"] for result in [run_trial(seed) for seed in seeds] if not result["conjecture_holds"]]
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")