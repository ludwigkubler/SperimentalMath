# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def generate_tseitin_formula(n):
    if n <= 0:
        return [], []
    
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for the OR part of Tseitin formula
    for i in range(1, n+1):
        clause = f'{literals[0]} {literals[i-1]} -{literals[i]}'
        clauses.append(clause)
    
    # Generate clauses for the AND part of Tseitin formula
    for i in range(2, n+1):
        clause = f'-{literals[0]} {literals[i-1]} {literals[i]}'
        clauses.append(clause)
    
    return literals, clauses

def generate_polynomial_system(literals, clauses):
    variables = set()
    polynomials = {}
    
    for literal in literals:
        variables.add(literal)
        polynomials[literal] = [literal]
    
    for clause in clauses:
        parts = clause.split()
        if len(parts) == 3 and parts[1] == '-':
            pos_var, neg_var = parts[0], parts[2]
            variables.add(pos_var)
            variables.add(neg_var)
            
            if pos_var not in polynomials:
                polynomials[pos_var] = [pos_var]
            if neg_var not in polynomials:
                polynomials[neg_var] = [-neg_var]
    
    return list(variables), polynomials

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find the maximum element in column i
        max_idx = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_idx][i]):
                max_idx = j
        
        # Swap rows i and max_idx
        A[i], A[max_idx] = A[max_idx], A[i]
        b[i], b[max_idx] = b[max_idx], b[i]
        
        # Eliminate non-zero elements below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    
    # Back-substitution to find the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def compute_diophantine_degree(polynomials):
    variables = set()
    for poly in polynomials.values():
        for term in poly:
            if isinstance(term, str):
                variables.add(term)
    
    n = len(variables)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    var_index = {var: i for i, var in enumerate(variables)}
    
    for poly in polynomials.values():
        degree = 1
        for term in poly:
            if isinstance(term, str):
                degree *= (1 + abs(var_index[term]))
        
        A[var_index[poly[0]]][var_index[poly[0]]] += degree
    
    x = gaussian_elimination(A, b)
    
    return max(abs(val) for val in x)

def compute_frege_proof_length(clauses):
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        literals, clauses = generate_tseitin_formula(n)
        variables, polynomials = generate_polynomial_system(literals, clauses)
        
        dd = compute_diophantine_degree(polynomials)
        f = compute_frege_proof_length(clauses)
        
        if dd > 2 * (sum(dd for _, dd in results) / len(results)) and len(results) >= 1:
            return {
                "metric_name": "diophantine_degree",
                "metric_value": dd,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"dd({n}) > 2 * mean(dd)"
            }
        
        results.append((dd, f))
    
    correlation = sum((dd - mean_dd) * (f - mean_f) for dd, f in results)
    correlation /= math.sqrt(sum((dd - mean_dd)**2 for dd, _ in results)) * math.sqrt(sum((f - mean_f)**2 for _, f in results))
    
    return {
        "metric_name": "diophantine_degree",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if all(r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.8)
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")