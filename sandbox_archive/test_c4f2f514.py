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
from itertools import combinations, permutations

def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(matrix: list[list[int]]) -> int:
    n = len(matrix)
    det = 0
    if n == 1:
        return matrix[0][0]
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** j
        det += sign * matrix[0][j] * determinant(submatrix)
    return det

def gaussian_elimination(A: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    n = len(A)
    B = [list(range(n)) for _ in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        B[i], B[max_row] = B[max_row], B[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A, B

def inverse(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    augmented_matrix = [row + col for row, col in zip(matrix, identity)]
    A, B = gaussian_elimination(augmented_matrix)
    if any(A[i][i] == 0 for i in range(n)):
        return None
    inverse = [[A[i][j+n] for j in range(n)] for i in range(n)]
    return inverse

def hook_length_formula(shape: list[int], n: int) -> Fraction:
    numerator = math.factorial(n)
    denominator = 1
    for row, col in product(range(n), repeat=2):
        if shape[row] > col and (row + 1 < n or col < shape[row+1]):
            denominator *= shape[row] - col
    return Fraction(numerator, denominator)

def young_tableau_count(shape: list[int], n: int) -> int:
    total = math.factorial(n)
    for size in shape:
        total //= math.factorial(size)
    for i in range(1, len(shape)):
        total //= math.factorial(len(shape) - i)
    return total

def multiplicity(f: str, shape: tuple[int], n: int) -> Fraction:
    if f == 'perm':
        return hook_length_formula(shape, n)
    elif f == 'det':
        det = determinant([[i+1 for i in range(n)]])
        return young_tableau_count(shape, n) * (Fraction(1, 2) ** n)
    else:
        return Fraction(0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_min = 5
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(n_min, n_max + 1):
        m_max = int(n ** 1.5)
        for _ in range(30):  # Ensure at least 30 instances per seed
            m = random.randint(1, m_max - 1)
            mu_perm = multiplicity('perm', (n-1, 1), n)
            mu_det = multiplicity('det', (m,), n)
            if mu_perm <= mu_det:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}: μ(perm_n, λ) = {mu_perm}, μ(det_m^O(1), λ) = {mu_det}"
                break
        instances_tested += 30

    if conjecture_holds:
        mean_metric_value = total_metric_value / instances_tested
        std_metric_value = math.sqrt(total_metric_value**2 / instances_tested - mean_metric_value**2)
    else:
        mean_metric_value = None
        std_metric_value = None

    return {
        "metric_name": "Multiplicity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results)/len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results)/len(results)))**2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")