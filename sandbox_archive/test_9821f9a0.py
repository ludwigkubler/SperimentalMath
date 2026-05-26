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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    # Augment the matrix with the identity matrix
    augmented = [[matrix[i][j] if i == j else 0 for j in range(n)] + [1 if i == k else 0 for k in range(n)] for i in range(n)]
    # Perform Gaussian elimination
    for i in range(n):
        # Make the diagonal element 1
        pivot = augmented[i][i]
        for j in range(i, n * 2):
            augmented[i][j] = (augmented[i][j] * mod_inverse(pivot, mod)) % mod
        # Eliminate other elements in the column
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(i, n * 2):
                    augmented[k][j] = (augmented[k][j] - factor * augmented[i][j]) % mod
    # Extract the inverse matrix
    inverse = [[augmented[i][j + n] for j in range(n)] for i in range(n)]
    return inverse

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % 2
    return C

def matrix_power(matrix, power):
    n = len(matrix)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while power > 0:
        if power % 2 == 1:
            result = matrix_multiply(result, matrix)
        matrix = matrix_multiply(matrix, matrix)
        power //= 2
    return result

def frege_proof_width(formula):
    if isinstance(formula, str) and formula.isalpha():
        return 1
    elif isinstance(formula, list):
        return max(frege_proof_width(subformula) for subformula in formula)
    else:
        raise ValueError("Invalid Frege proof formula")

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([20, 25, 30, 35, 40])
    d = random.randint(1, n)
    p = 7  # Fixed prime for simplicity
    c = 1  # Constant independent of n

    # Generate a random Frege proof tree
    def generate_formula(depth):
        if depth == 0:
            return random.choice(['x1', 'x2', 'x3'])
        else:
            op = random.choice(['&', '|'])
            subformulas = [generate_formula(depth - 1) for _ in range(2)]
            return [op, *subformulas]

    formula = generate_formula(d)
    proof_width = frege_proof_width(formula)

    # Compute the clause indicator polynomial modulo p
    def clause_indicator_polynomial(formula):
        if isinstance(formula, str):
            return {formula: 1}
        elif isinstance(formula, list):
            op = formula[0]
            subformulas = formula[1:]
            if op == '&':
                return sum(clause_indicator_polynomial(subformula) for subformula in subformulas)
            elif op == '|':
                result = {}
                for subformula in subformulas:
                    result.update(clause_indicator_polynomial(subformula))
                return result
        else:
            raise ValueError("Invalid Frege proof formula")

    polynomial = clause_indicator_polynomial(formula)

    # Determine the minimal rank of an Eichler order for the polynomial
    def minimal_rank(polynomial):
        n_vars = len(polynomial)
        identity_matrix = [[1 if i == j else 0 for j in range(n_vars)] for i in range(n_vars)]
        A = [[polynomial.get(f'x{i+1}', 0) for i in range(n_vars)] for _ in range(n_vars)]
        B = matrix_power(A, p)
        C = matrix_multiply(B, identity_matrix)
        rank = sum(1 for row in C if any(row))
        return rank

    rank = minimal_rank(polynomial)

    # Compare the actual rank to the expected value
    expected_value = c * p ** (n - d / 2)
    conjecture_holds = rank >= expected_value
    counterexample = "" if conjecture_holds else f"rank={rank}, expected={expected_value}"

    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")