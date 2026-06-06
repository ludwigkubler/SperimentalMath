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

def generate_random_cnf(n, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = -clause[0], -clause[1]
        cnf.append(clause)
    return cnf

def matrix_multiplication(A, B):
    m = len(A)
    k = len(B)
    n = len(B[0])
    result = [[Fraction(0) for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                result[i][j] += A[i][l] * B[l][j]
    return result

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * determinant(submatrix)
        sign *= -1
    return det

def trace(matrix):
    n = len(matrix)
    return sum(matrix[i][i] for i in range(n))

def frobenius_schur_indicator(matrix):
    det = determinant(matrix)
    if det == 0:
        return None
    tr = trace(matrix)
    return abs(tr / det)

def resolution_proof_width(cnf):
    n = len(cnf)
    clauses = [set(clause) for clause in cnf]
    stack = []
    while True:
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if not unit_clause:
            return len(stack)
        var = list(unit_clause)[0]
        stack.append(var)
        new_clauses = []
        for clause in clauses:
            if var in clause:
                continue
            if -var in clause:
                new_clauses.append(clause - {var, -var})
            else:
                new_clauses.append(clause)
        clauses = new_clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_random_cnf(n, 2 * n)
        matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for clause in cnf:
            i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
            if clause[0] > 0 and clause[1] > 0:
                matrix[i][j] += Fraction(1)
            elif clause[0] < 0 and clause[1] < 0:
                matrix[i][j] -= Fraction(1)
        
        fsi = frobenius_schur_indicator(matrix)
        if fsi is None:
            continue
        
        w_phi = resolution_proof_width(cnf)
        results.append((fsi, w_phi))
    
    if not results:
        return {
            "metric_name": "FSI vs. Resolution Width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    fsi_values, w_phi_values = zip(*results)
    correlation_coefficient = sum((fsi - mean_fsi) * (w_phi - mean_w_phi) for fsi, w_phi in results) / len(results)
    mean_absolute_difference = sum(abs(fsi - w_phi) for fsi, w_phi in results) / len(results)
    
    return {
        "metric_name": "FSI vs. Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_absolute_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")