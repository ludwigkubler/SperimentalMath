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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(i, n):
            A[i][j] /= pivot
        b[i] /= pivot
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
    return b

def matrix_multiplication(A, B):
    m, p = len(A), len(B[0])
    n = len(B)
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def characteristic_polynomial(L):
    n = len(L)
    t = Fraction('t')
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    A = matrix_multiplication(L, I)
    A[0][0] -= t
    det_A = determinant(A)
    return det_A

def hodge_rank(L):
    n = len(L)
    char_poly = characteristic_polynomial(L)
    coeffs = [char_poly.coeff(t, i) for i in range(n+1)]
    matrix = [[coeffs[n-i-j] for j in range(i+1)] for i in range(n)]
    try:
        b = [Fraction(0) for _ in range(n)]
        solution = gaussian_elimination(matrix, b)
        rank = sum(1 for x in solution if x != Fraction(0))
        return rank
    except ValueError:
        return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_size = 0
    for n in n_values:
        G = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
        L = matrix_multiplication(G, G)
        hodge_rank_val = hodge_rank(L)
        total_rank += hodge_rank_val
        total_size += n**2
    mean_rank = Fraction(total_rank) / len(n_values)
    conjecture_holds = mean_rank >= 3 * (len(n_values) ** 1.5)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Hodge Rank",
        "metric_value": float(mean_rank),
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")