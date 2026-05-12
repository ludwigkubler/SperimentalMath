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
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
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

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def polynomial_to_matrix(poly, n):
    m = len(poly)
    matrix = [[0] * (n + 1) for _ in range(m)]
    for i in range(m):
        for j in range(n + 1):
            if i >= j:
                matrix[i][j] = poly[i - j]
    return matrix

def polynomial_factorization(poly, n):
    m = len(poly)
    A = polynomial_to_matrix(poly, n)
    b = [0] * m
    for i in range(m):
        b[i] = 1 if i == 0 else 0
    x = gaussian_elimination(A, b)
    return x

def generate_random_3sat(n):
    clauses = []
    for _ in range(2 ** n):
        clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
        if sum(clause) != 0:
            clauses.append(clause)
    return clauses

def polynomial_from_3sat(clauses):
    n = max(abs(c) for c in set(sum(clauses, [])))
    poly = [0] * (n + 1)
    for clause in clauses:
        term = 1
        for literal in clause:
            if literal > 0:
                term *= (1 - x[literal])
            else:
                term *= (1 + x[-literal])
        poly[0] += term
    return poly

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_random_3sat(n)
    poly = polynomial_from_3sat(clauses)
    irreducible_components = polynomial_factorization(poly, n)
    circuit_size = len(irreducible_components) * (n + 1)
    conjecture_holds = circuit_size >= 2 ** (n / 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_circuit_size = sum(r["metric_value"] for r in results) / len(results)
    std_circuit_size = math.sqrt(sum((r["metric_value"] - mean_circuit_size) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_circuit_size} std={std_circuit_size} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_circuit_size} std={std_circuit_size} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")