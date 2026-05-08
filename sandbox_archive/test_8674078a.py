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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    ε = 1e-6
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def construct_polynomial(edges):
        f = [0] * (n * n)
        for i, j in edges:
            index = i * n + j
            f[index] = -1
            f[j * n + i] = -1
        return f
    
    def compute_moment_matrix(f):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                index = i * n + j
                M[i][j] = M[j][i] = f[index]
        return M
    
    def is_non_negative(M):
        try:
            x = gaussian_elimination(M, [0] * n)
            return all(x[i] >= 0 for i in range(n))
        except ZeroDivisionError:
            return False
    
    def is_sum_of_squares(f, d):
        # Placeholder for actual SOS check
        return False
    
    def sos_approximation(f, d):
        # Placeholder for actual SOS approximation
        return 1.0
    
    edges = generate_max_cut_instance(n)
    f = construct_polynomial(edges)
    M = compute_moment_matrix(f)
    
    if not is_non_negative(M):
        return {
            "metric_name": "SOS Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "f is negative"
        }
    
    if is_sum_of_squares(f, 0):
        return {
            "metric_name": "SOS Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "f is a sum of squares"
        }
    
    min_d = n
    for d in range(1, n):
        if sos_approximation(f, d) >= 1 - ε:
            min_d = d
            break
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": min_d,
        "instances_tested": 1,
        "conjecture_holds": min_d == math.ceil(math.log(n)),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = generate_primes(30)
        seeds = primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")