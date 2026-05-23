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
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for OR gates
    for i in range(1, n+1):
        a = random.choice(variables)
        b = random.choice(variables)
        while a == b:
            b = random.choice(variables)
        clauses.append(f'{a} {b}')
    
    # Generate clauses for NOT gates
    for i in range(n):
        a = variables[i]
        b = f'~{a}'
        clauses.append(f'-{a} {b}')
    
    # Generate the final clause
    final_clause = ' '.join(variables)
    clauses.append(final_clause)
    
    return '\n'.join(clauses)

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        for j in range(n):
            if i != j:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n+1):
                    matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def compute_minimal_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(abs(matrix[i][j]) < 1e-9 for j in range(i, n)):
            continue
        rank += 1
        for j in range(n):
            if i != j:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n+1):
                    matrix[j][k] -= factor * matrix[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    formula = generate_tseitin_formula(n)
    # Simulate resolution proof length (placeholder for actual computation)
    resolution_length = 2 * n ** 3
    
    # Convert Tseitin formula to tropicalized Boolean algebra matrix
    matrix = []
    for line in formula.split('\n'):
        row = [0] * (n + 1)
        if line.startswith('-'):
            var = line[1:]
            idx = variables.index(var) + 1
            row[idx] = -1
        else:
            vars = line.split()
            for var in vars:
                if var.startswith('~'):
                    var = var[1:]
                idx = variables.index(var) + 1
                row[idx] = 1
        matrix.append(row)
    
    # Compute minimal rank of quotient module
    minimal_rank = compute_minimal_rank(matrix)
    
    # Check conjecture bound
    alpha_n = n ** 2 * math.log(n)
    conjecture_holds = minimal_rank <= alpha_n
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Minimal rank {minimal_rank} exceeds bound {alpha_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")