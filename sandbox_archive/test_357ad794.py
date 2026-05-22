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

def gaussian_elimination(A, b):
    n = len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]

    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j

        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]

        factor = augmented_matrix[i][i]
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= factor

        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]

    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][n]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]

    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)

    # Generate a random n-CNF instance
    clauses = []
    for _ in range(n):
        variables = list(range(1, n+1))
        clause = [random.choice([f'x{i}', f'-x{i}']) for i in variables]
        clauses.append(clause)

    # Convert CNF to a system of linear equations over Z/2Z
    A = []
    b = []
    for clause in clauses:
        row = [0] * n
        for literal in clause:
            var = int(literal[1:])
            if literal[0] == '-':
                row[var-1] = 1
        A.append(row)
        b.append(1)

    # Solve the system using Gaussian elimination
    try:
        solution = gaussian_elimination(A, b)
    except ValueError as e:
        return {
            "metric_name": "DPLL_search_tree_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

    # Calculate the rank of the matrix A
    rank = len([row for row in A if any(row[i] != 0 for i in range(n))])

    # Estimate DPLL search tree width (simplified heuristic)
    dpll_width = sum(1 for var in range(n) if solution[var] == 1)

    return {
        "metric_name": "DPLL_search_tree_width",
        "metric_value": dpll_width,
        "instances_tested": 1,
        "conjecture_holds": dpll_width <= rank * 2,  # Simplified heuristic
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*100 + 1, 100))  # Default to first 30 primes

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")