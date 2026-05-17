# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def matrix_mult(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[j][i]
    return result

def jacobi_rotation(A):
    n = len(A)
    max_iter = 1000
    for _ in range(max_iter):
        max_val = 0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(A[i][j]) > max_val:
                    max_val = abs(A[i][j])
                    p, q = i, j
        if max_val < 1e-10:
            break
        theta = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
        c = math.cos(theta)
        s = math.sin(theta)
        R = [[0] * n for _ in range(n)]
        for i in range(n):
            R[i][i] = 1
        R[p][p] = c
        R[p][q] = -s
        R[q][p] = s
        R[q][q] = c
        A = matrix_mult(matrix_mult(matrix_transpose(R), A), R)
    eigenvalues = [A[i][i] for i in range(n)]
    return eigenvalues, A

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    stubs = [3] * n
    while True:
        random.shuffle(stubs)
        edges = []
        for i in range(0, n, 2):
            if stubs[i] > 0 and stubs[i+1] > 0:
                edges.append((i, i+1))
                stubs[i] -= 1
                stubs[i+1] -= 1
        if sum(stubs) == 0:
            break
    adj = [[0] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] += 1
        adj[v][u] += 1
    return adj

def compute_max_cut(adj):
    n = len(adj)
    max_cut = 0
    for mask in range(1, 1 << n):
        cut_size = 0
        for u in range(n):
            for v in range(u + 1, n):
                if ((mask >> u) & 1) != ((mask >> v) & 1):
                    cut_size += adj[u][v]
        if cut_size > max_cut:
            max_cut = cut_size
    return max_cut

def compute_free_cumulants(eigenvalues):
    n = len(eigenvalues)
    m1 = sum(eigenvalues) / n
    m2 = sum(e * e for e in eigenvalues) / n
    m3 = sum(e * e * e for e in eigenvalues) / n
    m4 = sum(e * e * e * e for e in eigenvalues) / n
    kappa_2 = m2 - m1 * m1
    kappa_4 = m4 - 4 * m3 * m1 - 2 * m2 * m2 + 10 * m2 * m1 * m1 - 5 * m1 * m1 * m1 * m1
    return kappa_2, kappa_4

def run_trial(seed):
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    adj = generate_3_regular_graph(n)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = sum(adj[i])
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            L[i][j] = D[i][j] - adj[i][j]
    L_hat = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            L_hat[i][j] = L[i][j] / 3
    eigenvalues, _ = jacobi_rotation(L_hat)
    kappa_2, kappa_4 = compute_free_cumulants(eigenvalues)
    max_cut = compute_max_cut(adj)
    lambda_max = max(eigenvalues)
    SDP_2 = (3 * n / 8) * (1 + lambda_max - 1)
    g = SDP_2 / max_cut
    epsilon = max(0, kappa_4 / (kappa_2 * kappa_2) - 1) if kappa_2 != 0 else 0
    T = (g - 1) * math.log2(n) - 4 * (epsilon + 1 / n)
    conjecture_holds = T <= 0
    counterexample = f"n={n}, T={T}" if not conjecture_holds else ""
    return {
        "metric_name": "T(G)",
        "metric_value": T,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    counterexamples = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        if result["counterexample"]:
            counterexamples.append(result["counterexample"])
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)
    if counterexamples:
        print(f'RESULT: FALSIFIED counterexample="{counterexamples[0]}" first_failing_seed={seeds[0]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')