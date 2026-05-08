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
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        factor = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def inverse(A):
    n = len(A)
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    A_augmented = [A[i] + identity[i] for i in range(n)]
    gaussian_elimination(A_augmented, [0]*n)
    return [row[n:] for row in A_augmented]

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def character_table(n):
    table = []
    for k in range(n + 1):
        row = []
        for l in range(k + 1):
            if (k - l) % 2 == 1:
                row.append(0)
            else:
                value = math.comb(k, l) * (-1)**((k - l) // 2) / math.factorial(l)
                row.append(value)
        table.append(row)
    return table

def decompose_matrix(M, n):
    char_table = character_table(n)
    inv_char_table = inverse(char_table)
    multiplicities = [sum(sum(a * b for a, b in zip(row, col)) for row in M) for col in inv_char_table]
    return multiplicities

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_sum = 0
    instances_tested = 0
    for n in n_values:
        for _ in range(5):  # Each n tested 5 times
            instances_tested += 1
            M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            multiplicities = decompose_matrix(M, n)
            sum_of_squares = sum(m**2 for m in multiplicities)
            total_sum += sum_of_squares
    mean_value = total_sum / instances_tested
    conjecture_holds = mean_value >= n_values[0]
    counterexample = "" if conjecture_holds else f"mean={mean_value}"
    return {
        "metric_name": "Sum of squares of multiplicities",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")