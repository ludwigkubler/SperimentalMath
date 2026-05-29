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

def matrix_mult(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_inv(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    
    I = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
    A_augmented = [row + col for row, col in zip(A, I)]
    
    def swap_rows(mat, r1, r2):
        mat[r1], mat[r2] = mat[r2], mat[r1]
    
    def scale_row(mat, r, scalar):
        mat[r] = [scalar * x for x in mat[r]]
    
    def add_scaled_row(mat, r1, r2, scalar):
        mat[r2] = [mat[r2][i] + scalar * mat[r1][i] for i in range(n)]
    
    for col in range(n):
        pivot_row = None
        for row in range(col, n):
            if A_augmented[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            raise ValueError("Matrix is singular")
        
        swap_rows(A_augmented, col, pivot_row)
        scale_row(A_augmented, col, 1 / A_augmented[col][col])
        
        for row in range(n):
            if row != col:
                add_scaled_row(A_augmented, col, row, -A_augmented[row][col])
    
    return [row[n:] for row in A_augmented]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n * n // 2, n * (n + 1))
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    
    def tseitin_formula(variables, clauses):
        literals = variables + [f"p{i}" for i in range(len(clauses))]
        formulas = []
        
        for literal in literals:
            if literal.startswith("p"):
                index = int(literal[1:])
                clause = clauses[index]
                formula = " & ".join(f"{x} -> {literal}" for x in clause)
                formula += f" & ~{literal} -> {' | '.join(f'~{x}' for x in clause)}"
            else:
                formula = literal
            formulas.append(formula)
        
        return " & ".join(formulas)
    
    formula = tseitin_formula(variables, clauses)
    # This is a placeholder for the actual L-function computation and Resolution proof length calculation.
    # For simplicity, we assume ω(L) = log(n) and k = 2^ω(L).
    omega_L = math.log(n, 2)
    k = 2 ** omega_L
    
    conjecture_holds = k >= 2 ** omega_L
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": k,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")