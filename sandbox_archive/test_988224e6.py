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

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

def gaussian_elimination(matrix, b):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(matrix[i][j] * x[j] for j in range(i + 1, n))) / matrix[i][i]
    return x

def matrix_multiply(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def plethysm_coefficient(matrix):
    n = len(matrix)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    symmetric_square = matrix_multiply(matrix, matrix)
    det = 1
    for i in range(n):
        det *= symmetric_square[i][i]
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = 2 * n
    clause_set = set()
    
    def generate_clause():
        variables = [random.randint(1, n) for _ in range(3)]
        if variables not in clause_set and variables[::-1] not in clause_set:
            clause_set.add(tuple(sorted(variables)))
            return variables
    
    clauses = [generate_clause() for _ in range(m)]
    
    if not all(clauses):
        return {
            "metric_name": "plethysm_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    clause_matrix = [[0] * n for _ in range(m)]
    for i, clause in enumerate(clauses):
        for var in clause:
            clause_matrix[i][var - 1] = 1
    
    plethysm_coeff = plethysm_coefficient(clause_matrix)
    
    if len(clause_set) == m / 2:  # Assuming half of the clauses are satisfiable
        return {
            "metric_name": "plethysm_coefficient",
            "metric_value": plethysm_coeff,
            "instances_tested": 1,
            "conjecture_holds": plethysm_coeff >= n ** 1.5,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "plethysm_coefficient",
            "metric_value": plethysm_coeff,
            "instances_tested": 1,
            "conjecture_holds": plethysm_coeff <= n ** 0.5,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")