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
from fractions import Fraction
from math import sqrt

def generate_random_matrix(n):
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(i, n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i + 1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
    
    return x

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def characteristic_polynomial(matrix):
    n = len(matrix)
    x = Fraction('x')
    identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    char_poly = 1
    for k in range(2, n + 1):
        A_k = matrix_multiplication(identity_matrix, matrix) - matrix_multiplication(matrix, identity_matrix)
        det_A_k = determinant(A_k)
        char_poly *= x - det_A_k
    return char_poly

def count_p_adic_roots(char_poly, p):
    roots = set()
    for i in range(p**2):
        if char_poly.subs('x', Fraction(i, p)) == 0:
            roots.add(Fraction(i, p))
    return len(roots)

def rank(matrix):
    n = len(matrix)
    A = [row[:] + [1] for row in matrix]
    gaussian_elimination(A, [0] * n)
    rank = sum(1 for row in A if any(row[j] != 0 for j in range(n)))
    return rank

def variance(values):
    mean = sum(values) / len(values)
    return sum((x - mean) ** 2 for x in values) / len(values)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        communication_matrix = generate_random_matrix(n)
        
        char_poly = characteristic_polynomial(communication_matrix)
        p_adic_roots_count = count_p_adic_roots(char_poly, 2)  # Assuming p=2
        rank_value = rank(communication_matrix)
        
        results.append({
            "n": n,
            "p_adic_roots_count": p_adic_roots_count,
            "rank_value": rank_value
        })
    
    if not results:
        return {
            "metric_name": "N_p-adic",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    p_adic_roots_counts = [result["p_adic_roots_count"] for result in results]
    rank_values = [result["rank_value"] for result in results]
    
    ratio_mean = sum(p_adic_roots_counts) / len(p_adic_roots_counts)
    ratio_variance = variance([p_adic_roots_count / rank_value for p_adic_roots_count, rank_value in zip(p_adic_roots_counts, rank_values)])
    
    return {
        "metric_name": "N_p-adic",
        "metric_value": ratio_mean,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": ratio_mean <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "N_p-adic ratio exceeds 3"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")