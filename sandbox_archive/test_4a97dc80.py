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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"No modular inverse for {a} modulo {m}")
    return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0] * n for _ in range(n)]
    det = determinant(matrix, mod)
    inv_det = mod_inverse(det, mod)

    for i in range(n):
        for j in range(n):
            minor = get_minor(matrix, i, j)
            cofactor = (-1) ** (i + j) * determinant(minor, mod)
            adj[j][i] = (cofactor * inv_det) % mod

    return adj

def determinant(matrix, mod):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        minor = get_minor(matrix, 0, j)
        det += (matrix[0][j] * (-1) ** j * determinant(minor, mod)) % mod
    return det

def get_minor(matrix, i, j):
    n = len(matrix)
    minor = []
    for x in range(n):
        if x == i:
            continue
        row = []
        for y in range(n):
            if y == j:
                continue
            row.append(matrix[x][y])
        minor.append(row)
    return minor

def matrix_mult(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_add(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] + B[i][j]) % mod
    return C

def matrix_sub(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] - B[i][j]) % mod
    return C

def matrix_scalar_mul(matrix, scalar, mod):
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (matrix[i][j] * scalar) % mod
    return result

def generate_tseitin_formula(n):
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []

    # Generate clauses for each variable
    for i in range(n):
        clauses.append(f'{variables[i]} {variables[n+i]}')
        clauses.append(f'-{variables[i]} -{variables[n+i]}')

    # Generate clauses for implications
    for i in range(1, n):
        clauses.append(f'{-variables[i-2]} {variables[i-1]}')
        clauses.append(f'{variables[i-2]} -{variables[i-1]}')

    return variables, clauses

def read_twice_bp_complexity(clauses):
    # Placeholder function to compute Read-Twice BP complexity
    # This is a dummy implementation for testing purposes
    return len(clauses)

def minimal_local_cohomology_rank(variables, clauses):
    n = len(variables)
    m = len(clauses)
    
    # Create the augmented matrix for the system of linear equations
    A = [[0] * (2*n + 1) for _ in range(m)]
    for i in range(m):
        if 'x' in clauses[i]:
            j = int(clauses[i].split()[1][1:]) - 1
            A[i][j] = 1
        else:
            j = int(clauses[i].split()[2][1:]) - 1
            A[i][j] = -1
    
    # Augment the matrix with an identity matrix to find the null space
    for i in range(n):
        A[i][n + i] = 1
    
    # Perform Gaussian elimination to find the rank of the matrix
    def gaussian_elimination(matrix, mod):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        
        for j in range(cols - 1):
            pivot_row = None
            for i in range(rank, rows):
                if matrix[i][j] != 0:
                    pivot_row = i
                    break
            
            if pivot_row is None:
                continue
            
            # Swap the current row with the pivot row
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            
            # Make the pivot element 1
            pivot = matrix[rank][j]
            for k in range(j, cols):
                matrix[rank][k] = (matrix[rank][k] * mod_inverse(pivot, mod)) % mod
            
            # Eliminate other elements in the current column
            for i in range(rows):
                if i != rank:
                    factor = matrix[i][j]
                    for k in range(j, cols):
                        matrix[i][k] = (matrix[i][k] - factor * matrix[rank][k]) % mod
            
            rank += 1
        
        return rank
    
    rank = gaussian_elimination(A, 2)
    
    # The minimal local cohomology rank is the number of variables minus the rank
    return n - rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    variables, clauses = generate_tseitin_formula(n)
    complexity = read_twice_bp_complexity(clauses)
    rank = minimal_local_cohomology_rank(variables, clauses)
    
    if complexity == 0:
        return {
            "metric_name": "Minimal Local Cohomology Rank",
            "metric_value": rank,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "Read-Twice BP complexity is zero"
        }
    
    ratio = abs(rank - complexity) / complexity
    
    return {
        "metric_name": "Minimal Local Cohomology Rank",
        "metric_value": rank,
        "instances_tested": n,
        "conjecture_holds": ratio <= 0.3 and ratio >= -0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 59))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rank = sum(r["metric_value"] for r in results)
    total_complexity = sum(read_twice_bp_complexity(generate_tseitin_formula(n)[1]) for n in [5, 10, 15, 20, 30, 40])
    mean_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")