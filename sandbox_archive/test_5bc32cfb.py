# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_multiplication(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Matrix dimensions do not match")

    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return result

def gaussian_elimination(matrix):
    n = len(matrix)
    m = len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(m, 2*m)] for i, row in enumerate(matrix)]

    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(augmented_matrix[k][i]) > abs(augmented_matrix[max_row][i]):
                max_row = k

        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]

        factor = augmented_matrix[i][i]
        for j in range(i, 2*m):
            augmented_matrix[i][j] /= factor

        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(i, 2*m):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]

    return [row[m:] for row in augmented_matrix]

def min_ehrhart_quotient(cnf):
    n = len(cnf)
    variables = set(var for clause in cnf for var in clause if isinstance(var, int))
    variables = sorted(variables)

    polytope_points = []
    for assignment in product([-1, 1], repeat=n):
        if all(any(sign * var == assignment[var-1] for sign, var in clause) for clause in cnf):
            point = [0] * (2*n)
            for i, var in enumerate(variables):
                point[i] = assignment[i]
                point[n+i] = -assignment[i]
            polytope_points.append(point)

    if not polytope_points:
        return 0

    matrix = []
    for point in polytope_points:
        row = [point[i] * point[j] for i in range(2*n) for j in range(2*n)]
        matrix.append(row)

    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(x != 0 for x in row))

    return len(polytope_points) // rank

def circuit_monotone_width(cnf):
    n = len(cnf)
    variables = set(var for clause in cnf for var in clause if isinstance(var, int))
    variables = sorted(variables)

    monotone_width = 0
    for assignment in product([-1, 1], repeat=n):
        if all(any(sign * var == assignment[var-1] for sign, var in clause) for clause in cnf):
            monotone_width += 1

    return monotone_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_random_cnf(n)

    mu = min_ehrhart_quotient(cnf)
    wm = circuit_monotone_width(cnf)

    if mu == 0 or wm == 0:
        return {
            "metric_name": "min_ehrhart_quotient",
            "metric_value": mu,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    correlation = (mu * wm) / (math.sqrt(mu**2 + wm**2))
    holds_bound = mu**2 <= wm

    return {
        "metric_name": "min_ehrhart_quotient",
        "metric_value": mu,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation >= 0.5 and holds_bound,
        "counterexample": ""
    }

def generate_random_cnf(n):
    num_clauses = random.randint(2*n, 3*n)
    variables = list(range(1, n+1))
    cnf = []

    for _ in range(num_clauses):
        clause = []
        while not clause:
            literals = random.sample(variables + [-var for var in variables], n)
            clause = [(l if l > 0 else -l, abs(l)) for l in literals]
        cnf.append(clause)

    return cnf

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i, j, k in product(range(5), range(5), range(5))]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")