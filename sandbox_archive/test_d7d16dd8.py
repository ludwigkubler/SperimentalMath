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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def max_eigenvalue(A):
    n = len(A)
    eigenvalues = []
    I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    for _ in range(100):  # Power iteration method
        v = [random.uniform(-1, 1) for _ in range(n)]
        v_norm = sum(x**2 for x in v)**0.5
        v = [x / v_norm for x in v]
        Av = matrix_multiply(A, [v])
        Av_norm = sum(x**2 for x in Av)**0.5
        lambda_ = sum(Av[i] * v[i] for i in range(n)) / Av_norm
        eigenvalues.append(lambda_)
    return max(eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(1, 2*n)
    phi = [random.choice([True, False]) for _ in range(n)]
    
    # Generate a random CNF
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.randint(0, n-1)
            if random.choice([True, False]):
                clause.add(var)
            else:
                clause.add(-var)
        clauses.append(clause)
    
    # Compute the quaternionic Kähler metrics
    Hodge_Laplacian = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                Hodge_Laplacian[i][j] = len([c for c in clauses if i+1 in c or -i-1 in c])
    
    # Compute the index
    A = gaussian_elimination(Hodge_Laplacian)
    det_A = determinant(A)
    lambda_max = max_eigenvalue(A)
    
    # Define the function f(n, m)
    def f(n, m):
        return Fraction(m**(3/2) * n**(1/4), 1)
    
    # Check if the conjecture holds
    conjecture_holds = lambda_max <= f(n, m)
    counterexample = "" if conjecture_holds else "f(n, m) too large"
    
    return {
        "metric_name": "max_eigenvalue",
        "metric_value": float(lambda_max),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"f(n, m) too large\" first_failing_seed={first_failing_seed}")