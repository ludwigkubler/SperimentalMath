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

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for OR conditions
    for i in range(1, n+1):
        clause = f'({variables[i-1]} v {variables[n+i-1]})'
        clauses.append(clause)
    
    # Generate clauses for AND conditions
    for i in range(n+1, 2*n+1):
        clause = f'({variables[i-n-1]} v {variables[i-1]} v ~{variables[2*n-i+1]})'
        clauses.append(clause)
    
    # Final clause
    final_clause = 'v'.join([f'~{variables[i-1]}' for i in range(1, n+1)])
    clauses.append(final_clause)
    
    return clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find the pivot row
        max_row = i
        for j in range(i+1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, rows):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] += factor * matrix[i][k]
    
    return matrix

def is_independent(matrix):
    rank = 0
    for row in gaussian_elimination(matrix):
        if any(row):
            rank += 1
    return rank == len(matrix)

def tropical_coordinate_values(clauses):
    variables = set()
    for clause in clauses:
        for var in clause.split():
            if var.startswith('x'):
                variables.add(var)
    
    n = len(variables)
    matrix = [[0] * (n + 1) for _ in range(n)]
    
    for i, var in enumerate(variables):
        for clause in clauses:
            if var in clause and '~' not in clause:
                matrix[i][i] += 1
            elif f'~{var}' in clause:
                matrix[i][i] -= 1
    
    return is_independent(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        clauses = generate_tseitin_formula(n)
        if not clauses:
            return {
                "metric_name": "Ratio",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        t_values = [tropical_coordinate_values(clauses) for _ in range(5)]
        if any(t is None for t in t_values):
            return {
                "metric_name": "Ratio",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        min_t = min(t_values)
        if min_t <= 0:
            continue
        
        ratio = sum(2**min_t for _ in range(5)) / len(t_values)
        ratios.append(ratio)
    
    mean_ratio = sum(ratios) / len(ratios)
    conjecture_holds = all(r < 2**min([tropical_coordinate_values(generate_tseitin_formula(n)) for n in [5, 10, 15, 20, 30, 40]]) for r in ratios)
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(ratios),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(r is not None for r in results):
        mean_ratio = sum(results) / len(results)
        support_fraction = sum(1 for r in results if r < 2**min([tropical_coordinate_values(generate_tseitin_formula(n)) for n in [5, 10, 15, 20, 30, 40]])) / len(results)
        
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=NA")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")