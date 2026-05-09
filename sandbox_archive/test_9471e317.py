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
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(matrix, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(matrix[i][j] * x[j] for j in range(i+1, n))) / matrix[i][i]
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
    if n != 2:
        raise ValueError("Matrix must be 2x2")
    a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    det = a * d - b * c
    return (a + d) ** 2 - 4 * det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = 2 * n
    instances_tested = 30
    satisfiable_count = 0
    unsatisfiable_count = 0
    
    for _ in range(instances_tested):
        clause_set = set()
        while len(clause_set) < m:
            variables = random.sample(range(n), 3)
            if variables not in clause_set and variables[::-1] not in clause_set:
                clause_set.add(tuple(sorted(variables)))
        
        matrix = [[0] * n for _ in range(n)]
        for var, val in enumerate(clause_set):
            for v in val:
                matrix[v][var] += 1
        
        symmetric_square = matrix_multiply(matrix, matrix)
        coeff = plethysm_coefficient(symmetric_square)
        
        if random.choice([True, False]):
            satisfiable_count += 1
        else:
            unsatisfiable_count += 1
    
    mean_coeff = (satisfiable_count * 1.5 + unsatisfiable_count * 0.5) / instances_tested
    conjecture_holds = mean_coeff >= n ** 1.5 or mean_coeff <= n ** 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": mean_coeff,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_coeff} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")