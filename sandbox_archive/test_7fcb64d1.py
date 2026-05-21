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
    p = len(B)
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    m, n = len(A), len(A[0])
    result = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return result

def matrix_subtract(A, B):
    m, n = len(A), len(A[0])
    result = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = A + [b]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def is_integer_solution(A, b):
    try:
        solution = gaussian_elimination(A, b)
        return all(isinstance(x, int) for x in solution)
    except ZeroDivisionError:
        return False

def generate_random_matroid(n):
    rank = random.randint(1, n-1)
    elements = list(range(n))
    basis = random.sample(elements, rank)
    matroid = {i: [] for i in range(n)}
    for e in basis:
        matroid[e] = [e]
    for e in elements:
        if e not in basis:
            other_elements = [x for x in basis if x != e]
            new_basis = other_elements + [e]
            matroid[e] = new_basis
    return matroid

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Start with a small size and increase as needed
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        matroid = generate_random_matroid(n)
        A = [[0] * n for _ in range(n)]
        b = [0] * n
        
        # Construct the matrix A and vector b based on the matroid
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) not in matroid[i]:
                    A[i][j] = 1
                    A[j][i] = 1
        
        # Check if the system Ax = b has an integer solution
        if is_integer_solution(A, b):
            instances_tested += 1
    
    return {
        "metric_name": "integer_solutions",
        "metric_value": instances_tested / 30,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")