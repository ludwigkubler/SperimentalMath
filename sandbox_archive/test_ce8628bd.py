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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] %= 2
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] // A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) // A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bp(n, read_once):
        bp = [0] * (2 ** n)
        for i in range(2 ** n):
            if read_once:
                bp[i] = random.randint(0, 1)
            else:
                bp[random.randint(0, n - 1)] ^= 1
        return bp
    
    def fourier_transform(bp, n):
        m = 2 ** n
        A = [[0] * m for _ in range(m)]
        b = [0] * m
        for i in range(m):
            for j in range(m):
                A[i][j] = (i & j).bit_count() % 2
                if i == j:
                    b[j] = bp[i]
        x = gaussian_elimination(A, b)
        return sum(abs(x[i]) for i in range(m))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        read_twice_bp = generate_bp(n, False)
        read_once_bp = generate_bp(n, True)
        ft_read_twice = fourier_transform(read_twice_bp, n)
        ft_read_once = fourier_transform(read_once_bp, n)
        results.append((n, ft_read_twice, ft_read_once))
    
    total_ft_read_twice = sum(ft for _, ft, _ in results)
    total_ft_read_once = sum(ft for _, _, ft in results)
    instances_tested = len(results) * len(n_values)
    
    conjecture_holds = all(ft > n ** 2 for _, ft, _ in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Fourier Coefficient Sum",
        "metric_value": total_ft_read_twice,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(30)
        seeds = [p for p in primes if p <= 40]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")