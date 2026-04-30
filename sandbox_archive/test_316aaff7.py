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
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(len(B)))
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        factor = 1 / augmented_matrix[i][i]
        for j in range(n+1):
            augmented_matrix[i][j] *= factor
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def tropical_multiplication(a, b):
    return max(a, b)

def tropical_addition(a, b):
    return a + b

def tropical_negation(a):
    return -a

def tropical_zero():
    return float('-inf')

def tropical_one():
    return 0

def tropical_identity(n):
    return [[tropical_one() if i == j else tropical_zero() for j in range(n)] for i in range(n)]

def tropical_inverse(A):
    n = len(A)
    I = tropical_identity(n)
    A_inv = I
    for _ in range(n):
        for i in range(n):
            if A[i][i] == tropical_one():
                continue
            factor = tropical_negation(A[i][i])
            for j in range(n):
                A[i][j] = tropical_multiplication(factor, A[i][j])
                I[i][j] = tropical_multiplication(factor, I[i][j])
        for i in range(n):
            if i == _:
                continue
            factor = tropical_negation(A[_][i])
            for j in range(n):
                A[_][j] = tropical_addition(A[_][j], tropical_multiplication(factor, A[i][j]))
                I[_][j] = tropical_addition(I[_][j], tropical_multiplication(factor, I[i][j]))
    return A_inv

def tropical_determinant(A):
    n = len(A)
    det = tropical_one()
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        det = tropical_multiplication(det, A[i][i])
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] = tropical_addition(A[j][k], tropical_multiplication(factor, A[i][k]))
    return det

def tropical_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if all(abs(A[j][i]) == tropical_zero() for j in range(n)):
            continue
        rank += 1
        factor = tropical_negation(A[i][i])
        for j in range(n):
            A[j][i] = tropical_multiplication(factor, A[j][i])
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] = tropical_addition(A[j][k], tropical_multiplication(factor, A[i][k]))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    phase_cells = 0
    for _ in range(100):  # Aim for at least 30 instances per seed
        circuit = [random.randint(-10, 10) for _ in range(n)]
        tropical_rank_value = tropical_rank(circuit)
        # Simulate counting phase cells (placeholder logic)
        phase_cells += tropical_rank_value
    return {
        "metric_name": "Phase Cell Count",
        "metric_value": phase_cells,
        "instances_tested": 100,
        "conjecture_holds": phase_cells <= tropical_rank_value,
        "counterexample": "" if phase_cells <= tropical_rank_value else f"Exceeded Tropical Proof Rank by {phase_cells - tropical_rank_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Exceeded Tropical Proof Rank\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient data")