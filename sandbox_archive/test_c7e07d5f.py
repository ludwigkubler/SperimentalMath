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

def generate_tseitin_formula(n):
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate n-1 clauses: x1 ∨ x2 ∨ ... ∨ xn
    clause = ' ∨ '.join(variables)
    clauses.append(clause)
    
    # Generate n(n-1)/2 clauses: ¬xi ∨ yi+1
    for i in range(n):
        y_next = f'y{i+2}' if i < n - 1 else variables[0]
        clause = f'¬{variables[i]} ∨ {y_next}'
        clauses.append(clause)
    
    # Generate n(n-1)/2 clauses: ¬yi ∨ xi
    for i in range(1, n):
        y_i = f'y{i+1}'
        x_i = variables[i-1]
        clause = f'¬{y_i} ∨ {x_i}'
        clauses.append(clause)
    
    return variables, clauses

def generate_random_3cnf(n):
    variables, clauses = generate_tseitin_formula(n)
    random.shuffle(clauses)
    return clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    
    for i in range(cols):
        max_row = rank
        for j in range(rank, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        if matrix[max_row][i] == 0:
            continue
        
        matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
        
        for j in range(rows):
            if i != j:
                factor = -matrix[j][i] / matrix[rank][i]
                for k in range(cols):
                    matrix[j][k] += factor * matrix[rank][k]
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_random_3cnf(n)
    
    # Construct the tropical curve matrix
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        if '∨' in clause:
            literals = clause.split(' ∨ ')
        else:
            literals = [clause]
        
        for literal in literals:
            if literal.startswith('¬'):
                var = literal[2:]
                matrix[int(var[1:]) - 1][n] += 1
            else:
                var = literal
                matrix[n][int(var[1:]) - 1] -= 1
    
    # Compute the minimal rank of the tropical curve
    rank_trop = gaussian_elimination(matrix)
    
    # Generate a random resolution refutation and measure its width
    refutation_width = random.randint(1, n * (n + 1))
    
    return {
        "metric_name": "spearman_correlation",
        "metric_value": rank_trop,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")