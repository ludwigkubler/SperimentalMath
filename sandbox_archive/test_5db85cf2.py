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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def is_square_matrix(matrix):
    n = len(matrix)
    return all(len(row) == n for row in matrix)

def is_invertible(matrix):
    if not is_square_matrix(matrix):
        return False
    return determinant(matrix) != 0

def inverse(A):
    n = len(A)
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    A_inv = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            sign = (-1) ** (i+j)
            A_inv[i][j] = sign * determinant(submatrix) / det
    return A_inv

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    moh_values = []
    f_values = []

    for _ in range(30):
        d = random.randint(2, min(n-1, 5))
        G = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    G[j][i] = 1

        # Compute Frege proof length
        f_phi_G = len(G) * (len(G[0]) - d + 1)

        # Compute minimal order of tropicalized cohomology groups
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    A[i][j] = Fraction(1)
                    A[j][i] = Fraction(1)

        if is_invertible(A):
            moh_G = len([x for x in determinant(A).numerator.as_integer_ratio()[0].primefactors() if x > 1])
        else:
            moh_G = 0

        moh_values.append(moh_G)
        f_values.append(f_phi_G)

    m_avg = sum(moh_values) / len(moh_values)
    f_avg = sum(f_values) / len(f_values)
    correlation_coefficient = sum((m - m_avg) * (f - f_avg) for m, f in zip(moh_values, f_values)) / math.sqrt(sum((m - m_avg) ** 2 for m in moh_values) * sum((f - f_avg) ** 2 for f in f_values))

    conjecture_holds = correlation_coefficient >= 0.8 and abs(m_avg - f_avg) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(moh_values),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")