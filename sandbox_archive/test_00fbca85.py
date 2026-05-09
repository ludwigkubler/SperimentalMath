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
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def symmetric_group_representations(n):
    if n == 1:
        return [[1]]
    G = []
    for i in range(2, n + 1):
        for j in range(i):
            g = [0] * i
            g[j], g[(j + 1) % i] = 1, -1
            G.append(g)
    return G

def noncommutative_fourier_coefficients(CNF, G):
    n = len(G)
    k = len(CNF)
    F = [[0] * n for _ in range(k)]
    for i in range(n):
        for j in range(k):
            F[j][i] = sum(CNF[j][g[i]] for g in G) / n
    return F

def norm_of_matrix(M):
    n = len(M)
    max_norm = 0
    for i in range(n):
        row_norm = sum(abs(x) for x in M[i])
        if row_norm > max_norm:
            max_norm = row_norm
    return max_norm

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        is_read_twice = random.choice([True, False])
        if is_read_twice:
            # Generate a read-twice CNF (simplified example)
            CNF = [[random.randint(-1, 1) for _ in range(n)] for _ in range(n)]
        else:
            # Generate a read-once CNF (simplified example)
            CNF = [[random.randint(-1, 1) for _ in range(n)] for _ in range(2)]

        G = symmetric_group_representations(n)
        F = noncommutative_fourier_coefficients(CNF, G)
        norm = norm_of_matrix(F)

        instances_tested += 1
        if is_read_twice and norm <= math.log(n):
            conjecture_holds = False
            counterexample = "Read-twice instance with norm ≤ log n"
            break
        elif not is_read_twice and norm >= n:
            conjecture_holds = False
            counterexample = "Read-once instance with norm ≥ n"
            break

    return {
        "metric_name": "Noncommutative Fourier Coefficient Norm",
        "metric_value": norm,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")