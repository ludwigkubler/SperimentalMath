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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

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

def generate_disj_n(n):
    X = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    Y = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    M = [x + y for x, y in zip(X, Y)]
    return X, Y, M

def matrix_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    A_copy = [row[:] for row in A]
    for j in range(n):
        i_max = max(range(rank, m), key=lambda i: abs(A_copy[i][j]))
        if abs(A_copy[i_max][j]) < 1e-9:
            continue
        A_copy[rank], A_copy[i_max] = A_copy[i_max], A_copy[rank]
        for i in range(m):
            if i != rank:
                factor = A_copy[i][j] / A_copy[rank][j]
                for k in range(n):
                    A_copy[i][k] -= factor * A_copy[rank][k]
        rank += 1
    return rank

def flatten_tensor(M):
    m, n = len(M), len(M[0])
    flat = []
    for i in range(m):
        for j in range(n):
            flat.extend(M[i][j])
    return flat

def tensor_rank_approximation(tensor, rank_bound):
    m, n = len(tensor), len(tensor[0])
    A = [[tensor[i][j] for j in range(n)] for i in range(m)]
    U, S, Vt = [], [], []
    for _ in range(rank_bound):
        u = [random.random() for _ in range(m)]
        v = [random.random() for _ in range(n)]
        s = sum(u[i] * v[j] for i in range(m) for j in range(n))
        U.append([u[i] / s for i in range(m)])
        Vt.append([v[j] / s for j in range(n)])
        S.append(s)
    return U, S, Vt

def secant_variety_dimension(M):
    flat = flatten_tensor(M)
    rank_bound = int(math.sqrt(len(flat)))
    U, S, Vt = tensor_rank_approximation(flat, rank_bound)
    rank = matrix_rank([u + v for u, v in zip(U, Vt)])
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        X, Y, M = generate_disj_n(n)
        dim_sec = secant_variety_dimension(M)
        expected_bound = math.sqrt(n * n)
        if dim_sec < 0.8 * expected_bound:
            conjecture_holds = False
            counterexample = f"n={n}, dim(sec(M))={dim_sec} < 0.8*sqrt({n}*{n})={expected_bound}"
        total_metric_value += dim_sec
        instances_tested += n

    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
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

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")