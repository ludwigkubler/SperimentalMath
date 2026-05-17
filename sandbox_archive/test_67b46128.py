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

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_norm(A):
    return math.sqrt(sum(sum(a**2 for a in row) for row in A))

def matrix_eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]

    # QR decomposition
    Q = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    R = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    for j in range(n):
        v = [Fraction(0) for _ in range(n)]
        for i in range(n):
            v[i] = A[i][j]
            for k in range(j):
                v[i] -= R[k][j] * Q[i][k]

        norm = matrix_norm([v])
        if norm == 0:
            continue

        for i in range(n):
            Q[i][j] = Fraction(v[i], norm)

        for k in range(j, n):
            R[j][k] = sum(Q[i][j] * A[i][k] for i in range(n))

    # Compute eigenvalues of R
    eigenvalues_R = []
    for i in range(n):
        eigenvalues_R.append(R[i][i])

    return eigenvalues_R

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")

    edges = []
    stubs = list(range(n)) * 3

    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice([s for s in stubs if s != u])
        stubs.remove(v)
        edges.append((u, v))

    # Check for multi-edges and self-loops
    edge_set = set()
    for u, v in edges:
        if u == v or (v, u) in edge_set:
            return None
        edge_set.add((u, v))

    return edges

def compute_laplacian(edges, n):
    A = [[0 for _ in range(n)] for _ in range(n)]
    D = [[0 for _ in range(n)] for _ in range(n)]

    for u, v in edges:
        A[u][v] = 1
        A[v][u] = 1
        D[u][u] += 1
        D[v][v] += 1

    L = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            L[i][j] = D[i][j] - A[i][j]

    return L

def compute_hcf(L, eigenvalues):
    n = len(L)
    sum_lambda_4 = sum(eigenvalue**4 for eigenvalue in eigenvalues[1:])
    sum_lambda_2 = sum(eigenvalue**2 for eigenvalue in eigenvalues[1:])
    if sum_lambda_2 == 0:
        return 1.0
    hcf = (n - 1) * sum_lambda_4 / (sum_lambda_2**2)
    return max(1.0, min(hcf, n - 1))

def compute_sb(L, eigenvalues):
    n = len(L)
    lambda_1 = eigenvalues[-1]
    return (n / 4) * lambda_1

def compute_mc(edges, n):
    max_cut = 0
    for subset in itertools.product([0, 1], repeat=n):
        cut_size = 0
        for u, v in edges:
            if subset[u] != subset[v]:
                cut_size += 1
        if cut_size > max_cut:
            max_cut = cut_size
    return max_cut

def run_trial(seed):
    n_values = [12, 14, 16, 18, 20]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Generate 5 graphs per n
            graph = None
            while graph is None:
                graph = generate_3_regular_graph(n, seed)
                seed += 1

            L = compute_laplacian(graph, n)
            eigenvalues = sorted(matrix_eigenvalues(L))

            hcf = compute_hcf(L, eigenvalues)
            sb = compute_sb(L, eigenvalues)
            mc = compute_mc(graph, n)

            if sb == 0:
                continue

            rho = mc / sb
            upper_bound = 1 - (1/10) * math.sqrt((hcf - 1) / (n - 1))

            if rho > upper_bound:
                conjecture_holds = False
                counterexample = f"n={n}, rho={rho}, upper_bound={upper_bound}, hcf={hcf}, sb={sb}, mc={mc}"

            metric_values.append(upper_bound - rho)
            instances_tested += 1

    if not metric_values:
        return {
            "metric_name": "margin",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "margin",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    instances_tested = 0
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        instances_tested += result["instances_tested"]
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for x in metric_values if x >= 0) / len(metric_values)

    if conjecture_holds_all and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif not conjecture_holds_all:
        first_failing_seed = seeds[next(i for i, x in enumerate(metric_values) if x < 0)]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")