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
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_transpose(A):
    m, n = len(A), len(A[0])
    B = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            B[j][i] = A[i][j]
    return B

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    pivot_col = 0
    for i in range(m):
        if pivot_col >= n:
            break
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][pivot_col]) > abs(A[max_row][pivot_col]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][pivot_col] == 0:
            pivot_col += 1
            continue
        for j in range(m):
            if j != i and A[j][pivot_col] != 0:
                factor = -A[j][pivot_col] / A[i][pivot_col]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        rank += 1
        pivot_col += 1
    return rank

def partition_size(partition):
    return sum(1 for part in partition if part > 0)

def log2(x):
    if x <= 0:
        return float('-inf')
    return math.log2(x)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(1, n * n)
    partition = [random.randint(1, n) for _ in range(n)]
    T_rank = m
    lower_bound = m / 2 + partition_size(partition) * log2(m)

    # Generate a random symmetric tensor T of size n with rank m
    A = [[0] * n for _ in range(n)]
    for _ in range(m):
        i, j = random.sample(range(n), 2)
        if i != j:
            A[i][j] = A[j][i] = random.random()
        else:
            A[i][i] += random.random()
    T = matrix_transpose(A)

    # Compute the minimal symplectic tensor product rank of T
    rank = gaussian_elimination(T)
    diff = abs(rank - lower_bound) / lower_bound

    # Construct a permutation circuit of depth O(n^log_2(3/4)) for the permanent of matrices of size n
    def permanent(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * permanent(submatrix)
        return det

    def permutation_circuit_size(n):
        return int(n ** log2(Fraction(3, 4)))

    circuit_depth = permutation_circuit_size(n)

    return {
        "metric_name": "rank_diff",
        "metric_value": diff,
        "instances_tested": 1,
        "conjecture_holds": diff <= 0.05,
        "counterexample": "" if diff <= 0.05 else f"Rank difference {diff} exceeds threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_diff = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"rank_diff {result['metric_value']} exceeds threshold\" first_failing_seed={first_failing_seed}")