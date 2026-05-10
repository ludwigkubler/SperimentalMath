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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def is_solution(x, A, b, tol=1e-6):
    return all(abs(sum(A[i][j] * x[j] for j in range(len(x))) - b[i]) < tol for i in range(len(b)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    clauses = [tuple(random.sample(range(n), 3)) for _ in range(n)]
    variables = set(var for clause in clauses for var in clause)
    m = len(variables)
    
    # Construct Coxeter group element
    C = [[0] * (m + 1) for _ in range(m + 1)]
    for i, j in combinations(range(m), 2):
        if any(i in clause and j in clause for clause in clauses):
            C[i][j], C[j][i] = -1, -1
    for i in range(m):
        C[i][m], C[m][i] = 1, 1
    C[m][m] = 0
    
    # Compute Coxeter polynomial using Chevalley's formula
    def chevalley(C, x):
        n = len(C)
        A = [[C[i][j] for j in range(n)] for i in range(n)]
        b = [sum(C[i][n]) for i in range(n)]
        return sum((-1)**i * math.factorial(i) * det(A[:i+1][:i+1]) for i in range(n))
    
    def det(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det_val = 0
            for j in range(n):
                det_val += ((-1)**j) * matrix[0][j] * det([row[:j] + row[j+1:] for row in matrix[1:]])
            return det_val
    
    x = gaussian_elimination(C, [0] * (m + 1))
    if not is_solution(x, C, [0] * (m + 1)):
        return {
            "metric_name": "Coxeter Polynomial Root Count",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Measure resolution proof length
    def dpll_with_clause_learning(clauses, assignment):
        stack = []
        while clauses:
            unit_clauses = [c for c in clauses if len(c) == 1]
            if not unit_clauses:
                break
            literal = unit_clauses[0][0]
            assignment[literal] = True
            clauses = [c for c in clauses if literal not in c and -literal not in c]
            stack.append((literal, assignment.copy()))
        return len(stack)
    
    resolution_length = dpll_with_clause_learning(clauses, {})
    
    # Count distinct roots of the Coxeter polynomial
    roots = set()
    for i in range(100):
        x = [random.uniform(-2, 2) for _ in range(m + 1)]
        if abs(chevalley(C, x)) < 1e-6:
            roots.add(tuple(sorted(x)))
    
    # Verify the conjecture
    metric_value = len(roots)
    conjecture_holds = metric_value >= math.log2(resolution_length) + 1
    counterexample = "" if conjecture_holds else f"resolution_length={resolution_length}, root_count={len(roots)}"
    
    return {
        "metric_name": "Coxeter Polynomial Root Count",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")