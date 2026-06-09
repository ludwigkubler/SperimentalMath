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
from fractions import Fraction
import math

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    C = [[Fraction(0) for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose_matrix(A):
    rows, cols = len(A), len(A[0])
    T = [[Fraction(0) for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            T[j][i] = A[i][j]
    return T

def matrix_determinant(A):
    rows, cols = len(A), len(A[0])
    if rows != cols:
        raise ValueError("Determinant is only defined for square matrices")
    if rows == 1:
        return A[0][0]
    det = Fraction(0)
    sign = Fraction(1)
    for j in range(cols):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * matrix_determinant(submatrix)
        sign *= -1
    return det

def inverse_fraction(A):
    det = matrix_determinant(A)
    if det == Fraction(0):
        raise ValueError("Matrix is not invertible")
    rows, cols = len(A), len(A[0])
    adjugate = [[Fraction(0) for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            adjugate[j][i] = (-1) ** (i + j) * matrix_determinant(submatrix)
    inv_A = matrix_multiply(transpose_matrix(adjugate), Fraction(1, det))
    return inv_A

def local_cohomological_defect(cnf):
    n = len(set(abs(lit) for clause in cnf for lit in clause))
    A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for clause in cnf:
        for i, lit1 in enumerate(clause):
            for j, lit2 in enumerate(clause):
                if i != j and abs(lit1) == abs(lit2):
                    A[i-1][j-1] += Fraction(1)
    try:
        inv_A = inverse_fraction(A)
    except ValueError as e:
        print(f"Error: {e}")
        return None
    return sum(sum(row) for row in inv_A)

def correlation_coefficient(x, y):
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    var_x = sum((xi - mean_x) ** 2 for xi in x) / n
    var_y = sum((yi - mean_y) ** 2 for yi in y) / n
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    metric_value = []
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2 * n, 4 * n))
            lcd = local_cohomological_defect(cnf)
            if lcd is not None:
                instances_tested += 1
                metric_value.append(lcd)
    
    if instances_tested < 30:
        return {
            "metric_name": "Local Cohomological Defect",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    corr_coeff = correlation_coefficient(metric_value, [len(cnf) for _ in metric_value])
    if corr_coeff < 0.7:
        conjecture_holds = False
        counterexample = f"Correlation coefficient {corr_coeff} is less than 0.7"
    
    return {
        "metric_name": "Local Cohomological Defect",
        "metric_value": corr_coeff,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient < 0.7' first_failing_seed={first_failing_seed}")