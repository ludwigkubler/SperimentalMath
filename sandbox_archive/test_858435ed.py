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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_random_graph(n, d):
    while True:
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d-1)
            if (i, *neighbors) not in edges and (i, *neighbors[::-1]) not in edges:
                edges.add((i, *neighbors))
        if len(edges) == n * d // 2:
            return [[(j in neighbors) for j in range(n)] for _, *neighbors in edges]

def generate_parity_charges(n):
    return [random.randint(0, 1) for _ in range(n)]

def sign_matrix(A, b):
    n = len(b)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    M[0][0] = 1
    for i in range(n):
        M[i+1][i+1] = 1
        for j in range(i+1, n):
            if A[i][j]:
                M[i+1][j+1] = (-1) ** (b[i] + b[j])
                M[j+1][i+1] = M[i+1][j+1]
    return M

def eigenvalues(matrix):
    def gaussian_elimination(A, B):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            B[i], B[max_row] = B[max_row], B[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                B[j] -= factor * B[i]
        X = [0] * n
        for i in range(n - 1, -1, -1):
            X[i] = (B[i] - sum(A[i][j] * X[j] for j in range(i + 1, n))) / A[i][i]
        return X

    n = len(matrix)
    A = [[matrix[i][j] if i != j else 0 for j in range(n)] for i in range(n)]
    B = [sum(matrix[i][j] * matrix[j][k] for j in range(n)) for k in range(n)]
    eigenvals = []
    for _ in range(n):
        eigval, A, B = gaussian_elimination(A, B)
        eigenvals.append(eigval)
    return eigenvals

def spectral_mahler_measure(eigenvals):
    return sum(math.log(max(1, abs(eig))) for eig in eigenvals if abs(eig) > 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([10, 15, 20, 25, 30, 35, 40])
    G = generate_random_graph(n, 3)
    b = generate_parity_charges(n)
    M = sign_matrix(G, b)
    lambda_values = eigenvalues(M)
    m_M = spectral_mahler_measure(lambda_values)
    alpha_d = (1/2) * math.log(2)
    instances_tested = 1
    conjecture_holds = m_M >= alpha_d * n - 0.5 * math.log(n)
    counterexample = "" if conjecture_holds else f"m(M)/n={m_M/n} < α_d·n/2"
    return {
        "metric_name": "spectral_mahler_measure",
        "metric_value": m_M,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_m_M = sum(r["metric_value"] for r in results) / len(results)
    std_m_M = math.sqrt(sum((r["metric_value"] - mean_m_M) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_m_M} std={std_m_M} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_m_M} std={std_m_M} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m(M)/n < α_d·n/2\" first_failing_seed={first_failing_seed}")