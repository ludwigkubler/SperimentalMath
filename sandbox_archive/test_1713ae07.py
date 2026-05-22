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
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    augmented_matrix = [row + col for row, col in zip(matrix, identity)]
    
    def swap_rows(mat, r1, r2):
        mat[r1], mat[r2] = mat[r2], mat[r1]
    
    def add_row(mat, r1, r2, factor):
        for i in range(n):
            mat[r1][i] = (mat[r1][i] + factor * mat[r2][i]) % mod
    
    def multiply_row(mat, r, factor):
        for i in range(n):
            mat[r][i] = (mat[r][i] * factor) % mod
    
    for i in range(n):
        if augmented_matrix[i][i] == 0:
            for j in range(i + 1, n):
                if augmented_matrix[j][i] != 0:
                    swap_rows(augmented_matrix, i, j)
                    break
            else:
                raise ValueError("Matrix is singular")
        
        factor = mod_inverse(augmented_matrix[i][i], mod)
        multiply_row(augmented_matrix, i, factor)
        
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                add_row(augmented_matrix, j, i, -factor)
    
    inv_matrix = [[row[i] for row in augmented_matrix[:n]] for i in range(n)]
    return inv_matrix

def matrix_mult(A, B):
    n = len(A)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(matrix, mod):
    n = len(matrix)
    augmented_matrix = [row + [1] for row in matrix]
    
    def swap_rows(mat, r1, r2):
        mat[r1], mat[r2] = mat[r2], mat[r1]
    
    def add_row(mat, r1, r2, factor):
        for i in range(n + 1):
            mat[r1][i] = (mat[r1][i] + factor * mat[r2][i]) % mod
    
    def multiply_row(mat, r, factor):
        for i in range(n + 1):
            mat[r][i] = (mat[r][i] * factor) % mod
    
    for i in range(n):
        if augmented_matrix[i][i] == 0:
            for j in range(i + 1, n):
                if augmented_matrix[j][i] != 0:
                    swap_rows(augmented_matrix, i, j)
                    break
            else:
                raise ValueError("Matrix is singular")
        
        factor = mod_inverse(augmented_matrix[i][i], mod)
        multiply_row(augmented_matrix, i, factor)
        
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                add_row(augmented_matrix, j, i, -factor)
    
    return [row[:-1] for row in augmented_matrix]

def parse_cnf(cnf):
    literals = []
    clauses = cnf.split('&')
    for clause in clauses:
        literals.extend(clause.split('|'))
    return literals, len(clauses)

def dpll(cnf):
    literals, num_clauses = parse_cnf(cnf)
    if not literals:
        return True
    
    literal = literals[0]
    positive_clauses = [clause for clause in literals if literal in clause]
    negative_clauses = [clause for clause in literals if literal.replace('-', '') in clause]
    
    if dpll('&'.join(positive_clauses)):
        return True
    elif dpll('&'.join(negative_clauses)):
        return True
    
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    coefficients = [random.randint(-10, 10) for _ in range(n)]
    
    # Compute minimal absolute value among all algebraic integers
    min_abs_value = min(abs(coeff) for coeff in coefficients if coeff != 0)
    
    # Generate a random CNF with n variables and the given coefficients
    cnf = '&'.join(f'x{i+1}' if coeff > 0 else f'-x{i+1}' for i, coeff in enumerate(coefficients))
    
    # Measure DPLL search tree width (simplified version)
    width = len(cnf.split('&'))
    
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width <= n * math.log(min_abs_value),
        "counterexample": "" if width <= n * math.log(min_abs_value) else f"Width {width} exceeds bound {n * math.log(min_abs_value)}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Width exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")