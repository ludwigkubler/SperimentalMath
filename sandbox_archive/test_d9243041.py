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
import math
from fractions import Fraction
import sys

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
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_mul(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_sub(A, B, mod):
    m = len(A)
    n = len(A[0])
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            C[i][j] = (A[i][j] - B[i][j]) % mod
    return C

def matrix_add(A, B, mod):
    m = len(A)
    n = len(A[0])
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            C[i][j] = (A[i][j] + B[i][j]) % mod
    return C

def matrix_transpose(A):
    m = len(A)
    n = len(A[0])
    B = [[0]*m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            B[j][i] = A[i][j]
    return B

def dpll(cnf):
    def search(assignments):
        unsatisfied_clauses = [c for c in cnf if not any(lit in assignments or -lit in assignments for lit in c)]
        if not unsatisfied_clauses:
            return True
        pure_literal = next((lit for lit in range(1, n+1) if all(lit not in c or -lit not in c for c in unsatisfied_clauses)), None)
        if pure_literal is None:
            return False
        assignments[pure_literal] = 1
        if search(assignments):
            return True
        del assignments[pure_literal]
        assignments[-pure_literal] = 1
        return search(assignments)
    n = max(abs(lit) for clause in cnf for lit in clause)
    assignments = {}
    return search(assignments)

def min_order(p, cnf):
    # Placeholder function to compute the minimal order of modular forms
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, 10)

def generate_cnf(n):
    num_clauses = random.randint(2*n, 3*n)
    clauses = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 2:
            lit = random.randint(-n, n)
            if lit != 0 and -lit not in clause:
                clause.add(lit)
        clauses.append(list(clause))
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        min_order_values = [min_order(p, cnf) for p in range(2, 10)]
        width = dpll(cnf)
        
        if len(min_order_values) == 0 or width is None:
            return {
                "metric_name": "correlation",
                "metric_value": float('nan'),
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append({
            "min_order_values": min_order_values,
            "width": width
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": len(results),
            "n_max": max(n for n in n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    min_order_all = [result["min_order_values"] for result in results]
    width_all = [result["width"] for result in results]
    
    mean_min_order = sum(sum(min_order) / len(min_order) for min_order in min_order_all) / len(n_values)
    mean_width = sum(width_all) / len(width_all)
    
    correlation_coefficient = 0
    for i in range(len(min_order_all)):
        for j in range(len(min_order_all[i])):
            correlation_coefficient += (min_order_all[i][j] - mean_min_order) * (width_all[j] - mean_width)
    correlation_coefficient /= len(min_order_all) * len(min_order_all[0])
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * len(min_order_all))))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n in n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {seed} {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_inconsistent_results")