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
    while True:
        stubs = [3] * n
        edges = []
        while stubs:
            u = random.choice([i for i, s in enumerate(stubs) if s > 0])
            v = random.choice([i for i, s in enumerate(stubs) if s > 0 and i != u])
            if (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
                stubs[u] -= 1
                stubs[v] -= 1
                if stubs[u] == 0:
                    stubs.remove(stubs[u])
                if stubs[v] == 0:
                    stubs.remove(stubs[v])
        if len(edges) == n:
            adjacency = [[0] * n for _ in range(n)]
            for u, v in edges:
                adjacency[u][v] = 1
                adjacency[v][u] = 1
            return adjacency

def jacobi_rotation(matrix):
    n = len(matrix)
    V = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for _ in range(100):
        max_val = Fraction(0)
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(matrix[i][j]) > max_val:
                    max_val = abs(matrix[i][j])
                    p, q = i, j
        if max_val == Fraction(0):
            break
        theta = Fraction(1, 2) * math.atan(Fraction(2 * matrix[p][q], matrix[p][p] - matrix[q][q]))
        c = math.cos(theta)
        s = math.sin(theta)
        for i in range(n):
            temp = matrix[i][p] * c - matrix[i][q] * s
            matrix[i][q] = matrix[i][p] * s + matrix[i][q] * c
            matrix[i][p] = temp
        for i in range(n):
            temp = V[i][p] * c - V[i][q] * s
            V[i][q] = V[i][p] * s + V[i][q] * c
            V[i][p] = temp
    eigenvalues = [matrix[i][i] for i in range(n)]
    return eigenvalues, V

def compute_moments(eigenvalues):
    n = len(eigenvalues)
    m1 = sum(eigenvalues) / n
    m2 = sum(e ** 2 for e in eigenvalues) / n
    m3 = sum(e ** 3 for e in eigenvalues) / n
    m4 = sum(e ** 4 for e in eigenvalues) / n
    return m1, m2, m3, m4

def compute_free_cumulants(m1, m2, m3, m4):
    kappa2 = m2 - m1 ** 2
    kappa4 = m4 - 4 * m3 * m1 - 2 * m2 ** 2 + 10 * m2 * m1 ** 2 - 5 * m1 ** 4
    return kappa2, kappa4

def compute_max_cut(adjacency):
    n = len(adjacency)
    max_cut = 0
    for mask in range(1, 1 << n):
        cut = 0
        for i in range(n):
            for j in range(i + 1, n):
                if ((mask >> i) & 1) != ((mask >> j) & 1):
                    cut += adjacency[i][j]
        if cut > max_cut:
            max_cut = cut
    return max_cut

def compute_sdp2(adjacency):
    n = len(adjacency)
    D = [sum(row) for row in adjacency]
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                L[i][j] = D[i]
            else:
                L[i][j] = -adjacency[i][j]
    L_hat = [[Fraction(L[i][j], 3) for j in range(n)] for i in range(n)]
    eigenvalues, _ = jacobi_rotation(L_hat)
    lambda_max = max(eigenvalues)
    sdp2 = (3 * n / 8) * (1 + lambda_max)
    return sdp2

def run_trial(seed):
    n = random.choice([8, 10, 12, 14, 16])
    adjacency = generate_3_regular_graph(n, seed)
    eigenvalues, _ = jacobi_rotation(adjacency)
    m1, m2, m3, m4 = compute_moments(eigenvalues)
    kappa2, kappa4 = compute_free_cumulants(m1, m2, m3, m4)
    max_cut = compute_max_cut(adjacency)
    sdp2 = compute_sdp2(adjacency)
    epsilon = max(0, kappa4 / (kappa2 ** 2) - 1) if kappa2 != 0 else 0
    g = sdp2 / max_cut if max_cut != 0 else 0
    T = (g - 1) * math.log2(n) - 4 * (epsilon + 1 / n)
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
    metric_values = []
    conjecture_holds_counts = 0
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)
    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for seed in seeds:
            result = run_trial(seed)
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={seed}")
                break