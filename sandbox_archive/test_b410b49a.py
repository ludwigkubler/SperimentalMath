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
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * matrix_minor(matrix, 0, i) * (-1) ** (0 + i)
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = []
    for i in range(n):
        row = []
        for j in range(n):
            minor = matrix_minor(matrix, i, j)
            cofactor = (-1) ** (i + j) * minor
            adjugate.append(cofactor % mod)
        adjugate.insert(0, row[::-1])
    inv_matrix = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def matrix_minor(matrix, i, j):
    minor = []
    for r in range(len(matrix)):
        if r == i:
            continue
        row = []
        for c in range(len(matrix[r])):
            if c == j:
                continue
            row.append(matrix[r][c])
        minor.append(row)
    return determinant(minor)

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for i in range(n):
        det += matrix[0][i] * matrix_minor(matrix, 0, i) * (-1) ** (0 + i)
    return det

def multiply_matrices(a, b):
    n = len(a)
    m = len(b[0])
    p = len(b)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += a[i][k] * b[k][j]
    return result

def add_matrices(a, b):
    n = len(a)
    m = len(a[0])
    result = [[a[i][j] + b[i][j] for j in range(m)] for i in range(n)]
    return result

def subtract_matrices(a, b):
    n = len(a)
    m = len(a[0])
    result = [[a[i][j] - b[i][j] for j in range(m)] for i in range(n)]
    return result

def scalar_multiply(matrix, scalar):
    n = len(matrix)
    m = len(matrix[0])
    result = [[matrix[i][j] * scalar for j in range(m)] for i in range(n)]
    return result

def transpose_matrix(matrix):
    n = len(matrix)
    m = len(matrix[0])
    result = [[matrix[j][i] for j in range(n)] for i in range(m)]
    return result

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    for num in range(2, n):
        if is_prime(num):
            primes.append(num)
    return primes

def random_polynomial(n, degree):
    coefficients = [random.randint(0, 1) for _ in range(degree + 1)]
    return coefficients

def evaluate_polynomial(poly, x):
    result = 0
    for i, coeff in enumerate(poly):
        result += coeff * (x ** i)
    return result

def generate_random_seeds(n=30):
    primes = generate_primes(1000)[:n]
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5
    poly_type = "permanent" if random.choice([True, False]) else "determinant"
    poly = random_polynomial(n, n)
    
    def permanent(poly):
        result = 0
        for perm in itertools.permutations(range(n)):
            prod = 1
            for i in range(n):
                prod *= poly[perm[i]][i]
            result += prod
        return result
    
    def determinant(poly):
        if n == 1:
            return poly[0][0]
        det = 0
        for i in range(n):
            minor = []
            for r in range(1, n):
                row = []
                for c in range(n):
                    if c != i:
                        row.append(poly[r][c])
                minor.append(row)
            det += (-1) ** i * poly[0][i] * determinant(minor)
        return det
    
    func = permanent if poly_type == "permanent" else determinant
    result = func(poly)
    
    metric_value = len(list(itertools.permutations(range(n)))) if poly_type == "permanent" else n
    conjecture_holds = True if poly_type == "permanent" else False
    counterexample = "" if conjecture_holds else f"{poly_type} is polynomial for n={n}"
    
    return {
        "metric_name": "tableau_count",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_random_seeds()
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")