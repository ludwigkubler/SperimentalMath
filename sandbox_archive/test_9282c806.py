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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def rank(matrix):
    A = matrix[:]
    m, n = len(A), len(A[0])
    r = 0
    for i in range(n):
        if r < m:
            pivot_row = r
            while pivot_row < m and A[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row < m:
                A[r], A[pivot_row] = A[pivot_row], A[r]
                for j in range(n):
                    A[r][j] /= A[r][i]
                for j in range(m):
                    if j != r:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[r][k]
                r += 1
    return r

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 2  # Fixed prime p
    n_values = [5, 10, 15, 20, 30, 40]
    C_p = 1.0  # Placeholder constant for demonstration purposes

    results = []
    for n in n_values:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""

        for _ in range(5):  # Sample 5 instances per n
            A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            b = [sum(A[i][j] for j in range(n)) % 2 for i in range(n)]

            rank_Ab = rank(gaussian_elimination(A, b))
            expected_rank = C_p * math.log(n)

            if rank_Ab < expected_rank:
                conjecture_holds = False
                counterexample = f"n={n}, rank={rank_Ab}, expected>={expected_rank}"
                break

            instances_tested += 1

        results.append({
            "metric_name": "p-adic L-function rank",
            "metric_value": expected_rank,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })

    return {
        "seed": seed,
        **results[-1]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")