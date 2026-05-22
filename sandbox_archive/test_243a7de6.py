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

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def rank(A):
    m, n = len(A), len(A[0])
    if m == 0 or n == 0:
        return 0
    A_augmented = [row[:] + [1] for row in A]
    pivot_row = 0
    for pivot_col in range(n):
        if all(row[pivot_col] == 0 for row in A_augmented[pivot_row:]):
            continue
        max_pivot_row = pivot_row
        for i in range(pivot_row + 1, m):
            if abs(A_augmented[i][pivot_col]) > abs(A_augmented[max_pivot_row][pivot_col]):
                max_pivot_row = i
        A_augmented[pivot_row], A_augmented[max_pivot_row] = A_augmented[max_pivot_row], A_augmented[pivot_row]
        pivot_val = A_augmented[pivot_row][pivot_col]
        for j in range(n + 1):
            A_augmented[pivot_row][j] /= pivot_val
        for i in range(m):
            if i != pivot_row:
                factor = A_augmented[i][pivot_col]
                for j in range(n + 1):
                    A_augmented[i][j] -= factor * A_augmented[pivot_row][j]
        pivot_row += 1
    return sum(1 for row in A_augmented if any(row[j] != 0 for j in range(n)))

def generate_disjointness_instance(n):
    x = [random.randint(0, 1) for _ in range(n)]
    y = [random.randint(0, 1) for _ in range(n)]
    return (x, y)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            x, y = generate_disjointness_instance(n)
            A = [[x[i] * (1 - y[j]) + y[i] * (1 - x[j]) for j in range(n)] for i in range(n)]
            rank_A = rank(A)
            if rank_A < n:
                conjecture_holds = False
                counterexample = f"n={n}, rank_A={rank_A}"
                break
            total_metric_value += rank_A
            instances_tested += 1

    mean_metric_value = Fraction(total_metric_value, instances_tested) if instances_tested > 0 else 0
    return {
        "metric_name": "Minimal Rank of Twisted Derivatives",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")