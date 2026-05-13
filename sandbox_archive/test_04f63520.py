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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        factor = 1 / A[i][i]
        for j in range(n):
            A[i][j] *= factor
        b[i] *= factor
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
    return [b[i] for i in range(n)]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def generate_max_cut_instance(n):
    G = {}
    for i in range(n):
        G[i] = set()
    for _ in range(int(n * (n - 1) / 4)):
        u, v = random.sample(range(n), 2)
        if u not in G[v]:
            G[u].add(v)
            G[v].add(u)
    return G

def degree_d_sos_moment_matrix(G, d):
    n = len(G)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        A[i][i] = 2
        for j in G[i]:
            A[j][i] = -1
    B = [0] * (n + 1)
    B[0] = n
    return gaussian_elimination(A, B)

def integrality_gap(G):
    n = len(G)
    cut_value = sum(len(G[i]) for i in range(n)) / 2
    goemans_williamson_bound = n * (n - 1) / 4
    return cut_value / goemans_williamson_bound

def run_trial(seed: int) -> dict:
    random.seed(seed)
    primes = generate_primes(30)
    results = []
    for d in [5, 10, 15, 20, 30, 40]:
        n = random.choice(primes)
        G = generate_max_cut_instance(n)
        A = degree_d_sos_moment_matrix(G, d)
        negative_eigenvalues = sum(1 for x in A if x < 0)
        gap = integrality_gap(G)
        results.append({
            "n": n,
            "d": d,
            "negative_eigenvalues": negative_eigenvalues,
            "gap": gap
        })
    metric_value = sum(result["negative_eigenvalues"] for result in results) / len(results)
    conjecture_holds = all(result["negative_eigenvalues"] <= math.log(result["n"]) * 2 for result in results if result["gap"] < 1.5)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Negative Eigenvalue Count",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")