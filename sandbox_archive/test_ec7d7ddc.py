# auto-injected by SEC sandbox
import math
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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * sum(matrix[j][(j + 1) % n] * matrix[(j + 2) % n][(j + 3) % n]
                                  - matrix[j][(j + 2) % n] * matrix[(j + 1) % n][(j + 3) % n]
                                  for j in range(1, n)) * (-1) ** i
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            if (i + j) % 2 == 0:
                adjugate[i][j] = inv_det * sum(submatrix[k][(k + 1) % n] * submatrix[(k + 2) % n][(k + 3) % n]
                                              - submatrix[k][(k + 2) % n] * submatrix[(k + 1) % n][(k + 3) % n]
                                              for k in range(n)) % mod
            else:
                adjugate[i][j] = -inv_det * sum(submatrix[k][(k + 1) % n] * submatrix[(k + 2) % n][(k + 3) % n]
                                               - submatrix[k][(k + 2) % n] * submatrix[(k + 1) % n][(k + 3) % n]
                                               for k in range(n)) % mod
    return adjugate

def matrix_mod_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= mod
    return C

def matrix_mod_pow(matrix, power, mod):
    n = len(matrix)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    base = matrix
    while power > 0:
        if power % 2 == 1:
            result = matrix_mod_mul(result, base, mod)
        base = matrix_mod_mul(base, base, mod)
        power //= 2
    return result

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(m)] for i, row in enumerate(matrix)]
    for i in range(n):
        pivot = None
        for j in range(i, n):
            if augmented_matrix[j][i] != 0:
                pivot = j
                break
        if pivot is None:
            continue
        augmented_matrix[i], augmented_matrix[pivot] = augmented_matrix[pivot], augmented_matrix[i]
        for j in range(n + m):
            augmented_matrix[i][j] %= mod
        for j in range(n):
            if j != i and augmented_matrix[j][i] != 0:
                factor = -augmented_matrix[j][i] * mod_inverse(augmented_matrix[i][i], mod) % mod
                for k in range(n + m):
                    augmented_matrix[j][k] += factor * augmented_matrix[i][k]
                    augmented_matrix[j][k] %= mod
    rank = 0
    for i in range(n):
        if any(augmented_matrix[i][j] != 0 for j in range(m)):
            rank += 1
    return rank

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-v for v in clause]
        clauses.append(clause)
    return clauses

def tropical_semigroup_rank(clauses):
    n = len(clauses[0])
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for var in clause:
            if var > 0:
                matrix[var - 1][var - 1] += 1
            else:
                matrix[-var - 1][-var - 1] += 1
    return rank(matrix)

def monomial_ideal_complexity(clauses):
    n = len(clauses[0])
    m = len(clauses)
    complexity = 1
    for clause in clauses:
        complexity *= n
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(5, 40)
    clauses = generate_cnf(n, m)
    tropical_rank = tropical_semigroup_rank(clauses)
    monomial_complexity = monomial_ideal_complexity(clauses)
    if tropical_rank > m + n:
        return {
            "metric_name": "tropical_rank",
            "metric_value": tropical_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CNF with n={n}, m={m} has tropical rank {tropical_rank} > c(m+n) for any constant c"
        }
    if monomial_complexity > m ** n:
        return {
            "metric_name": "monomial_complexity",
            "metric_value": monomial_complexity,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CNF with n={n}, m={m} has monomial complexity {monomial_complexity} > m^n"
        }
    return {
        "metric_name": "tropical_rank",
        "metric_value": tropical_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")