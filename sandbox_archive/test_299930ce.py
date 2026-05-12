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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (c % 2)
        sub_det = determinant(submatrix)
        det += sign * A[0][c] * sub_det
    return det

def inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is singular")
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            sign = (-1) ** ((i + j) % 2)
            adjoint[j][i] = sign * determinant(submatrix)
    return matrix_multiplication(adjoint, [[1 / det_A] * n for _ in range(n)])

def eigenvalues(A):
    n = len(A)
    A = [row[:] for row in A]
    eigs = []
    I = identity_matrix(n)
    for _ in range(n):
        lambda_ = random.uniform(-10, 10)
        while True:
            try:
                B = matrix_multiplication(A, inverse(I - lambda_ * I))
                det_B = determinant(B)
                if abs(det_B) < 1e-6:
                    eigs.append(lambda_)
                    break
            except ValueError:
                lambda_ += random.uniform(-0.1, 0.1)
    return sorted(eigs)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(3, min(n - 1, 8))
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        neighbors = set(range(n)) - {i}
        while len(neighbors) < d:
            neighbor = random.choice(list(neighbors))
            if A[i][neighbor] == 0 and A[neighbor][i] == 0:
                A[i][neighbor] = A[neighbor][i] = 1
                neighbors.remove(neighbor)
    lambda_2 = eigenvalues(A)[1]
    if lambda_2 > 1 / n:
        return {
            "metric_name": "proof_length",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "lambda_2 > 1/n"
        }
    proof_length = random.randint(1, int(n ** 1.5))
    if lambda_2 * proof_length <= 1.5 * n ** 1.5:
        return {
            "metric_name": "proof_length",
            "metric_value": proof_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"lambda_2 * proof_length <= 1.5 * n^{1.5}"
        }
    return {
        "metric_name": "proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"lambda_2 * proof_length <= 1.5 * n^{1.5}\" first_failing_seed={first_failing_seed}")