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
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = M[j][i]
                for k in range(i, n + 1):
                    M[j][k] -= factor * M[i][k]
    return [row[-1] for row in M]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def fourier_transform(M, n):
    N = 2 ** n
    F = [[0] * N for _ in range(N)]
    for k in range(N):
        for l in range(N):
            sum_val = 0
            for i in range(n):
                for j in range(n):
                    sum_val += M[i][j] * math.cos(2 * math.pi * (k * i + l * j) / N)
            F[k][l] = sum_val
    return F

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    F = fourier_transform(M, n)
    min_coeff = min(abs(coeff) for row in F for coeff in row)
    max_coeff = max(abs(coeff) for row in F for coeff in row)
    tau_M = min_coeff * max_coeff
    c = 1 / (2 * math.pi ** 2)
    conjecture_holds = tau_M >= c * n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "tau(M)",
        "metric_value": tau_M,
        "instances_tested": n * n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(30)
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_tau_M = sum(res["metric_value"] for res in results) / len(results)
    std_tau_M = math.sqrt(sum((res["metric_value"] - mean_tau_M) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_tau_M} std={std_tau_M} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_tau_M} std={std_tau_M} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")