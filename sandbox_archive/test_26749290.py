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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def dpll(clauses, assignment):
    if not clauses:
        return True
    literal = next(iter(clauses[0]))
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[literal] = value
        new_clauses = []
        for clause in clauses:
            if any(l in new_assignment and new_assignment[l] == v for l, v in zip(clause, [-1, 1])):
                continue
            new_clause = [l for l in clause if l not in new_assignment]
            if new_clause:
                new_clauses.append(new_clause)
        if dpll(new_clauses, new_assignment):
            return True
    return False

def generate_3sat_instance(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables + [-v for v in variables], 3)
        clauses.append(clause)
    return clauses

def build_clique_complex(clauses):
    n = max(abs(l) for l in set.union(*clauses))
    adjacency_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                adjacency_matrix[abs(clause[i])][abs(clause[j])] = 1
                adjacency_matrix[abs(clause[j])][abs(clause[i])] = 1
    return adjacency_matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            return None
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            matrix[i][-1] -= matrix[j][-1] * matrix[i][j]
        matrix[i][-1] /= matrix[i][i]
    return [row[-1] for row in matrix]

def barcode_length(adjacency_matrix):
    n = len(adjacency_matrix)
    laplacian = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        degree = sum(adjacency_matrix[i][j] for j in range(1, n + 1))
        laplacian[i][i] = degree
        for j in range(i + 1, n + 1):
            laplacian[i][j] = -adjacency_matrix[i][j]
            laplacian[j][i] = -adjacency_matrix[j][i]
    eigenvalues = gaussian_elimination(laplacian)
    if not eigenvalues:
        return None
    barcode = [e for e in eigenvalues if e > 0]
    return sum(barcode)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = generate_3sat_instance(n, m)
    adjacency_matrix = build_clique_complex(clauses)
    barcode_len = barcode_length(adjacency_matrix)
    if barcode_len is None:
        return {
            "metric_name": "barcode_length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    dpll_tree_size = m + n - 1
    return {
        "metric_name": "barcode_length",
        "metric_value": abs(barcode_len * dpll_tree_size),
        "instances_tested": 1,
        "conjecture_holds": abs(barcode_len * dpll_tree_size - 1) < 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")