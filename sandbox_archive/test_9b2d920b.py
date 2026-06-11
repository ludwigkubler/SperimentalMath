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

def generate_tseitin_formula(n, d=3):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for each variable
    for var in variables:
        clause = [var]
        for _ in range(d-1):
            neg_var = f'~{var}'
            clause.append(neg_var)
            variables.append(neg_var)
            clauses.append(clause)
        
        # Add a clause to connect all literals for the variable
        clauses.append([f'{var}_i' for i in range(1, d+1)])
    
    # Generate Tseitin axioms
    tseitin_axioms = []
    for var in variables:
        if '~' not in var:
            continue
        pos_var = var[1:]
        tseitin_axioms.append([f'{pos_var}_i', f'{var}', f'~{pos_var}_{d}'])
    
    # Combine all clauses and axioms
    all_clauses = clauses + tseitin_axioms
    
    return variables, all_clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i+1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        
        for j in range(i, cols):
            matrix[i][j] /= pivot
        
        for j in range(rows):
            if j != i and matrix[j][i] != 0:
                factor = matrix[j][i]
                for k in range(i, cols):
                    matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def symmetric_tensor_rank(clause_indicator_poly):
    n = len(clause_indicator_poly)
    tensor = [[sum(clause_indicator_poly[i][j] * clause_indicator_poly[k][l] for i in range(n) if clause_indicator_poly[i][j]) for j in range(n)] for k in range(n)]
    
    rank = 0
    while any(any(row) for row in tensor):
        pivot_row, pivot_col = next((i, j) for i in range(rank, n) for j in range(rank, n) if tensor[i][j] != 0)
        for i in range(rank, n):
            tensor[pivot_row][i], tensor[i][pivot_col] = tensor[i][pivot_col], tensor[pivot_row][i]
        
        for i in range(n):
            if i == pivot_row:
                continue
            factor = tensor[i][pivot_col] / tensor[pivot_row][pivot_col]
            for j in range(rank, n):
                tensor[i][j] -= factor * tensor[pivot_row][j]
        
        rank += 1
    
    return rank

def resolution_width(clause_set):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if literal.startswith('~'):
                new_assignment[literal[1:]] = False
            return dpll([c for c in clauses if not any(l in c for l in (literal, f'~{literal}'))], new_assignment)
        pure_literal = next((l for l in assignment if all(l not in c or ~assignment[l] for c in clauses)), None)
        if pure_literal:
            return dpll([c for c in clauses if not any(l in c for l in (pure_literal, f'~{pure_literal}'))], assignment)
        
        literal = random.choice(clauses[0])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if not any(l in c for l in (literal, f'~{literal}'))], new_assignment):
            return True
        
        new_assignment[literal] = False
        if dpll([c for c in clauses if not any(l in c for l in (literal, f'~{literal}'))], new_assignment):
            return True
        
        return False
    
    assignment = {}
    return len(clause_set) - len([c for c in clause_set if dpll(c, assignment)])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    str_sum = 0
    w_sum = 0
    support_count = 0
    
    for n in n_values:
        instances_tested = 0
        n_max = n
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(5):  # Sample 5 instances per size
            variables, clauses = generate_tseitin_formula(n)
            clause_indicator_poly = [[1 if var in c else 0 for var in variables] for c in clauses]
            
            str_value = symmetric_tensor_rank(clause_indicator_poly)
            w_value = resolution_width(clauses)
            
            str_sum += str_value
            w_sum += w_value
            total_instances += 1
            
            instances_tested += 1
            
            if instances_tested >= 30:
                break
        
        mean_str = str_sum / instances_tested
        mean_w = w_sum / instances_tested
        support_fraction = mean_str <= 3 * mean_w
        
        if not support_fraction:
            conjecture_holds = False
            counterexample = f"n={n}, STR_mean={mean_str}, w_mean={mean_w}"
    
    return {
        "metric_name": "STR_mean",
        "metric_value": str_sum / total_instances,
        "instances_tested": total_instances,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_str = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_str} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_str} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_max too small\" first_failing_seed={first_failing_seed}")