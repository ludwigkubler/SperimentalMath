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

def matrix_mul(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]
    return result

def transpose(matrix):
    return [list(col) for col in zip(*matrix)]

def polyfit(x, y, degree):
    n = len(x)
    X = [[x[i]**j for j in range(degree + 1)] for i in range(n)]
    Y = y
    A = matrix_mul(transpose(X), X)
    B = matrix_mul(transpose(X), Y)
    coefficients = [Fraction(b, a) for a, b in zip(*gaussian_elimination(A, B))]
    return coefficients

def gaussian_elimination(A, B):
    n = len(B)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        B[i], B[max_row] = B[max_row], B[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            B[j] -= factor * B[i]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            B[i] -= A[i][j] * B[j]
        B[i] /= A[i][i]
    return [b for b in B]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    msqr_values = []
    rv_values = []

    for n in n_values:
        # Generate a random instance of communication complexity φ
        φ = [random.randint(1, 100) for _ in range(n)]
        rank_variance = sum((x - sum(φ) / n)**2 for x in φ) / n
        rv_values.append(rank_variance)

        # Compute the minimal symplectic quotient rank msqr(φ)
        msqr = len(set(φ))
        msqr_values.append(msqr)

    if not msqr_values or not rv_values:
        return {
            "metric_name": "msqr_vs_rv",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_instance"
        }

    coefficients = polyfit(rv_values, msqr_values, 1)
    slope = coefficients[0]
    intercept = coefficients[1]

    # Check if the relationship is Θ(RV(φ))
    mean_rv = sum(rv_values) / len(rv_values)
    predicted_msqr = slope * mean_rv + intercept
    actual_msqr = sum(msqr_values) / len(msqr_values)

    correlation_coefficient = (n_values[1] * sum(x*y for x, y in zip(rv_values, msqr_values)) -
                                sum(rv_values) * sum(msqr_values)) / \
                               math.sqrt((n_values[1] * sum(x**2 for x in rv_values) - sum(rv_values)**2) *
                                         (n_values[1] * sum(x**2 for x in msqr_values) - sum(msqr_values)**2))

    return {
        "metric_name": "msqr_vs_rv",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")