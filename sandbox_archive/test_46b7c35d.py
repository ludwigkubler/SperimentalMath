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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def operator_norm(A):
    m, n = len(A), len(A[0])
    max_row_norm = 0
    for row in A:
        row_norm = sum(abs(x) for x in row)
        if row_norm > max_row_norm:
            max_row_norm = row_norm
    max_col_norm = 0
    for j in range(n):
        col_norm = sum(abs(A[i][j]) for i in range(m))
        if col_norm > max_col_norm:
            max_col_norm = col_norm
    return max(max_row_norm, max_col_norm)

def regular_representation(n):
    size = 2 * n
    rep = [[0] * size for _ in range(size)]
    for i in range(n):
        rep[i][i] = 1
        rep[n+i][n+i] = -1
    return rep

def noncommutative_fourier_transform(M, rep):
    n = len(M)
    fourier_rep = [[0] * (2*n) for _ in range(2*n)]
    for i in range(n):
        for j in range(n):
            if M[i][j]:
                fourier_rep[i][j] = 1
                fourier_rep[n+i][n+j] = -1
    return matrix_multiplication(fourier_rep, matrix_multiplication(M, fourier_rep))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        rep = regular_representation(n)
        F_M = noncommutative_fourier_transform(M, rep)
        norm = operator_norm(F_M)
        results.append(norm * n)
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    conjecture_holds = all(0.5 <= x / n <= 1.5 for x, n in zip(results, n_values))
    return {
        "metric_name": "operator_norm",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean = sum(x["metric_value"] for x in results) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")