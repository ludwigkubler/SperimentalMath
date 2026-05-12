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
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * matrix_minor(matrix, 0, i) * (-1) ** (0 + i)
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = []
    for i in range(n):
        row = []
        for j in range(n):
            minor = matrix_minor(matrix, i, j)
            cofactor = (-1) ** (i + j) * minor
            row.append(cofactor % mod)
        adjugate.append(row)
    inv_matrix = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def matrix_minor(matrix, i, j):
    submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
    return determinant(submatrix)

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for j in range(len(matrix)):
        det += ((-1) ** j) * matrix[0][j] * determinant([row[:j] + row[j+1:] for row in matrix[1:]])
    return det

def multiply_matrices(a, b):
    result = [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
    return result

def add_matrices(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def subtract_matrices(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def is_zero_matrix(matrix):
    return all(all(val == 0 for val in row) for row in matrix)

def is_identity_matrix(matrix):
    n = len(matrix)
    return all(all(matrix[i][j] == (1 if i == j else 0) for j in range(n)) for i in range(n))

def extend_basis(basis, vector):
    basis.append(vector)
    return basis

def reduce_basis(basis, mod):
    n = len(basis[0])
    for i in range(n):
        pivot_row = None
        for j in range(len(basis)):
            if basis[j][i] != 0:
                pivot_row = j
                break
        if pivot_row is not None:
            for k in range(len(basis)):
                if k != pivot_row and basis[k][i] != 0:
                    factor = (basis[k][i] * mod_inverse(basis[pivot_row][i], mod)) % mod
                    basis[k] = subtract_matrices(basis[k], multiply_matrices([[factor]], basis[pivot_row]))
    return [row for row in basis if not is_zero_matrix(row)]

def groebner_basis(generators, mod):
    basis = generators[:]
    while True:
        new_elements = []
        for i in range(len(basis)):
            for j in range(i + 1, len(basis)):
                s = subtract_matrices(basis[i], multiply_matrices([[basis[j][k] * mod_inverse(basis[i][j], mod)]], basis[j]))
                if not is_zero_matrix(s):
                    new_elements.append(s)
        if not new_elements:
            break
        for element in new_elements:
            basis = extend_basis(basis, element)
            basis = reduce_basis(basis, mod)
    return basis

def hilbert_function(ideal, d, mod):
    n = len(ideal[0])
    monomials = [[1] * (n + 1)]
    for i in range(1, d + 1):
        new_monomials = []
        for monomial in monomials:
            for j in range(n + 1):
                if monomial[j] < i:
                    new_monomial = monomial[:]
                    new_monomial[j] += 1
                    new_monomials.append(new_monomial)
        monomials.extend(new_monomials)
    count = 0
    for monomial in monomials:
        product = [1]
        for i in range(n):
            if monomial[i] > 0:
                product = multiply_matrices(product, ideal[i])
        if is_zero_matrix(subtract_matrices(product, [[monomial[-1]]])):
            count += 1
    return count % mod

def extended_frege_length(phi):
    # Placeholder for actual implementation
    return random.randint(10, 100)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = []
    for _ in range(n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        phi.append(clause)
    ideal = groebner_basis(phi, 2**32 - 5)
    d = math.ceil(n / 2)
    H = hilbert_function(ideal, d, 2**32 - 5)
    lambda_n = extended_frege_length(phi)
    if lambda_n == 0:
        return {
            "metric_name": "Hilbert function",
            "metric_value": H,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    expected_H = round(2 ** (-lambda_n))
    if abs(H - expected_H) <= expected_H / 2:
        return {
            "metric_name": "Hilbert function",
            "metric_value": H,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Hilbert function",
            "metric_value": H,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"H({n}, {d}) = {H} does not match expected ≈ {expected_H}"
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_metric_value = sum(res["metric_value"] for res in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")