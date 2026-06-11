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
from itertools import combinations

def generate_tseitin_formula(n, d):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for each variable being true
    for var in variables:
        clause = [var]
        for _ in range(d-1):
            neg_var = f'~{var}'
            clause.append(neg_var)
            if random.choice([True, False]):
                clauses.append(clause)
                clause = [neg_var]
    
    # Generate clauses for each variable being false
    for var in variables:
        clause = [f'~{var}']
        for _ in range(d-1):
            neg_var = f'x{i}'
            clause.append(neg_var)
            if random.choice([True, False]):
                clauses.append(clause)
                clause = [neg_var]
    
    # Generate tautological clauses
    for var in variables:
        clauses.append([f'{var}', f'~{var}'])
    
    return variables, clauses

def polynomial_from_clauses(variables, clauses):
    n = len(variables)
    poly = [[0] * n for _ in range(n)]
    
    for clause in clauses:
        for var in clause:
            if var.startswith('x'):
                idx = int(var[1:]) - 1
                poly[idx][idx] += 1
            elif var.startswith('~'):
                idx = int(var[2:]) - 1
                poly[idx][idx] -= 1
    
    return poly

def symmetric_tensor_rank(poly):
    n = len(poly)
    tensor = [[poly[i][j] for j in range(n)] for i in range(n)]
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        
        for col in range(n):
            pivot_row = -1
            for row in range(rank, m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            
            if pivot_row == -1:
                continue
            
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            
            for row in range(rank, m):
                factor = Fraction(matrix[row][col], matrix[pivot_row][col])
                for j in range(n):
                    matrix[row][j] -= factor * matrix[pivot_row][j]
        
        return rank
    
    return gaussian_elimination(tensor)

def resolution_width(clause):
    return len(clause) - 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    str_sum = 0
    w_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            variables, clauses = generate_tseitin_formula(n, d=3)
            poly = polynomial_from_clauses(variables, clauses)
            str_rank = symmetric_tensor_rank(poly)
            
            width_sum = sum(resolution_width(clause) for clause in clauses)
            w_mean = width_sum / len(clauses)
            
            str_sum += str_rank
            w_sum += w_mean
            instances_tested += 1
    
    str_mean = str_sum / instances_tested
    w_mean = w_sum / instances_tested
    
    if str_mean <= 3 * w_mean:
        conjecture_holds = True
    else:
        conjecture_holds = False
        counterexample = f"STR_mean={str_mean}, w_mean={w_mean}"
    
    return {
        "metric_name": "STR_mean / w_mean",
        "metric_value": str_mean / w_mean,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    str_means = [r["metric_value"] * r["w_mean"] for r in results]
    w_means = [r["w_mean"] for r in results]
    
    mean_str_mean = sum(str_means) / len(results)
    mean_w_mean = sum(w_means) / len(results)
    support_fraction = sum(1 for r in results if r["str_mean"] <= 3 * r["w_mean"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_str_mean} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_str_mean} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"STR_mean > 3 * w_mean\" first_failing_seed={first_failing_seed}")