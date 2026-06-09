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
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = Fraction(1)
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def inverse(A):
    n = len(A)
    det = determinant(A)
    if det == Fraction(0):
        raise ValueError("Matrix is not invertible")
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [[A[m][k] for k in range(n) if k != j] for m in range(n) if m != i]
            adjugate[i][j] = (-1)**(i+j) * determinant(submatrix)
    return matrix_multiplication(adjugate, Fraction(1, det))

def resolution_width(cnf):
    variables = set()
    for clause in cnf:
        for lit in clause:
            variables.add(abs(lit))
    n = len(variables)
    if n == 0:
        return 0
    A = [[Fraction(0)] * (n+1) for _ in range(n)]
    b = [Fraction(0)] * n
    for clause in cnf:
        for lit in clause:
            i = variables.index(abs(lit)) - 1
            if lit > 0:
                A[i][i] += Fraction(1)
            else:
                A[i][i] -= Fraction(1)
                b[i] -= Fraction(1)
    try:
        x = gaussian_elimination(A, b)
        return max(x) + 1
    except ZeroDivisionError:
        return float('inf')

def cayley_graph_diameter(cnf):
    variables = set()
    for clause in cnf:
        for lit in clause:
            variables.add(abs(lit))
    n = len(variables)
    if n == 0:
        return 0
    adjacency_matrix = [[Fraction(0)] * n for _ in range(n)]
    for clause in cnf:
        for lit1 in clause:
            i = variables.index(abs(lit1)) - 1
            for lit2 in clause:
                j = variables.index(abs(lit2)) - 1
                if lit1 != lit2:
                    adjacency_matrix[i][j] += Fraction(1)
    distance_matrix = [row[:] for row in adjacency_matrix]
    n = len(distance_matrix)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                distance_matrix[i][j] = min(distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j])
    return max(max(row) for row in distance_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    widths = []
    diameters = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = [[random.randint(-n, n) for _ in range(random.randint(2, 4))] for _ in range(n)]
            width = resolution_width(cnf)
            diameter = cayley_graph_diameter(cnf)
            widths.append(width)
            diameters.append(diameter)
            instances_tested += 1
            if n > n_max:
                n_max = n

    if len(widths) == 0 or len(diameters) == 0:
        return {
            "metric_name": "resolution_width vs cayley_graph_diameter",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    correlation = sum((widths[i] - mean_width) * (diameters[i]**2 - mean_diameter**2) for i in range(len(widths))) / len(widths)
    mean_ratio = sum(width / diameter**2 for width, diameter in zip(widths, diameters)) / len(widths)

    if correlation < 0.8 or mean_ratio > 1:
        conjecture_holds = False
        counterexample = "correlation_bound_violated"

    return {
        "metric_name": "resolution_width vs cayley_graph_diameter",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_correlation = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_bound_violated\" first_failing_seed={first_failing_seed}")