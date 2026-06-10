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

def inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0] * n for _ in range(n)]
    det = determinant(matrix, mod)
    inv_det = inverse(det, mod)

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
        det += (-1) ** j * matrix[0][j] * determinant(minor, mod)
    return det % mod

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

def matrix_multiply(A, B, mod):
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

def matrix_subtract(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] - B[i][j]) % mod
    return C

def matrix_power(matrix, k, mod):
    result = [[(i == j) * 1 for j in range(len(matrix))] for i in range(len(matrix))]
    base = matrix
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, base, mod)
        base = matrix_multiply(base, base, mod)
        k //= 2
    return result

def generate_tseitin_formula(n):
    literals = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    
    for i in range(1, n + 1):
        clause = f'{literals[0]} {literals[i-1]} -{literals[i]}'
        clauses.append(clause)
    
    for i in range(n):
        clause = f'-{literals[i]} {literals[n+i+1]}'
        clauses.append(clause)
    
    for i in range(1, n + 1):
        clause = f'{literals[0]} -{literals[i-1]} {literals[n+i+1]}'
        clauses.append(clause)
    
    return literals, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        literals, clauses = generate_tseitin_formula(n)
        num_clauses = len(clauses)
        
        # Construct the polynomial system
        A = [[0] * (n + 1) for _ in range(num_clauses)]
        b = [0] * num_clauses
        
        for i, clause in enumerate(clauses):
            parts = clause.split()
            if parts[0] == '-':
                literal = parts[1]
                j = int(literal[1:]) - 1
                A[i][j] = -1
            else:
                literal = parts[0]
                j = int(literal[1:]) - 1
                A[i][j] = 1
        
        # Add the constant term
        for i in range(num_clauses):
            b[i] = 1
        
        # Solve the system using Gaussian elimination
        n_vars = len(A[0])
        augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0]) - 1
            for i in range(rows):
                max_row = i
                for j in range(i + 1, rows):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                
                pivot = matrix[i][i]
                for j in range(i, cols + 1):
                    matrix[i][j] /= pivot
                
                for j in range(rows):
                    if j != i:
                        factor = matrix[j][i]
                        for k in range(i, cols + 1):
                            matrix[j][k] -= factor * matrix[i][k]
            
            return [row[:-1] for row in matrix]
        
        solution = gaussian_elimination(augmented_matrix)
        
        # Calculate the minimal diophantine degree
        dd = max([abs(coeff) for coeff in solution])
        
        # Calculate the Frege proof length (simplified heuristic)
        f_phi = num_clauses * n
        
        results.append({
            "n": n,
            "dd": dd,
            "f_phi": f_phi
        })
    
    if not results:
        return {
            "metric_name": "minimal_diophantine_degree",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    dd_values = [result["dd"] for result in results]
    f_phi_values = [result["f_phi"] for result in results]
    
    mean_dd = sum(dd_values) / len(dd_values)
    std_dd = math.sqrt(sum((x - mean_dd) ** 2 for x in dd_values) / len(dd_values))
    mean_f_phi = sum(f_phi_values) / len(f_phi_values)
    std_f_phi = math.sqrt(sum((x - mean_f_phi) ** 2 for x in f_phi_values) / len(f_phi_values))
    
    correlation_coefficient = (sum((dd_values[i] - mean_dd) * (f_phi_values[i] - mean_f_phi) for i in range(len(dd_values))) /
                               (len(dd_values) * std_dd * std_f_phi))
    
    conjecture_holds = correlation_coefficient >= 0.8 and max(dd_values) <= 2 * mean_dd
    
    return {
        "metric_name": "minimal_diophantine_degree",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([result["n"] for result in results]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"dd > 2 * mean_dd (max dd={max(dd_values)}, mean dd={mean_dd})"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dd > 2 * mean_dd\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")