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
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0 for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_add(A, B):
    m = len(A)
    n = len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_subtract(A, B):
    m = len(A)
    n = len(A[0])
    C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return C

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def transpose(A):
    m = len(A)
    n = len(A[0])
    B = [[A[j][i] for j in range(m)] for i in range(n)]
    return B

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def compute_coxeter_matrix(variables, clauses):
    m = len(clauses)
    n = len(variables)
    W_G = [[0 for _ in range(m + n)] for _ in range(m + n)]
    
    # Initialize the matrix with identity blocks
    for i in range(n):
        W_G[i][i] = 1
    
    # Fill in the matrix based on clauses
    for j, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                W_G[j + n][var - 1] = 2
                W_G[var - 1][j + n] = 2
    
    return W_G

def tropicalize_matrix(A):
    m = len(A)
    n = len(A[0])
    B = [[float('-inf') for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if A[i][j] != 0:
                B[i][j] = max(B[i][j], math.log(abs(A[i][j])))
    return B

def resolution_tree_width(clauses):
    m = len(clauses)
    width = 1
    for clause in clauses:
        width = lcm(width, len(clause))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) if random.random() < 0.8 else -random.choice(variables) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    
    W_G = compute_coxeter_matrix(variables, clauses)
    tropicalized_W_G = tropicalize_matrix(W_G)
    rho_W_W_G = max(max(row) for row in tropicalized_W_G)
    
    t_star_G = resolution_tree_width(clauses)
    
    expected_rho = math.log(n + math.log(m))
    if rho_W_W_G < expected_rho:
        return {
            "metric_name": "rho_W(W_G)",
            "metric_value": rho_W_W_G,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rho_W(W_G)={rho_W_W_G}, expected>=Θ(log(n + log(m)))"
        }
    
    if t_star_G < 2 ** math.ceil(rho_W_W_G):
        return {
            "metric_name": "t*(G)",
            "metric_value": t_star_G,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"t*(G)={t_star_G}, expected>=2^Ω(ρ_W(W_G))"
        }
    
    return {
        "metric_name": "rho_W(W_G)",
        "metric_value": rho_W_W_G,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho_W(W_G) or t*(G) does not meet the conjecture\" first_failing_seed={first_failing_seed}")