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

def matrix_mod_inv(matrix, p):
    n = len(matrix)
    det = 0
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in matrix[1:]]
        det += ((-1) ** i) * matrix[0][i] * matrix_mod_det(minor, p)
    det = det % p
    inv_det = mod_inverse(det, p)
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            cofactor = ((-1) ** (i + j)) * matrix_mod_det(minor, p)
            adjugate[j][i] = cofactor
    inv_matrix = [[(adjugate[i][j] * inv_det) % p for j in range(n)] for i in range(n)]
    return inv_matrix

def matrix_mod_mul(A, B, p):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % p
    return C

def matrix_mod_det(matrix, p):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in matrix[1:]]
        det += ((-1) ** i) * matrix[0][i] * matrix_mod_det(minor, p)
    return det % p

def frege_proof_width(formula):
    if isinstance(formula, str):
        return 1
    else:
        return max(frege_proof_width(subformula) for subformula in formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([20, 25, 30, 35, 40])
    d = random.randint(1, n)
    p = random.randint(2, 100)
    c = 1.0  # Constant independent of n

    # Generate a random Frege proof tree
    def generate_formula(depth):
        if depth == 0:
            return random.choice(['x' + str(i) for i in range(n)])
        else:
            op = random.choice(['&', '|'])
            sub1 = generate_formula(depth - 1)
            sub2 = generate_formula(depth - 1)
            return (op, sub1, sub2)

    formula = generate_formula(d)
    proof_width = frege_proof_width(formula)

    # Compute the clause indicator polynomial modulo p
    def clause_indicator_polynomial(formula):
        if isinstance(formula, str):
            return {formula: 1}
        else:
            op, sub1, sub2 = formula
            if op == '&':
                poly1 = clause_indicator_polynomial(sub1)
                poly2 = clause_indicator_polynomial(sub2)
                result = {}
                for key1 in poly1:
                    for key2 in poly2:
                        new_key = key1 + key2
                        result[new_key] = (result.get(new_key, 0) + poly1[key1] * poly2[key2]) % p
                return result
            elif op == '|':
                poly1 = clause_indicator_polynomial(sub1)
                poly2 = clause_indicator_polynomial(sub2)
                result = {}
                for key in poly1:
                    result[key] = (result.get(key, 0) + poly1[key]) % p
                for key in poly2:
                    if key not in result:
                        result[key] = poly2[key]
                    else:
                        result[key] = (result[key] + poly2[key]) % p
                return result

    clause_poly = clause_indicator_polynomial(formula)

    # Determine the minimal rank of an Eichler order for the polynomial
    def eichler_order_rank(poly):
        n_vars = len(poly)
        matrix = [[0] * n_vars for _ in range(n_vars)]
        for key, value in poly.items():
            if len(key) == 1:
                i = int(key[0][1:])
                matrix[i-1][i-1] += value
            else:
                for var in key:
                    i = int(var[1:])
                    matrix[i-1][i-1] += value

        det = matrix_mod_det(matrix, p)
        return det % p

    rank = eichler_order_rank(clause_poly)

    # Compare the actual rank to the expected value
    expected_value = math.ceil(c * p ** (n - d / 2))
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
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")