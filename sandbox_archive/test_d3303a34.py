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
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
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

def permanent(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    perm = 0
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        perm += (-1)**i * A[0][i] * permanent(submatrix)
    return perm

def symmetric_square(A):
    n = len(A)
    B = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            B[i][j] = sum(A[k][i] * A[k][j] for k in range(n))
            B[j][i] = B[i][j]
    return B

def young_tableau_decomposition(matrix):
    n = len(matrix)
    tableaux = []
    def backtrack(row, col, path):
        if row == n:
            tableaux.append(path[:])
            return
        for i in range(col, n):
            if matrix[row][i] != 0:
                path.append((row, i))
                matrix[row][i] -= 1
                backtrack(row + 1, col, path)
                matrix[row][i] += 1
    backtrack(0, 0, [])
    return tableaux

def trivial_representation_multiplicity(tableau):
    n = len(tableau)
    mult = 1
    for row in tableau:
        for i in range(len(row) - 1):
            if row[i] == row[i+1]:
                mult *= (row[i] + 1) // gcd(row[i], row[i+1])
    return mult

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    perm_poly = permanent(A)
    det_poly = determinant(A)
    perm_sym_square = symmetric_square(A)
    det_sym_square = symmetric_square(A)
    
    perm_tableaux = young_tableau_decomposition(perm_sym_square)
    det_tableaux = young_tableau_decomposition(det_sym_square)
    
    perm_mult = sum(trivial_representation_multiplicity(tableau) for tableau in perm_tableaux)
    det_mult = sum(trivial_representation_multiplicity(tableau) for tableau in det_tableaux)
    
    metric_name = "trivial_representation_multiplicity"
    metric_value = perm_mult - det_mult
    instances_tested = 1
    conjecture_holds = perm_mult > det_mult
    counterexample = "" if conjecture_holds else f"Permanent: {perm_mult}, Determinant: {det_mult}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")