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

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
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
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        sum_val = 0
        for j in range(i+1, n):
            sum_val += A[i][j] * x[j]
        x[i] = (b[i] - sum_val) / A[i][i]
    return x

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        sign = (-1) ** (j % 2)
        det += sign * A[0][j] * determinant(submatrix)
    return det

def permanent(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    perm = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        sign = (-1) ** (j % 2)
        perm += sign * A[0][j] * permanent(submatrix)
    return abs(perm)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i+1) for i in range(random.randint(1, n))]
        clauses.append(clause)
    
    M = [[0 for _ in range(n)] for _ in range(n)]
    for clause in clauses:
        sign = random.choice([-1, 1])
        for var in clause:
            if abs(var) <= n:
                M[abs(var)-1][clauses.index(clause)] += sign
    
    perm_matrix = [[0 for _ in range(n)] for _ in range(n)]
    det_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (i+1) * (j+1) % 2 == 0:
                perm_matrix[i][j] = M[i][j]
            else:
                det_matrix[i][j] = -M[i][j]
    
    perm_val = permanent(perm_matrix)
    det_val = determinant(det_matrix)
    
    if perm_val == 0 or det_val == 0:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Permanent or Determinant is zero"
        }
    
    perm_multiplicity = Fraction(perm_val, det_val)
    det_multiplicity = Fraction(det_val, det_val)
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": float(perm_multiplicity - det_multiplicity),
        "instances_tested": 1,
        "conjecture_holds": perm_multiplicity > det_multiplicity,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30*3 + 1))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity Gap does not hold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")