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
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = -A[k][i]
                for j in range(n):
                    A[k][j] += factor * A[i][j]

def matrix_determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        sign = (-1) ** j
        det += sign * A[0][j] * matrix_determinant(submatrix)
    return det

def frobenius_schur_indicator(matrix):
    n = len(matrix)
    trace = sum(matrix[i][i] for i in range(n))
    det = matrix_determinant(matrix)
    if det == 0:
        return 0
    return (trace * det) / (n * det**2)

def frege_proof_depth(formula):
    # Placeholder function to simulate Frege proof depth calculation
    # This is a dummy implementation and should be replaced with an actual algorithm
    return random.randint(1, 100)

def generate_random_formula(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    trials = 30
    instances_tested = 0
    frobenius_schur_values = []
    frege_depth_values = []

    for _ in range(trials):
        n = random.choice([5, 10, 15, 20, 30, 40])
        m = random.randint(1, n)
        formula = generate_random_formula(n, m)

        # Construct the matrix based on the formula
        matrix = [[0] * n for _ in range(n)]
        for clause in formula:
            for var in clause:
                matrix[var][var] += 1

        frobenius_schur = frobenius_schur_indicator(matrix)
        depth = frege_proof_depth(formula)

        frobenius_schur_values.append(frobenius_schur)
        frege_depth_values.append(depth)
        instances_tested += 1

    n_max = max(n for _ in range(trials))
    if n_max < 16:
        return {
            "metric_name": "Frobenius-Schur Indicator vs Frege Proof Depth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }

    correlation = sum((frobenius_schur_values[i] - mean_frobenius) * (frege_depth_values[i] - mean_depth)
                      for i in range(trials)) / trials
    variance_frobenius = sum((frobenius_schur_values[i] - mean_frobenius) ** 2 for i in range(trials)) / trials
    variance_depth = sum((frege_depth_values[i] - mean_depth) ** 2 for i in range(trials)) / trials
    std_dev_frobenius = math.sqrt(variance_frobenius)
    std_dev_depth = math.sqrt(variance_depth)

    if std_dev_frobenius == 0 or std_dev_depth == 0:
        return {
            "metric_name": "Frobenius-Schur Indicator vs Frege Proof Depth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Standard deviation is zero"
        }

    slope = correlation * std_dev_depth / std_dev_frobenius
    intercept = mean_depth - slope * mean_frobenius

    return {
        "metric_name": "Frobenius-Schur Indicator vs Frege Proof Depth",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(slope) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_slope = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_slope = math.sqrt(sum((r["metric_value"] - mean_slope) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_dev_slope} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")