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

def matrix_norm(A):
    return math.sqrt(sum(sum(a**2 for a in row) for row in A))

def matrix_eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]

    # Power iteration to find the largest eigenvalue
    x = [random.random() for _ in range(n)]
    for _ in range(100):
        x = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
        norm = matrix_norm([x])
        if norm == 0:
            x = [random.random() for _ in range(n)]
        else:
            x = [a / norm for a in x]

    # Rayleigh quotient approximation
    lambda_max = sum(x[i] * sum(A[i][j] * x[j] for j in range(n)) for i in range(n)) / sum(a**2 for a in x)

    # Deflate and find the next eigenvalue
    B = [[A[i][j] - lambda_max * (i == j) for j in range(n)] for i in range(n)]
    eigenvalues = matrix_eigenvalues(B)
    eigenvalues.append(lambda_max)
    return sorted(eigenvalues)

def compute_hcf(L, n):
    eigenvalues = matrix_eigenvalues(L)
    sum_lambda2 = sum(l**2 for l in eigenvalues[1:])
    sum_lambda4 = sum(l**4 for l in eigenvalues[1:])
    if sum_lambda2 == 0:
        return 1.0
    hcf = (n - 1) * sum_lambda4 / sum_lambda2**2
    return max(1.0, min(hcf, n - 1))

def compute_max_cut(G, n):
    max_cut = 0
    for mask in range(1, 1 << (n - 1)):
        cut = 0
        for i in range(n):
            for j in range(i + 1, n):
                if ((mask >> i) & 1) != ((mask >> j) & 1) and j in G[i]:
                    cut += 1
        if cut > max_cut:
            max_cut = cut
    return max_cut

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    while True:
        edges = []
        stubs = list(range(n)) * 3
        random.shuffle(stubs)
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i + 1]
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        if len(edges) == 3 * n // 2:
            G = defaultdict(list)
            for u, v in edges:
                G[u].append(v)
                G[v].append(u)
            return G

def run_trial(seed):
    n = random.choice([12, 14, 16, 18, 20])
    G = generate_3_regular_graph(n, seed)

    # Compute Laplacian matrix L = D - A
    D = [[0.0 for _ in range(n)] for _ in range(n)]
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    for u in range(n):
        D[u][u] = len(G[u])
        for v in G[u]:
            A[u][v] = -1.0

    L = [[D[i][j] + A[i][j] for j in range(n)] for i in range(n)]

    # Compute eigenvalues
    eigenvalues = matrix_eigenvalues(L)
    lambda_1 = eigenvalues[-1]

    # Compute HCF, SB, MC
    hcf = compute_hcf(L, n)
    sb = (n / 4) * lambda_1
    mc = compute_max_cut(G, n)

    # Compute rho and U
    rho = mc / sb if sb != 0 else 0.0
    u = 1 - (1 / 10) * math.sqrt((hcf - 1) / (n - 1))

    conjecture_holds = rho <= u
    counterexample = "" if conjecture_holds else f"rho={rho:.4f} > U={u:.4f}"

    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
        "n": n,
        "hcf": hcf,
        "sb": sb,
        "mc": mc,
        "u": u
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]

    metric_values = []
    conjecture_holds_counts = 0
    total_instances = 0
    first_failing_seed = None
    first_counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        else:
            if first_failing_seed is None:
                first_failing_seed = seed
                first_counterexample = result["counterexample"]
        total_instances += result["instances_tested"]

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values)) if len(metric_values) > 1 else 0.0
    support_fraction = conjecture_holds_counts / total_instances if total_instances > 0 else 0.0

    if first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")