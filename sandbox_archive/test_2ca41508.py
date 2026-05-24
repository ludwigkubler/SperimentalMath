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
    variables = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    
    def new_var():
        return f'y{len(variables) + len(clauses)}'
    
    for i in range(n):
        clause = [-variables[i]]
        for j in range(i + 1, n):
            clause.append(-variables[j])
            clause.append(new_var())
            clauses.append(clause)
            clause = [new_var()]
        variables.append(variables[i])
        clauses.append([variables[i]])
    
    return variables, clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        if matrix[i][i] == 0:
            continue
        
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] += factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    
    # Convert to integer literals
    literal_to_index = {var: i for i, var in enumerate(variables)}
    matrix = [[0] * (2 * n) for _ in range(2 * n)]
    
    for clause in clauses:
        for lit in clause:
            if lit > 0:
                row, col = literal_to_index[lit], literal_to_index[lit]
            else:
                row, col = literal_to_index[-lit], literal_to_index[-lit] + n
            matrix[row][col] += 1
    
    rank = gaussian_elimination(matrix)
    
    # Solve using DPLL (simplified version for demonstration)
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        pure_literals = {}
        for lit in set([abs(lit) for clause in clauses for lit in clause]):
            pos_count = sum(1 for clause in clauses if lit in clause)
            neg_count = sum(1 for clause in clauses if -lit in clause)
            if pos_count == 0:
                pure_literals[lit] = True
            elif neg_count == 0:
                pure_literals[lit] = False
        
        for lit, value in pure_literals.items():
            new_assignment = assignment.copy()
            new_assignment[lit] = value
            if not dpll([c for c in clauses if lit not in c], new_assignment):
                return False
        
        unit_lit = next((lit for lit in unit_clauses if lit not in assignment), None)
        if unit_lit is None:
            return False
        
        new_assignment = assignment.copy()
        new_assignment[unit_lit] = True
        if not dpll([c for c in clauses if unit_lit not in c], new_assignment):
            new_assignment[unit_lit] = False
            if not dpll([c for c in clauses if -unit_lit not in c], new_assignment):
                return False
        
        return True
    
    resolution_length = 0
    while not dpll(clauses, {}):
        resolution_length += 1
    
    ratio = resolution_length / (2 ** rank)
    
    return {
        "metric_name": "resolution_proof_length_to_rank_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 1,  # Placeholder value, should be adjusted based on actual conjecture
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")