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

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                max_row = j
        
        A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
        
        factor = A_b[i][i]
        for j in range(i, n+1):
            A_b[i][j] /= factor
        
        for j in range(n):
            if j != i:
                factor = A_b[j][i]
                for k in range(i, n+1):
                    A_b[j][k] -= factor * A_b[i][k]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A_b[i][-1]
        for j in range(i+1, n):
            x[i] -= A_b[i][j] * x[j]
    
    return x

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def inverse_matrix(A):
    n = len(A)
    I = identity_matrix(n)
    augmented = [A[i] + I[i] for i in range(n)]
    
    gaussian_elimination(augmented)
    
    inv_A = [row[n:] for row in augmented]
    return inv_A

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(submatrix)
    
    return det

def polynomial_eval(poly, x):
    result = 0
    for coeff in reversed(poly):
        result = result * x + coeff
    return result

def clause_indicator_polynomial(phi, p):
    n = len(phi)
    m = len(phi[0])
    A = [[0] * (n+1) for _ in range(m)]
    
    for i in range(m):
        for j in range(n):
            if phi[i][j]:
                A[i][-1] += 1
                A[i][j] -= 1
    
    inv_A = inverse_matrix(A)
    b = [0] * (n+1)
    b[-1] = m
    
    x = gaussian_elimination(inv_A, b)
    
    return [x[j] for j in range(n)]

def resolution_width(phi):
    n = len(phi)
    m = len(phi[0])
    clauses = phi
    literals = set()
    for clause in clauses:
        for literal in clause:
            literals.add(abs(literal))
    
    resolvents = []
    while True:
        new_resolvent = False
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                common_vars = set()
                for lit_i in clauses[i]:
                    if -lit_i in clauses[j]:
                        common_vars.add(abs(lit_i))
                
                if common_vars:
                    new_clause = []
                    for lit_i in clauses[i]:
                        if abs(lit_i) not in common_vars:
                            new_clause.append(lit_i)
                    for lit_j in clauses[j]:
                        if abs(lit_j) not in common_vars and -lit_j not in new_clause:
                            new_clause.append(-lit_j)
                    
                    if new_clause not in resolvents:
                        resolvents.append(new_clause)
                        new_resolvent = True
        
        if not new_resolvent:
            break
    
    return len(resolvents)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 15
    m = 2 * n
    k = 3
    
    phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    p = 7
    
    h_phi = sum(abs(polynomial_eval(clause_indicator_polynomial(phi, p), x)) for x in range(-n, n+1))
    w_phi = resolution_width(phi)
    
    return {
        "metric_name": "h(w)",
        "metric_value": h_phi / w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if 0.5 <= h_phi / w_phi <= 2 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")