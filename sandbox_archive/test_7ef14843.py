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
    m, n = len(A), len(B[0])
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def transpose(A):
    return [list(row) for row in zip(*A)]

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def permanent(A):
    if len(A) == 1:
        return A[0][0]
    perm = 0
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        sign = (-1) ** (len(A) - 1 - i)
        perm += sign * A[0][i] * permanent(submatrix)
    return perm

def schur_coefficient(matrix, partition):
    n = len(matrix)
    if len(partition) != n:
        return 0
    tableaux = []
    def fill_tableau(row, col, path):
        if row == n:
            tableaux.append(path[:])
            return
        for i in range(col + 1):
            if path and path[-1] > partition[row - 1]:
                break
            path.append(i)
            fill_tableau(row + 1, i, path)
            path.pop()
    fill_tableau(0, -1, [])
    sign = 1
    for i in range(n):
        if tableaux[0][i] > partition[i]:
            sign *= -1
    return sign * math.prod(matrix[row][col] for row, col in enumerate(tableaux))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        perm_matrix = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
        det_matrix = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]

        S_n = sum(schur_coefficient(perm_matrix, partition) for partition in partitions(n) if max(partition) <= n**0.5)
        S_prime_n = sum(schur_coefficient(det_matrix, partition) for partition in partitions(n) if max(partition) <= n**0.5)

        metric_value = S_n / S_prime_n
        total_metric_value += metric_value
        instances_tested += 1

        if metric_value <= 2**(n/2):
            conjecture_holds = False
            counterexample = f"n={n}, S_n/S'_n={metric_value}"

    return {
        "metric_name": "Schur Coefficient Sum Ratio",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def partitions(n):
    def extend_partition(partition, start):
        if len(partition) == n:
            yield partition
            return
        for i in range(start, n + 1):
            yield from extend_partition(partition + [i], i)
    return list(extend_partition([], 1))

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")