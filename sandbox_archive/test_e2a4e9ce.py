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
    return abs(a*b) // gcd(a, b)

def fraction_add(f1, f2):
    num = f1[0] * f2[1] + f2[0] * f1[1]
    den = f1[1] * f2[1]
    common_divisor = gcd(num, den)
    return (num // common_divisor, den // common_divisor)

def fraction_sub(f1, f2):
    num = f1[0] * f2[1] - f2[0] * f1[1]
    den = f1[1] * f2[1]
    common_divisor = gcd(num, den)
    return (num // common_divisor, den // common_divisor)

def fraction_mul(f1, f2):
    num = f1[0] * f2[0]
    den = f1[1] * f2[1]
    common_divisor = gcd(num, den)
    return (num // common_divisor, den // common_divisor)

def fraction_div(f1, f2):
    if f2[0] == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    num = f1[0] * f2[1]
    den = f1[1] * f2[0]
    common_divisor = gcd(num, den)
    return (num // common_divisor, den // common_divisor)

def fraction_to_float(f):
    return f[0] / f[1]

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result

def fraction_matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")

    result = [[(0, 1) for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] = fraction_add(result[i][j], fraction_mul(A[i][k], B[k][j]))

    return result

def gaussian_elimination(M, b):
    rows = len(M)
    cols = len(M[0])

    # Augmented matrix
    aug_matrix = [row + [b[i]] for i, row in enumerate(M)]

    for j in range(cols):
        max_row = None
        for i in range(j, rows):
            if max_row is None or abs(aug_matrix[i][j]) > abs(aug_matrix[max_row][j]):
                max_row = i

        # Swap current row with the max row
        aug_matrix[j], aug_matrix[max_row] = aug_matrix[max_row], aug_matrix[j]

        # Make the diagonal element 1
        pivot = aug_matrix[j][j]
        for k in range(cols + 1):
            aug_matrix[j][k] = fraction_div(aug_matrix[j][k], (pivot, 1))

        # Eliminate the column below the pivot
        for i in range(j + 1, rows):
            factor = aug_matrix[i][j]
            for k in range(cols + 1):
                aug_matrix[i][k] = fraction_sub(aug_matrix[i][k], fraction_mul((factor, 1), aug_matrix[j][k]))

    # Back substitution
    x = [0] * cols
    for i in range(cols - 1, -1, -1):
        x[i] = aug_matrix[i][-1]
        for j in range(i + 1, cols):
            x[i] = fraction_sub(x[i], fraction_mul((aug_matrix[i][j], 1), x[j]))
        if aug_matrix[i][i] == (0, 1):
            raise ValueError("No unique solution exists")

    return x

def build_ABP(N, w, d, prime):
    M = [[[random.randint(-prime // 2, prime // 2) for _ in range(d + 1)] for _ in range(w)] for _ in range(w)]
    f = [[M[i][j][k] * M[(i + j) % w][k][l] for k in range(d + 1)] for j in range(w) for l in range(2)]
    return f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    N_values = [8, 10, 12, 14]
    w_values = [2, 3]
    d_values = [3, 4]

    results = []
    for N in N_values:
        for w in w_values:
            for d in d_values:
                f = build_ABP(N, w, d, 2**30 - 1)
                T = [[(0, 1) for _ in range(N * (N + 1) // 2)] for _ in range(N * N)]
                monomials = [(i, j) for i in range(N) for j in range(N)]
                for A in f:
                    for (i, j), coeff in zip(monomials, A):
                        T[i][j] = fraction_add(T[i][j], fraction_mul(coeff, (1, 1)))

                rank_T = len(gaussian_elimination(T, [0] * (N * N)))
                sigma_f = N * N - rank_T
                results.append({
                    "metric_name": "sigma_f",
                    "metric_value": sigma_f,
                    "instances_tested": 1,
                    "conjecture_holds": sigma_f >= N - 2 * w ** 2,
                    "counterexample": "" if sigma_f >= N - 2 * w ** 2 else f"ABP width {w} too small"
                })

    return {
        "metric_name": "sigma_f",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")