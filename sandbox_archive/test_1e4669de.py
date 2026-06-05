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
        pivot = A_b[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(i, n+1):
            A_b[i][j] /= pivot
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
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll(cnf, assignment=None):
    if assignment is None:
        assignment = {}
    
    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    for clause in unit_clauses:
        literal = clause[0]
        if literal in assignment and assignment[literal] != (literal > 0):
            return False
        assignment[literal] = literal > 0
    
    pure_literals = {}
    for literal in set.union(*cnf):
        positive_count = sum(1 for c in cnf if literal in c)
        negative_count = sum(1 for c in cnf if -literal in c)
        if positive_count == 0:
            pure_literals[literal] = True
        elif negative_count == 0:
            pure_literals[-literal] = True
    
    for literal, value in pure_literals.items():
        if literal in assignment and assignment[literal] != value:
            return False
        assignment[literal] = value
    
    if not cnf:
        return True
    
    literal = next(l for l in set.union(*cnf) if l not in assignment)
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    if dpll(cnf, new_assignment):
        return True
    
    new_assignment[literal] = False
    return dpll(cnf, new_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    cnf = []
    for _ in range(10 * n):  # Generate multiple clauses to ensure variety
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause.reverse()
        cnf.append(clause)
    
    A = [[0] * (2 * n) for _ in range(n)]
    b = [0] * n
    for i in range(n):
        for j in range(n):
            A[i][j] = 1 if i == j else -1 if i == j + n else 0
    
    try:
        gaussian_elimination(A, b)
    except ValueError as e:
        return {
            "metric_name": "min_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    min_order = sum(1 for row in A if any(x != 0 for x in row))
    
    w_phi = dpll(cnf)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_order <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"min_order > 10\" first_failing_seed={first_failing_seed}")