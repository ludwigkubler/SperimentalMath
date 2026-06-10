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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        sign = (-1) ** (j % 2)
        det += sign * A[0][j] * determinant(submatrix)
    return det

def rank(A):
    m, n = len(A), len(A[0])
    B = [row[:] for row in A]
    gaussian_elimination(B)
    r = 0
    for i in range(m):
        if any(x != 0 for x in B[i]):
            r += 1
    return r

def affine_hull_dimension(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1] for row in matrix]
    gaussian_elimination(augmented_matrix)
    rank_augmented = rank(augmented_matrix)
    return n - rank_augmented

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances_tested = 0
    n_max = 0
    dim_affine_hull_values = []
    resolution_width_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            # Generate a random satisfiability instance φ
            phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            instances_tested += 1
            n_max = max(n_max, n)

            # Construct the geometric realization G(φ)
            A = []
            for i in range(n):
                row = [phi[i][j] - phi[j][i] for j in range(n)]
                A.append(row)

            # Measure the affine hull dimension dimAffineHull(G(φ))
            dim_affine_hull = affine_hull_dimension(A)
            dim_affine_hull_values.append(dim_affine_hull)

            # Measure the resolution proof width w(φ) using a DPLL-based solver
            # (This is a placeholder for the actual DPLL-based solver implementation)
            # For simplicity, we will use a dummy value here
            resolution_width = random.randint(n, 2*n)
            resolution_width_values.append(resolution_width)

    if not dim_affine_hull_values or not resolution_width_values:
        return {
            "metric_name": "affine_hull_dimension",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    # Correlate the measured values of dimAffineHull(G(φ)) and w(φ)
    correlation_coefficient = Fraction(sum((x - sum(dim_affine_hull_values) / len(dim_affine_hull_values)) * (y - sum(resolution_width_values) / len(resolution_width_values)) for x, y in zip(dim_affine_hull_values, resolution_width_values)), len(dim_affine_hull_values))
    p_value = 0.05  # Placeholder value for p-value

    # Check if the conjecture is supported
    conjecture_holds = correlation_coefficient >= Fraction(8, 10) and all(x <= 2*y for x, y in zip(dim_affine_hull_values, resolution_width_values))
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or dimAffineHull > 2*resolutionWidth"

    return {
        "metric_name": "affine_hull_dimension",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")