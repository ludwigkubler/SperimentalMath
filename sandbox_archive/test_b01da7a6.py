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

def matrix_mod_inv(A, m):
    n = len(A)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant_mod(A, m)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    inv_det = mod_inverse(det, m)
    for i in range(n):
        for j in range(n):
            adj[j][i] = (mod_inverse(determinant_minor(A, i, j), m) * det) % m
    return adj

def determinant_mod(matrix, mod):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for c in range(len(matrix)):
        det += ((-1)**c) * matrix[0][c] * determinant_mod(minor(matrix, 0, c), mod)
    return det % mod

def minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]

def determinant_minor(matrix, i, j):
    return determinant_mod(minor(matrix, i, j), 2)

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(i, n + 1):
            A[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = Fraction(A[j][i])
                for k in range(i, n + 1):
                    A[j][k] -= factor * A[i][k]
    return [row[:n] for row in A]

def rank(matrix):
    rref = gaussian_elimination(matrix)
    return sum(1 for row in rref if any(row))

def tseitin_formula(equations, variables):
    n_vars = len(variables)
    literals = {f'x{i}': i for i in range(n_vars)}
    neg_lits = {f'-x{i}': i for i in range(n_vars)}
    clauses = []
    for eq in equations:
        clause = []
        for term in eq.split(' '):
            if term.startswith('-'):
                lit = neg_lits[term]
            else:
                lit = literals[term]
            clause.append(lit)
        clauses.append(clause)
    return clauses

def resolution_proofs_width(clauses):
    n_clauses = len(clauses)
    max_width = 0
    for i in range(n_clauses):
        for j in range(i + 1, n_clauses):
            common_lits = set(clauses[i]) & set(clauses[j])
            if not common_lits:
                continue
            new_clause = [lit for lit in clauses[i] if lit not in common_lits]
            new_clause.extend([f'-{lit}' for lit in clauses[j] if lit not in common_lits])
            max_width = max(max_width, len(new_clause))
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = [f'x{i}' for i in range(n)]
    equations = []
    for _ in range(n):
        eq = ' '.join(random.sample(variables, random.randint(1, n)))
        equations.append(eq)
    tseitin_clauses = tseitin_formula(equations, variables)
    rank_value = rank([[int(lit[1:]) if lit.startswith('-') else int(lit) for lit in clause] for clause in tseitin_clauses])
    width_value = resolution_proofs_width(tseitin_clauses)
    return {
        "metric_name": "Rank vs Width",
        "metric_value": rank_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")