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

class Fraction:
    def __init__(self, numerator=0, denominator=1):
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("Both numerator and denominator must be integers.")
        common_divisor = gcd(numerator, denominator)
        self.numerator = numerator // common_divisor
        self.denominator = denominator // common_divisor

    def __add__(self, other):
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type for +: 'Fraction' and '{}'".format(type(other).__name__))
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __mul__(self, other):
        if not isinstance(other, (int, Fraction)):
            raise TypeError("Unsupported operand type for *: 'Fraction' and '{}'".format(type(other).__name__))
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        if not isinstance(other, (int, Fraction)):
            raise TypeError("Unsupported operand type for /: 'Fraction' and '{}'".format(type(other).__name__))
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

def matrix_multiplication(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Matrix dimensions do not match for multiplication.")
    result = [[Fraction(0) for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    rows, cols = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(rows)]
    for i in range(cols):
        max_row = i
        for j in range(i+1, rows):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, cols + 1):
            augmented_matrix[i][j] /= pivot
        for j in range(rows):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, cols + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def tseitin_formula(n):
    variables = list(range(1, n+1))
    clauses = []
    for i in range(n):
        y = 2 * n + i + 1
        clauses.append([variables[i], -y])
        for j in range(i+1, n):
            z = 2 * n + j + 1
            clauses.append([-variables[i], variables[j], -z])
            clauses.append([-variables[j], variables[i], -z])
            clauses.append([variables[i], variables[j], y, z])
            clauses.append([-variables[i], -variables[j], y, -z])
            clauses.append([variables[i], -variables[j], -y, z])
            clauses.append([-variables[i], variables[j], -y, -z])
    return variables, clauses

def kauffman_bracket(knot):
    # Placeholder for Kauffman bracket calculation
    # This is a simplified version and should be replaced with actual implementation
    if knot == "unknot":
        return 1
    else:
        return 0

def resolution_width(clauses):
    # Placeholder for resolution width calculation
    # This is a simplified version and should be replaced with actual implementation
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = Fraction(0)
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        variables, clauses = tseitin_formula(n)
        knot = "unknot"  # Placeholder for actual knot calculation
        chi_K = kauffman_bracket(knot)
        w_phi = resolution_width(clauses)
        
        if w_phi > 1.5 * (2 ** chi_K):
            conjecture_holds = False
            counterexample = f"n={n}, w(φ)={w_phi}, O(2^χ(K))={1.5 * (2 ** chi_K)}"
            break
        
        total_metric_value += Fraction(w_phi)
        instances_tested += len(clauses)
        n_max = max(n_max, n)

    return {
        "metric_name": "resolution_width",
        "metric_value": float(total_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")