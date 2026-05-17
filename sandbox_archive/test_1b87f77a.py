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

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    degrees = [3] * n
    while True:
        stubs = list(itertools.chain.from_iterable([i] * d for i, d in enumerate(degrees)))
        random.shuffle(stubs)
        edges = set()
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i+1]
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        if len(edges) == n * 3 // 2:
            break
    adjacency = [[0] * n for _ in range(n)]
    for u, v in edges:
        adjacency[u][v] = 1
        adjacency[v][u] = 1
    return adjacency

def matrix_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def jacobi_rotation(A):
    n = len(A)
    V = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for _ in range(100):
        max_val = Fraction(0)
        p, q = 0, 1
        for i in range(n):
            for j in range(i+1, n):
                if abs(A[i][j]) > max_val:
                    max_val = abs(A[i][j])
                    p, q = i, j
        if max_val == Fraction(0):
            break
        if A[p][p] == A[q][q]:
            theta = Fraction(math.pi/4)
        else:
            theta = Fraction(1, 2) * math.atan(2 * A[p][q] / (A[p][p] - A[q][q]))
        c = math.cos(theta)
        s = math.sin(theta)
        for i in range(n):
            A_ip = A[i][p]
            A_iq = A[i][q]
            A[i][p] = A_ip * c - A_iq * s
            A[i][q] = A_ip * s + A_iq * c
        for i in range(n):
            V_ip = V[i][p]
            V_iq = V[i][q]
            V[i][p] = V_ip * c - V_iq * s
            V[i][q] = V_ip * s + V_iq * c
        A[p][p] = A[p][p] * c**2 - 2 * A[p][q] * c * s + A[q][q] * s**2
        A[q][q] = A[p][p] * s**2 + 2 * A[p][q] * c * s + A[q][q] * c**2
        A[p][q] = A[q][p] = Fraction(0)
    eigenvalues = [A[i][i] for i in range(n)]
    return eigenvalues, V

def compute_free_cumulants(eigenvalues):
    n = len(eigenvalues)
    m1 = sum(eigenvalues) / n
    m2 = sum(e**2 for e in eigenvalues) / n - m1**2
    m3 = sum(e**3 for e in eigenvalues) / n - 3 * m1 * m2 - m1**3
    m4 = sum(e**4 for e in eigenvalues) / n - 4 * m1 * m3 - 6 * m2**2 - 4 * m1**2 * m2 - m1**4
    kappa2 = m2 - m1**2
    kappa4 = m4 - 4 * m3 * m1 - 2 * m2**2 + 10 * m2 * m1**2 - 5 * m1**4
    return kappa2, kappa4

def compute_max_cut(adjacency):
    n = len(adjacency)
    max_cut = 0
    for mask in range(1, 1 << n):
        cut = 0
        for u in range(n):
            for v in range(u+1, n):
                if ((mask >> u) & 1) != ((mask >> v) & 1):
                    cut += adjacency[u][v]
        if cut > max_cut:
            max_cut = cut
    return max_cut

def compute_sdp2(adjacency):
    n = len(adjacency)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = sum(adjacency[i])
    L = [[D[i][j] - adjacency[i][j] for j in range(n)] for i in range(n)]
    L_hat = [[Fraction(L[i][j], 3) for j in range(n)] for i in range(n)]
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    L_hat_minus_I = [[L_hat[i][j] - I[i][j] for j in range(n)] for i in range(n)]
    eigenvalues, _ = jacobi_rotation(L_hat_minus_I)
    lambda_max = max(eigenvalues)
    sdp2 = (3 * n / 8) * (1 + lambda_max)
    return sdp2

def run_trial(seed):
    n = random.choice([8, 10, 12, 14, 16])
    adjacency = generate_3_regular_graph(n, seed)
    eigenvalues, _ = jacobi_rotation(adjacency)
    kappa2, kappa4 = compute_free_cumulants(eigenvalues)
    max_cut = compute_max_cut(adjacency)
    sdp2 = compute_sdp2(adjacency)
    g = sdp2 / max_cut
    epsilon = max(0, kappa4 / kappa2**2 - 1)
    T = (g - 1) * math.log2(n) - 4 * (epsilon + 1/n)
    conjecture_holds = T <= 0
    counterexample = f"n={n}, T={T}" if not conjecture_holds else ""
    return {
        "metric_name": "T(G)",
        "metric_value": float(T),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = seeds[results.index(next(r for r in results if not r["conjecture_holds"]))]
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")