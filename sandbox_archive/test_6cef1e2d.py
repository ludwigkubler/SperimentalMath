# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mul(A, B):
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

def matrix_sub(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C

def matrix_det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * matrix_det(submatrix)
        return det

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    augmented_matrix = [row + [0] for row in matrix]
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(augmented_matrix[k][i]) > abs(augmented_matrix[max_row][i]):
                max_row = k
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        for j in range(m):
            augmented_matrix[i][j] /= augmented_matrix[i][i]
        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                augmented_matrix[k] = [augmented_matrix[k][j] - factor * augmented_matrix[i][j] for j in range(m)]
    rank = sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(m)))
    return rank

def degree_of_smallest_xor_tautology(poly):
    n = len(poly)
    max_degree = 0
    for i in range(n):
        for j in range(i+1, n):
            if poly[i] == poly[j]:
                continue
            degree = 0
            while (i + degree) % n != j:
                degree += 1
            max_degree = max(max_degree, degree)
    return max_degree

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    poly = [random.choice([0, 1]) for _ in range(n)]
    rho_f = rank([[poly[i] for i in range(j, j+degree_of_smallest_xor_tautology(poly)+1)] for j in range(n)])
    degree_tautology = degree_of_smallest_xor_tautology(poly)
    return {
        "metric_name": "rank",
        "metric_value": rho_f,
        "instances_tested": 1,
        "conjecture_holds": rho_f >= degree_tautology,
        "counterexample": "" if rho_f >= degree_tautology else f"rho(f)={rho_f}, degree of tautology={degree_tautology}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*31, 2))  # Default to first 30 primes
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")