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
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k] == 0:
                continue
            for j in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_norm(A):
    return math.sqrt(sum(sum(a**2 for a in row) for row in A))

def matrix_eigenvalues(A):
    n = len(A)
    eigenvalues = []
    for _ in range(n):
        x = [random.random() for _ in range(n)]
        x = [a / matrix_norm(x) for a in x]
        for _ in range(100):
            Ax = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            x = [a / matrix_norm(Ax) for a in Ax]
        eigenvalue = sum(x[i] * Ax[i] for i in range(n))
        eigenvalues.append(eigenvalue)
        A = [[A[i][j] - eigenvalue * (i == j) for j in range(n)] for i in range(n)]
    return sorted(eigenvalues)

def compute_hcf(L, n):
    eigenvalues = matrix_eigenvalues(L)
    sum_lambda2 = sum(l**2 for l in eigenvalues[1:])
    sum_lambda4 = sum(l**4 for l in eigenvalues[1:])
    hcf = (n - 1) * sum_lambda4 / (sum_lambda2 ** 2)
    return hcf

def compute_max_cut(G, n):
    max_cut = 0
    for S in itertools.product([0, 1], repeat=n-1):
        S = list(S) + [0]
        cut = sum(G[i][j] for i in range(n) for j in range(n) if S[i] != S[j])
        if cut > max_cut:
            max_cut = cut
    return max_cut / 2

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    edges = []
    stubs = list(range(n)) * 3
    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice([s for s in stubs if s != u])
        stubs.remove(v)
        edges.append((u, v))
    G = [[0] * n for _ in range(n)]
    for u, v in edges:
        G[u][v] = 1
        G[v][u] = 1
    return G

def run_trial(seed):
    n = random.choice([12, 14, 16, 18, 20])
    G = generate_3_regular_graph(n, seed)
    D = [[sum(G[i]) if i == j else 0 for j in range(n)] for i in range(n)]
    L = [[D[i][j] - G[i][j] for j in range(n)] for i in range(n)]
    hcf = compute_hcf(L, n)
    eigenvalues = matrix_eigenvalues(L)
    sb = (n / 4) * eigenvalues[-1]
    mc = compute_max_cut(G, n)
    rho = mc / sb
    U = 1 - (1 / 10) * math.sqrt((hcf - 1) / (n - 1))
    conjecture_holds = rho <= U
    counterexample = f"rho={rho}, U={U}" if not conjecture_holds else ""
    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        conjecture_holds.append(result["conjecture_holds"])
        if not result["conjecture_holds"]:
            print(f'RESULT: FALSIFIED counterexample="{result["counterexample"]}" first_failing_seed={seed}')
            sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds) / len(conjecture_holds)
    if support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')