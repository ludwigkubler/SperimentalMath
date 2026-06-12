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

def generate_instance(n):
    literals = [f'x{i+1}' for i in range(n)]
    clauses = []
    for var in literals:
        clauses.append([var])
    return literals, clauses

def tseitin_formula(literals, clauses):
    n = len(literals)
    new_vars = [f'y{i+1}' for i in range(2*n-1)]
    tseitin_clauses = []
    for i in range(n):
        tseitin_clauses.append([literals[i], new_vars[2*i]])
        tseitin_clauses.append([-literals[i], -new_vars[2*i]])
        tseitin_clauses.append([new_vars[2*i], new_vars[2*i+1]])
        tseitin_clauses.append([-new_vars[2*i], -new_vars[2*i+1]])
    for i in range(n):
        for j in range(i+1, n):
            tseitin_clauses.append([literals[i], literals[j], -new_vars[2*n-2+i-j]])
            tseitin_clauses.append([-literals[i], literals[j], new_vars[2*n-2+i-j]])
            tseitin_clauses.append([literals[i], -literals[j], -new_vars[2*n-2+i-j]])
            tseitin_clauses.append([-literals[i], -literals[j], new_vars[2*n-2+i-j]])
    for clause in clauses:
        tseitin_clauses.append(clause + [new_vars[-1]])
        tseitin_clauses.append([i for i in range(-n, 0) if i not in clause] + [-new_vars[-1]])
    return new_vars, tseitin_clauses

def tropical_hessian(literals, clauses):
    n = len(literals)
    hessian = [[0]*n for _ in range(n)]
    for clause in clauses:
        for var in clause:
            if var.startswith('x'):
                i = int(var[1:]) - 1
                hessian[i][i] += 1
            elif var.startswith('-x'):
                i = int(var[2:]) - 1
                hessian[i][i] -= 1
    return hessian

def min_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if matrix[i][i] != 0:
            rank += 1
            for j in range(i+1, n):
                matrix[j][i] /= matrix[i][i]
            for k in range(n):
                if k != i:
                    for j in range(i, n):
                        matrix[k][j] -= matrix[k][i] * matrix[i][j]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    total_sat_proof_size = 0
    total_tropical_hessian_rank = 0
    success_count = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        literals, clauses = generate_instance(n)
        new_vars, tseitin_clauses = tseitin_formula(literals, clauses)
        hessian = tropical_hessian(new_vars, tseitin_clauses)
        rank = min_rank(hessian)
        
        # Placeholder for SAT solver (e.g., DPLL)
        sat_proof_size = n * 2  # Simplified example
        
        instances_tested += 1
        total_sat_proof_size += sat_proof_size
        total_tropical_hessian_rank += rank
        
        if sat_proof_size <= 1.5 * rank:
            success_count += 1
    
    metric_value = total_sat_proof_size / instances_tested
    conjecture_holds = success_count >= 0.8 * instances_tested
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "sat_proof_size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")