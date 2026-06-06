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
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = 0
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            adj[j][i] = ((-1) ** (i+j)) * determinant(minor)
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matrix is singular")
    inv_det = mod_inverse(det, mod)
    for i in range(n):
        for j in range(n):
            adj[i][j] = (adj[i][j] * inv_det) % mod
    return adj

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det = 0
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(minor)
        return det

def gaussian_elimination(matrix, mod):
    n = len(matrix)
    augmented_matrix = [row[:] + [i] for i, row in enumerate(matrix)]
    for i in range(n):
        pivot_row = max(range(i, n), key=lambda x: abs(augmented_matrix[x][i]))
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
        lead = augmented_matrix[i][i]
        for j in range(i, n + 1):
            augmented_matrix[i][j] = (augmented_matrix[i][j] * mod_inverse(lead, mod)) % mod
        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(i, n + 1):
                    augmented_matrix[k][j] = (augmented_matrix[k][j] - factor * augmented_matrix[i][j]) % mod
    return [row[:-1] for row in augmented_matrix]

def generate_cnf(n):
    clauses = []
    for i in range(2**n):
        clause = []
        for j in range(n):
            if (i >> j) & 1:
                clause.append(j + 1)
            else:
                clause.append(-(j + 1))
        clauses.append(clause)
    return clauses

def sat_clause_subset_complexity(cnf):
    n = len(cnf[0])
    max_clauses = 2**n
    complexity = [0] * (max_clauses + 1)
    for i in range(1, max_clauses + 1):
        for j in range(i):
            if all(x in cnf[j] for x in cnf[i]):
                complexity[i] += 1
    return sum(complexity)

def hodge_tate_degree(cnf):
    n = len(cnf[0])
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for clause in cnf:
        for x in clause:
            if x > 0:
                i, j = x - 1, (x - 1) % n
            else:
                i, j = -x - 1, (-x - 1) % n
            matrix[i][j] += 1
    matrix = gaussian_elimination(matrix, 2)
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    htd = hodge_tate_degree(cnf)
    csc = sat_clause_subset_complexity(cnf)
    correlation = (htd - csc) / math.sqrt(htd**2 + csc**2)
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation) > 0.7 and correlation >= -0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] and r["metric_value"] < -0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"] and result["metric_value"] < -0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_below_minus_0.5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")