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

def generate_symmetric_matrix(n):
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            A[i][j] = random.randint(-10, 10)
            A[j][i] = A[i][j]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(A):
    n = len(A)
    T = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            T[j][i] = A[i][j]
    return T

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (1 + c)
        sub_det = determinant(submatrix)
        det += sign * A[0][c] * sub_det
    return det

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def eigenvalues(A):
    n = len(A)
    eigenvals = []
    B = [row[:] for row in A]
    while True:
        gaussian_elimination(B)
        diag_sum = sum(B[i][i] for i in range(n))
        if abs(diag_sum - sum(eigenvals)) < 1e-6:
            break
        eigenvals.append(diag_sum)
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                B[i][j] = A[i][j]
    return eigenvals

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    A = generate_symmetric_matrix(n)
    eigs = eigenvalues(A)
    lambda_min = min(eig for eig in eigs if eig != 0)
    
    # Placeholder for quantum communication complexity calculation
    CC_XOR_n = 2**n / lambda_min
    
    B = [row[:] for row in A]
    for i in range(n):
        for j in range(i, n):
            B[i][j] /= math.sqrt(lambda_min)
            B[j][i] = B[i][j]
    
    # Placeholder for verifying eigenvalues of B
    eigs_B = eigenvalues(B)
    if any(abs(eig) > 1 for eig in eigs_B):
        return {
            "metric_name": "minimal_non_zero_eigenvalue",
            "metric_value": lambda_min,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "eigenvalues_of_B_not_distinct_or_outside_unit_circle"
        }
    
    return {
        "metric_name": "minimal_non_zero_eigenvalue",
        "metric_value": lambda_min,
        "instances_tested": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"eigenvalues_of_B_not_distinct_or_outside_unit_circle\" first_failing_seed={first_failing_seed}")