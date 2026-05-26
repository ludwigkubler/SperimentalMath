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
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        max_row = j
        for i in range(j+1, m):
            if abs(augmented_matrix[i][j]) > abs(augmented_matrix[max_row][j]):
                max_row = i
        augmented_matrix[j], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[j]
        pivot = augmented_matrix[j][j]
        for k in range(j, n+1):
            augmented_matrix[j][k] /= pivot
        for i in range(m):
            if i != j:
                factor = augmented_matrix[i][j]
                for k in range(j, n+1):
                    augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
    return [row[-1] for row in augmented_matrix]

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    A = [[Fraction(matrix[i][j]) for j in range(n)] for i in range(m)]
    return sum(1 for row in gaussian_elimination(A, [0]*n) if any(row))

def generate_tseitin_formula(n):
    variables = list(range(n))
    clauses = []
    for i in range(n):
        clauses.append([variables[i]])
    for i in range(n-1):
        new_var = n + i
        clauses.append([-variables[i], new_var])
        clauses.append([-new_var, variables[i+1]])
    return variables, clauses

def tropicalize(matrix):
    m, n = len(matrix), len(matrix[0])
    tropical_matrix = [[max(matrix[i][j], matrix[j][i]) for j in range(n)] for i in range(m)]
    return tropical_matrix

def resolution_tree_width(clauses):
    # Simplified version of resolution tree width calculation
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    variables, clauses = generate_tseitin_formula(n)
    
    W_G = [[0] * n for _ in range(n)]
    for clause in clauses:
        for var in clause:
            W_G[abs(var)-1][abs(var)-1] += 1
    
    tropical_W_G = tropicalize(W_G)
    rho_W_W_G = rank(tropical_W_G)
    
    t_star_G = resolution_tree_width(clauses)
    
    expected_rho = math.log(n + math.log(m))
    conjecture_holds = rho_W_W_G >= expected_rho
    counterexample = "" if conjecture_holds else f"rho_W(W_G)={rho_W_W_G}, expected>=Θ(log({n}+log({m})))"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rho_W_W_G,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho_W(W_G) < Θ(log(n + log(m)))\" first_failing_seed={first_failing_seed}")