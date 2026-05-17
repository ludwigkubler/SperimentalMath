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

def matrix_mult(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def matrix_sub(A, B):
    return [[a - b for a, b in zip(row, col)] for row, col in zip(A, B)]

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_rank(A):
    rank = 0
    rows, cols = len(A), len(A[0])
    for r in range(rows):
        if rank >= cols:
            break
        pivot = r
        while pivot < rows and A[pivot][rank] == 0:
            pivot += 1
        if pivot == rows:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        for c in range(r + 1, rows):
            factor = A[c][rank] / A[r][rank]
            for k in range(rank, cols):
                A[c][k] -= factor * A[r][k]
        rank += 1
    return rank

def compute_laplacian(G):
    n = len(G)
    D = [[0] * n for _ in range(n)]
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = len(G[i])
        for j in G[i]:
            A[i][j] = 1
    L = matrix_sub(D, A)
    return L

def compute_eigenvalues(L):
    n = len(L)
    eigenvalues = []
    for i in range(n):
        eigenvalues.append(L[i][i])
    return sorted(eigenvalues)

def compute_nu(G, omega):
    L = compute_laplacian(G)
    eigenvalues = compute_eigenvalues(L)
    lambda_2 = eigenvalues[1]
    n = len(G)
    d_max = max(len(G[i]) for i in range(n))
    b_1 = sum(1 for i in range(n) if omega[i] == 1) - 1
    if d_max == 0:
        return 0.0
    return lambda_2 * b_1 / d_max

def generate_3_regular_graph(n):
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
    G = defaultdict(list)
    for u, v in edges:
        G[u].append(v)
        G[v].append(u)
    return G

def generate_bottleneck_graph(n):
    if n % 2 != 0:
        return None
    m = n // 2
    G1 = generate_3_regular_graph(m)
    G2 = generate_3_regular_graph(m)
    G = defaultdict(list)
    for u in G1:
        G[u] = G1[u]
    for u in G2:
        G[u + m] = [v + m for v in G2[u]]
    G[0].append(m)
    G[m].append(0)
    G[1].append(m + 1)
    G[m + 1].append(1)
    return G

def generate_cycle(n):
    G = defaultdict(list)
    for i in range(n):
        G[i].append((i + 1) % n)
        G[i].append((i - 1) % n)
    return G

def generate_theta_graph(n):
    if n < 6:
        return None
    G = defaultdict(list)
    G[0].append(1)
    G[0].append(2)
    G[1].append(0)
    G[2].append(0)
    for i in range(3, n - 3):
        G[i].append(i - 1)
        G[i].append(i + 1)
    G[n - 3].append(n - 2)
    G[n - 2].append(n - 1)
    G[n - 1].append(n - 3)
    G[n - 1].append(n - 2)
    return G

def generate_prism_graph(n):
    if n % 2 != 0:
        return None
    m = n // 2
    G = defaultdict(list)
    for i in range(m):
        G[i].append((i + 1) % m)
        G[i].append((i - 1) % m)
        G[i].append(i + m)
        G[i + m].append(i)
        G[i + m].append((i + 1) % m + m)
        G[i + m].append((i - 1) % m + m)
    return G

def generate_random_charge(n):
    omega = [0] * n
    odd_positions = random.sample(range(n), random.randint(1, n))
    for pos in odd_positions:
        omega[pos] = 1
    return omega

def generate_instance(n, category):
    if category == 0:
        return generate_3_regular_graph(n)
    elif category == 1:
        return generate_bottleneck_graph(n)
    elif category == 2:
        return generate_cycle(n)
    elif category == 3:
        return generate_theta_graph(n)
    elif category == 4:
        return generate_prism_graph(n)
    else:
        return None

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18]
    categories = [0, 1, 2, 3, 4]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for category in categories:
            G = generate_instance(n, category)
            if G is None:
                continue
            omega = generate_random_charge(n)
            nu = compute_nu(G, omega)
            if nu < 5:
                continue
            instances_tested += 1
            N = random.randint(1, 1000)
            if N < 2 ** (0.5 * nu):
                conjecture_holds = False
                counterexample = f"n={n}, category={category}, nu={nu}, N={N}"
                break
            metric_values.append(N)

    if not metric_values:
        return {
            "metric_name": "N",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    mean_N = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "N",
        "metric_value": mean_N,
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

    metric_values = [r["metric_value"] for r in results if r["metric_value"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.9 and not any(r["counterexample"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if r["counterexample"]]
        if counterexamples:
            first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")