# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    
    # Forward elimination
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        
        pivot = A_augmented[i][i]
        for j in range(i, n+1):
            A_augmented[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = A_augmented[k][i]
                for j in range(i, n+1):
                    A_augmented[k][j] -= factor * A_augmented[i][j]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A_augmented[i][-1]
        for j in range(i+1, n):
            x[i] -= A_augmented[i][j] * x[j]
    
    return x

def matrix_multiply(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    if unit_clauses:
        var = unit_clauses[0]
        if var < 0:
            var = -var
        assignment[var] = var not in assignment or assignment[var] != 1
        return dpll([c for c in cnf if var not in c], assignment)
    
    var = random.choice(list(assignment.keys()) if assignment else range(1, len(cnf) + 1))
    new_assignment = assignment.copy()
    new_assignment[var] = True
    if dpll(cnf, new_assignment):
        return True
    
    new_assignment[var] = False
    return dpll(cnf, new_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    cnf = []
    variables = set()
    
    for _ in range(m):
        clause = []
        while not clause or len(clause) == len(variables):
            var = random.randint(-n, n)
            if var != 0 and -var not in clause:
                clause.append(var)
                variables.add(abs(var))
        cnf.append(clause)
    
    h_DPLL = dpll(cnf)
    C_phi = len(gaussian_elimination([[1 if i == abs(j) else 0 for j in range(1, n + 1)] for i in range(n)], [1] * n))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": Fraction(C_phi, h_DPLL),
        "instances_tested": len(cnf),
        "n_max": n,
        "conjecture_holds": C_phi <= h_DPLL,
        "counterexample": "" if C_phi <= h_DPLL else f"Counterexample found with n={n}, m={m}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(r["metric_value"] > Fraction(8, 10) for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["metric_value"] > Fraction(8, 10)), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient > 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")