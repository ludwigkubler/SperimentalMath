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

def matrix_mul(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    m, n = len(A), len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for c in range(len(matrix)):
        submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        sign = (-1) ** (c % 2)
        sub_det = determinant(submatrix)
        det += sign * matrix[0][c] * sub_det
    return det

def inverse(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    n = len(matrix)
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            sign = (-1) ** (i + j)
            adjugate[j][i] = sign * determinant(submatrix)
    return matrix_mul(adjugate, [[1 / det] * n for _ in range(n)])

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def norm(v):
    return sum(x**2 for x in v) ** 0.5

def convex_hull(points):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def distance(p, q):
        return norm([p[0] - q[0], p[1] - q[1]])

    points = sorted(points)
    lower = []
    for p in points:
        while len(lower) >= 2 and orientation(lower[-2], lower[-1], p) != 2:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and orientation(upper[-2], upper[-1], p) != 2:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def covering_radius(n):
    # Approximate using a randomized sampling method
    points = [[random.randint(-n, n) for _ in range(n)] for _ in range(100)]
    hull = convex_hull(points)
    radius = max(distance(p, q) for p in hull for q in hull)
    return radius

def discrepancy(S):
    n = len(S[0])
    char_vectors = [[1 if i in S[j] else 0 for j in range(len(S))] for i in range(n)]
    A = matrix_mul(char_vectors, char_vectors)
    inv_A = inverse(A)
    B = [[sum(1 for s in S if i in s) - len(S) / 2 for i in range(n)]]
    D = matrix_mul(inv_A, B)
    return norm(D[0])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    S = [set(random.sample(range(n), random.randint(1, n))) for _ in range(100)]
    disc_S = discrepancy(S)
    Z_n_radius = covering_radius(n)
    scaled_radius = Z_n_radius * (n ** (n / 2))
    return {
        "metric_name": "discrepancy_bound",
        "metric_value": disc_S,
        "instances_tested": len(S),
        "conjecture_holds": disc_S <= scaled_radius,
        "counterexample": "" if disc_S <= scaled_radius else f"discrepancy={disc_S}, scaled_radius={scaled_radius}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")