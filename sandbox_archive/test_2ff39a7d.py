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

def generate_primes(count=30):
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

def generate_disjointness_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                matrix[i][j] = 1
                matrix[j][i] = 1
    return matrix

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def matrix_scale(A, c):
    n = len(A)
    B = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            B[i][j] = c * A[i][j]
    return B

def gaussian_elimination(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        I[i], I[max_row] = I[max_row], I[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                    I[j][k] -= factor * I[i][k]
    return I

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def inverse(A):
    n = len(A)
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is singular")
    I = gaussian_elimination(A)
    return I

def character_table(n):
    table = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        table[i][i + 1] = 1
    for k in range(2, n + 1):
        for j in range(k - 1, -1, -1):
            sum_val = 0
            for l in range(j, k):
                sum_val += (-1) ** (l - j) * binomial_coefficient(l, j) * character_table(n - k, l)
            table[j][k] = sum_val / k
    return table

def binomial_coefficient(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def fourier_coefficient(M, lambda_partition):
    n = len(M)
    character_values = [1]
    for k in lambda_partition:
        char_table = character_table(n)
        value = 0
        for i in range(n):
            product = 1
            for j in range(k):
                product *= M[i][j]
            value += product * char_table[i][k + 1]
        character_values.append(value / n ** k)
    return sum(character_values)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = generate_disjointness_matrix(n)
    lambda_1 = (n - 1, 1)
    lambda_n = (n,)
    chi_lambda_1 = fourier_coefficient(M, lambda_1)
    chi_lambda_n = fourier_coefficient(M, lambda_n)
    metric_value = max(abs(chi_lambda_1), abs(chi_lambda_n))
    conjecture_holds = abs(chi_lambda_1) >= n**2 / 2 and abs(chi_lambda_n) <= n / 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Fourier Coefficient Gap",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes()
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")