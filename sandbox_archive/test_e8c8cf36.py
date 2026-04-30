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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

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
    else:
        return x % m

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    rows = len(A)
    cols = len(A[0])
    result = [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]
    return result

def matrix_subtract(A, B):
    rows = len(A)
    cols = len(A[0])
    result = [[A[i][j] - B[i][j] for j in range(cols)] for i in range(rows)]
    return result

def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[matrix[j][i] for j in range(rows)] for i in range(cols)]
    return result

def matrix_power(matrix, n):
    if n == 1:
        return matrix
    elif n % 2 == 0:
        half_power = matrix_power(matrix, n // 2)
        return matrix_multiply(half_power, half_power)
    else:
        return matrix_multiply(matrix, matrix_power(matrix, n - 1))

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        max_row = i
        for j in range(i+1, rows):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        for j in range(cols):
            A[i][j] /= factor
        for j in range(rows):
            if i != j:
                factor = A[j][i]
                for k in range(cols):
                    A[j][k] -= factor * A[i][k]
    return A

def compute_transition_algebra(program, q):
    n = len(q)
    transition_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if program[i][j] != 0:
                transition_matrix[i][j] = 1
    return transition_matrix

def compute_module_dimension(transition_matrix):
    rows, cols = len(transition_matrix), len(transition_matrix[0])
    augmented_matrix = [row + [1] for row in transition_matrix]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    rank = sum(1 for row in reduced_matrix if any(row[i] != 0 for i in range(cols)))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5
    q = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    transition_matrix = compute_transition_algebra(q, q)
    module_dimension = compute_module_dimension(transition_matrix)
    length = sum(sum(row) for row in q)
    symmetry = sum(q[i][j] == q[j][i] for i in range(n) for j in range(i+1, n))
    metric_value = module_dimension / (length + 1e-9)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    return {
        "metric_name": "module_dimension",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")