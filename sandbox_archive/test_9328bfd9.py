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
    for num in range(2, n+1):
        if is_prime(num):
            primes.append(num)
    return primes

def legendre_symbol(a, p):
    if a == 0:
        return 0
    if a < 0:
        return (-1) ** ((p - 1) // 2) * legendre_symbol(-a, p)
    if a % p == 0:
        return 0
    s = (p - 1) // 2
    t = a
    r = 1
    while t != 1:
        e = 0
        while t & 1 == 0:
            t >>= 1
            e += 1
        if e % 2 == 1 and s % 2 == 1:
            r *= -1
        p, a = a, p % a
        s = (p - 1) // 2
    return r

def quadratic_reciprocity_matrix(n):
    m = n * (n + 1) // 2
    matrix = [[0] * m for _ in range(m)]
    literals = list(range(1, n+1)) + [-i for i in range(1, n+1)]
    for i in range(m):
        for j in range(i, m):
            l1, l2 = literals[i], literals[j]
            if l1 == -l2:
                matrix[i][j] = 0
            else:
                p = abs(l1)
                q = abs(l2)
                if p > q:
                    p, q = q, p
                matrix[i][j] = legendre_symbol(p, q)
    return matrix

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if matrix[i][j] != 0:
                i_max = i
                break
        if i_max == -1:
            continue
        matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
        for i in range(m):
            if i != rank and matrix[i][j] != 0:
                factor = matrix[i][j] / matrix[rank][j]
                for k in range(n):
                    matrix[i][k] -= factor * matrix[rank][k]
        rank += 1
    return rank

def tseitin_resolution_width(matrix):
    m, n = len(matrix), len(matrix[0])
    width = 0
    for i in range(m):
        for j in range(i+1, m):
            if matrix[i][j] != 0:
                width += 1
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * (n - 1) // 2, n * (n + 1) // 2)
    F = [[random.choice([True, False]) for _ in range(m)] for _ in range(n)]
    
    matrix = quadratic_reciprocity_matrix(n)
    rank = gaussian_elimination(matrix)
    width = tseitin_resolution_width(matrix)
    
    primes = generate_primes(n)
    determinants_non_zero = all(legendre_symbol(p, n) != 0 for p in primes if n % p == 0)
    
    return {
        "metric_name": "width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": rank == math.isclose(width, math.sqrt(n) * math.log(n), rel_tol=1e-2) and determinants_non_zero,
        "counterexample": "" if rank == math.isclose(width, math.sqrt(n) * math.log(n), rel_tol=1e-2) and determinants_non_zero else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")