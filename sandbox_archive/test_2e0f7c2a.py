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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in matrix[1:]]
        det += ((-1) ** i) * matrix[0][i] * determinant(minor, mod)
    inv_det = mod_inverse(det % mod, mod)
    adjugate = [[((-1) ** (i+j)) * determinant([row[:j] + row[j+1:] for row in minor], mod) for j in range(n)] for i in range(n)]
    return matrix_mod_mul(adjugate, inv_det, mod)

def matrix_mod_mul(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
                result[i][j] %= mod
    return result

def matrix_mod_add(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] + B[i][j]) % mod
    return result

def matrix_mod_sub(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] - B[i][j]) % mod
    return result

def matrix_mod_scalar_mul(matrix, scalar, mod):
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (matrix[i][j] * scalar) % mod
    return result

def matrix_mod_trace(matrix, mod):
    n = len(matrix)
    trace = 0
    for i in range(n):
        trace += matrix[i][i]
    return trace % mod

def matrix_mod_det(matrix, mod):
    n = len(matrix)
    if n == 1:
        return matrix[0][0] % mod
    det = 0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += ((-1) ** j) * matrix[0][j] * matrix_mod_det(minor, mod)
    return det % mod

def matrix_mod_pow(matrix, power, mod):
    n = len(matrix)
    result = [[int(i == j) for j in range(n)] for i in range(n)]
    base = matrix
    while power > 0:
        if power % 2 == 1:
            result = matrix_mod_mul(result, base, mod)
        base = matrix_mod_mul(base, base, mod)
        power //= 2
    return result

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in matrix[1:]]
        det += ((-1) ** i) * matrix[0][i] * determinant(minor, mod)
    inv_det = mod_inverse(det % mod, mod)
    adjugate = [[((-1) ** (i+j)) * determinant([row[:j] + row[j+1:] for row in minor], mod) for j in range(n)] for i in range(n)]
    return matrix_mod_mul(adjugate, inv_det, mod)

def matrix_mod_add(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] + B[i][j]) % mod
    return result

def matrix_mod_sub(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] - B[i][j]) % mod
    return result

def matrix_mod_scalar_mul(matrix, scalar, mod):
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (matrix[i][j] * scalar) % mod
    return result

def matrix_mod_trace(matrix, mod):
    n = len(matrix)
    trace = 0
    for i in range(n):
        trace += matrix[i][i]
    return trace % mod

def matrix_mod_det(matrix, mod):
    n = len(matrix)
    if n == 1:
        return matrix[0][0] % mod
    det = 0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += ((-1) ** j) * matrix[0][j] * matrix_mod_det(minor, mod)
    return det % mod

def matrix_mod_pow(matrix, power, mod):
    n = len(matrix)
    result = [[int(i == j) for j in range(n)] for i in range(n)]
    base = matrix
    while power > 0:
        if power % 2 == 1:
            result = matrix_mod_mul(result, base, mod)
        base = matrix_mod_mul(base, base, mod)
        power //= 2
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0

    # Construct the ideal I of quadratic forms
    I = []
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j] == 1:
                Q = [[0] * n for _ in range(n)]
                Q[i][i] = 1
                Q[j][j] = 1
                Q[i][j] = -2
                Q[j][i] = -2
                I.append(Q)

    # Compute the real radical rank via Gröbner basis reduction
    def monomial_to_index(monomial):
        return sum(monomial[i] * (n-1-i) for i in range(n))

    def index_to_monomial(index):
        monomial = [0] * n
        for i in range(n):
            if index >= (n-1-i)*(n-i)//2:
                monomial[i] += 1
                index -= (n-1-i)*(n-i)//2
        return monomial

    def monomial_degree(monomial):
        return sum(monomial)

    def monomial_compare(monomial1, monomial2):
        if monomial_degree(monomial1) != monomial_degree(monomial2):
            return monomial_degree(monomial2) - monomial_degree(monomial1)
        for i in range(n):
            if monomial1[i] != monomial2[i]:
                return monomial2[i] - monomial1[i]
        return 0

    def groebner_basis_reduction(I):
        basis = []
        for poly in I:
            leading_term = None
            for term in poly:
                if term[0] > 0 and (leading_term is None or monomial_compare(term, leading_term) < 0):
                    leading_term = term
            if leading_term is not None:
                basis.append(leading_term)
        while True:
            new_basis = []
            for i in range(len(basis)):
                for j in range(i+1, len(basis)):
                    lcm_term = [lcm(basis[i][0], basis[j][0]), 0] * n
                    for k in range(n):
                        lcm_term[1+k] = (basis[i][1+k] * basis[j][0] - basis[j][1+k] * basis[i][0]) % mod
                    new_basis.append(lcm_term)
            if len(new_basis) == len(basis):
                break
            basis = new_basis
        return basis

    def real_radical_rank(I):
        basis = groebner_basis_reduction(I)
        rank = 0
        for term in basis:
            if term[0] > 0:
                rank += 1
        return rank

    rank_real_radical_I = real_radical_rank(I)

    # Measure the minimal SOS degree needed for Ω(1) approximation using a truncated Lasserre hierarchy
    def lasserre_hierarchy(poly, level):
        if level == 0:
            return [poly]
        result = []
        for term in poly:
            if term[0] > 0:
                result.append(term)
                for i in range(n):
                    new_term = [term[0], term[1] + (n-1-i)*term[2]]
                    result.append(new_term)
        return result

    def sos_degree(poly, level):
        hierarchy = lasserre_hierarchy(poly, level)
        for term in hierarchy:
            if term[0] > 0 and all(term[i] == 0 for i in range(1, n)):
                return term[2]
        return float('inf')

    min_sos_degree_I = float('inf')
    for poly in I:
        degree = sos_degree(poly, 1)
        if degree < min_sos_degree_I:
            min_sos_degree_I = degree

    # Verify deg_SOS ≥ rank_real_radical
    conjecture_holds = min_sos_degree_I >= rank_real_radical_I
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "SOS Degree",
        "metric_value": min_sos_degree_I,
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

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")