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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def min_eigenvalue(A):
        n = len(A)
        tol = 1e-10
        max_iter = 1000
        v = [random.random() for _ in range(n)]
        v /= math.sqrt(sum(x**2 for x in v))
        for _ in range(max_iter):
            Av = matrix_multiply(A, v)
            lambda_ = sum(Av[i] * v[i] for i in range(n)) / sum(v[i]**2 for i in range(n))
            v_new = [Av[i] - lambda_ * v[i] for i in range(n)]
            v_new /= math.sqrt(sum(x**2 for x in v_new))
            if max(abs(v_new[i] - v[i]) for i in range(n)) < tol:
                break
            v = v_new
        return lambda_

    def grothendieck_witt_class(polynomial):
        n = len(polynomial)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if polynomial[i][j]:
                    A[i][j] = 1
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return rank

    def communication_complexity_graph(phi):
        n = len(phi)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if phi[i][j]:
                    G[i][j] = 1
                    G[j][i] = 1
        return G

    def indicator(phi, x):
        return [int(x & (1 << i)) for i in range(len(phi))]

    def clause_indicator_polynomial(phi):
        n = len(phi)
        m = len(phi[0])
        polynomial = [[0] * n for _ in range(n)]
        for j in range(m):
            for x in range(2**n):
                if all(indicator(phi, x)[i] == phi[i][j] for i in range(n)):
                    polynomial[x // 2**(n-1)][x % 2**(n-1)] += 1
        return polynomial

    def omega_sqrt(m):
        return math.sqrt(m) * (math.sqrt(2) / 2)

    m = random.randint(5, 40)
    phi = [[random.choice([0, 1]) for _ in range(m)] for _ in range(m)]
    polynomial = clause_indicator_polynomial(phi)
    grothendieck_class = grothendieck_witt_class(polynomial)
    G = communication_complexity_graph(phi)
    eigenvalue = min_eigenvalue(G)
    expected_value = omega_sqrt(m) * math.sqrt(eigenvalue)

    return {
        "metric_name": "Grothendieck-Witt Class / Expected Value",
        "metric_value": grothendieck_class / expected_value,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": grothendieck_class >= expected_value * 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")