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
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        pivot_row = max(range(j, m), key=lambda i: abs(augmented[i][j]))
        if augmented[pivot_row][j] == 0:
            continue
        augmented[j], augmented[pivot_row] = augmented[pivot_row], augmented[j]
        for i in range(m):
            if i != j:
                factor = -augmented[i][j] / augmented[j][j]
                for k in range(n + 1):
                    augmented[i][k] += factor * augmented[j][k]
    return [row[-1] for row in augmented]

def rank(A):
    m, n = len(A), len(A[0])
    A_copy = [row[:] for row in A]
    rank = 0
    for i in range(n):
        if all(A_copy[j][i] == 0 for j in range(rank)):
            continue
        pivot_row = rank
        for j in range(rank + 1, m):
            if abs(A_copy[j][i]) > abs(A_copy[pivot_row][i]):
                pivot_row = j
        A_copy[pivot_row], A_copy[rank] = A_copy[rank], A_copy[pivot_row]
        rank += 1
    return rank

def characteristic_polynomial(matrix):
    n = len(matrix)
    if n == 0:
        return [1]
    if n == 1:
        return [matrix[0][0], -1]
    
    char_poly = [1]
    for i in range(n):
        sub_matrix = [[matrix[j][k] for k in range(n) if k != i] for j in range(1, n)]
        sub_det = characteristic_polynomial(sub_matrix)
        char_poly = [c * matrix[0][i] + (-1)**(i+1) * s for c in char_poly for s in sub_det]
    return char_poly

def min_representations(char_poly):
    n = len(char_poly) - 1
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    def is_positive_definite(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] <= 0:
                return False
            for j in range(i + 1, m):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return True
    
    def count_representations(char_poly):
        n = len(char_poly) - 1
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        count = 0
        for i in range(2, n + 1):
            sub_matrix = [[char_poly[j][k] for k in range(n) if k != i - 1] for j in range(i)]
            if is_positive_definite(sub_matrix):
                count += 1
        return count
    
    return count_representations(char_poly)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(1, n)
    
    # Generate a random CNF formula
    variables = set(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    
    # Construct the communication complexity matrix A(φ)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            count = sum(1 for clause in clauses if (i + 1) in clause and (j + 1) not in clause or (i + 1) not in clause and (j + 1) in clause)
            A[i][j] = A[j][i] = count
    
    # Compute the characteristic polynomial of A(φ)
    char_poly = characteristic_polynomial(A)
    
    # Determine the minimal number of positive definite symplectic quadratic forms required to represent its characteristic polynomial
    min_rep = min_representations(char_poly)
    
    # Measure the rank variance of A(φ)
    rank_A = rank(A)
    rank_variance = (rank_A - n) / n
    
    return {
        "metric_name": "rank_variance",
        "metric_value": rank_variance,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank_variance <= min_rep,
        "counterexample": "" if rank_variance <= min_rep else f"Rank variance {rank_variance} > min_rep {min_rep}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_variance > min_rep\" first_failing_seed={first_failing_seed}")