# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    n_values = [8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40]
    c_star_range = (Fraction(62, 100), Fraction(80, 100))
    threshold_ratio = 0.878
    min_ratio = 0.55
    instances_per_n = 30

    random.seed(seed)
    results = []

    for n in n_values:
        if n > 20 and n % 2 != 0:  # Skip odd n > 20 as they cannot be regular
            continue

        for _ in range(instances_per_n):
            G = generate_3_regular_graph(n)
            M_G = compute_M_G(G, n)
            R_G = count_real_roots(M_G, n)
            SDP_ratio = compute_SDP_ratio(M_G, G)

            results.append({
                "n": n,
                "R_G": R_G,
                "SDP_ratio": SDP_ratio
            })

    if not results:
        return {
            "metric_name": "R(G)/n",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    R_G_values = [r["R_G"] / r["n"] for r in results]
    mean_R_G = sum(R_G_values) / len(R_G_values)
    std_R_G = math.sqrt(sum((x - mean_R_G) ** 2 for x in R_G_values) / len(R_G_values))

    valid_instances = [r for r in results if r["SDP_ratio"] >= threshold_ratio]
    min_valid_R_G = min(valid_instances, key=lambda x: x["R_G"] / x["n"])["R_G"] / min_valid_R_G

    conjecture_holds = all(c_star_range[0] <= R_G / n <= c_star_range[1] for R_G in R_G_values) and min_valid_R_G >= min_ratio
    counterexample = "" if conjecture_holds else "SDP ratio < 0.878 with R/n < 0.55"

    return {
        "metric_name": "R(G)/n",
        "metric_value": mean_R_G,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_3_regular_graph(n: int) -> list:
    if n % 2 != 0 or n < 4:
        raise ValueError("n must be even and at least 4")

    vertices = list(range(n))
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            if len(edges) == (n * (n - 1)) // 2:
                break
            if random.choice([True, False]):
                edges.append((i, j))

    return [edges[i:i + n] for i in range(0, n * n, n)]

def compute_M_G(G: list, n: int) -> list:
    r = math.ceil(math.sqrt(2 * n))
    V = initialize_V(n, r)
    lambda_max = max(abs(eig) for eig in compute_eigenvalues(V))

    for _ in range(80):
        V = projected_gradient_ascent(G, V, lambda_max, r)

    return V @ V.T

def initialize_V(n: int, r: int) -> list:
    V = [[1] * n]
    for _ in range(r - 1):
        row = [random.gauss(0, 1) for _ in range(n)]
        norm = math.sqrt(sum(x ** 2 for x in row))
        V.append([x / norm for x in row])
    return V

def projected_gradient_ascent(G: list, V: list, lambda_max: float, r: int) -> list:
    n = len(V)
    M_G = V @ V.T
    gradient = compute_gradient(G, M_G, lambda_max)

    for i in range(n):
        V[i] = [v - 0.1 * lambda_max * g for v, g in zip(V[i], gradient[i])]
        norm = math.sqrt(sum(x ** 2 for x in V[i]))
        if norm != 0:
            V[i] = [x / norm for x in V[i]]

    return V

def compute_gradient(G: list, M_G: list, lambda_max: float) -> list:
    n = len(M_G)
    gradient = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j]:
                gradient[i][j] = (M_G[i][j] - lambda_max) / 2
                gradient[j][i] = gradient[i][j]

    return gradient

def compute_eigenvalues(M: list) -> list:
    def QR_with_shifts(A: list, shift: float) -> tuple:
        n = len(A)
        Q = [[0] * n for _ in range(n)]
        R = A.copy()

        for k in range(n):
            v = [x + shift for x in R[k]]
            norm = math.sqrt(sum(x ** 2 for x in v))
            q = [x / norm for x in v]

            Q[k][k] = norm
            for i in range(k + 1, n):
                R[i][k] = sum(q[j] * R[i][j] for j in range(k, n))
                for j in range(k, n):
                    R[i][j] -= q[k] * R[k][j]

        return Q, R

    def QR_iterations(A: list, max_iter=100) -> list:
        n = len(A)
        Q = [[float(i == j) for i in range(n)] for j in range(n)]
        R = A.copy()

        for _ in range(max_iter):
            Q, R = QR_with_shifts(R, -max_eigenvalue(R))
            A = R @ Q

        return R

    def max_eigenvalue(A: list) -> float:
        n = len(A)
        eigenvalues = [A[i][i] for i in range(n)]
        while True:
            new_eigenvalues = []
            for i in range(n):
                v = A[i]
                norm = math.sqrt(sum(x ** 2 for x in v))
                if norm == 0:
                    continue
                v = [x / norm for x in v]
                max_proj = -math.inf
                for j in range(n):
                    proj = sum(v[k] * A[j][k] for k in range(n))
                    if proj > max_proj:
                        max_proj = proj
                new_eigenvalues.append(max_proj)
            if all(abs(eig1 - eig2) < 1e-6 for eig1, eig2 in zip(eigenvalues, new_eigenvalues)):
                break
            eigenvalues = new_eigenvalues

        return max(eigenvalues)

    R = QR_iterations(M)
    eigenvalues = [R[i][i] for i in range(n)]
    return eigenvalues

def count_real_roots(M_G: list, n: int) -> int:
    interval = (-1 + 1 / math.sqrt(n), 1 - 1 / math.sqrt(n))
    count = 0
    for eig in compute_eigenvalues(M_G):
        if interval[0] < eig < interval[1]:
            count += 1
    return count

def compute_SDP_ratio(M_G: list, G: list) -> float:
    n = len(G)
    lambda_max = max(abs(eig) for eig in compute_eigenvalues(M_G))
    UB_G = sum(len(edges) for edges in G) / 2 + n * lambda_max / 4
    return (M_G[0][1] + M_G[1][0]) / (4 * UB_G)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i - 1 for i in range(5, 8)] + [31, 67, 97, 107, 127, 151, 181, 191, 211, 223]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_R_G = sum(r["metric_value"] for r in results) / len(results)
    std_R_G = math.sqrt(sum((r["metric_value"] - mean_R_G) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if c_star_range[0] <= r["metric_value"] <= c_star_range[1]) / len(results)

    if all(c_star_range[0] <= r["metric_value"] <= c_star_range[1] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_R_G} std={std_R_G} support_fraction={support_fraction}")
    elif any(r["SDP_ratio"] >= threshold_ratio and r["metric_value"] < min_ratio for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["SDP_ratio"] >= threshold_ratio and r["metric_value"] < min_ratio)
        print(f"RESULT: FALSIFIED counterexample='SDP ratio < 0.878 with R/n < 0.55' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")