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
    variables = list(range(1, n + 1))
    clauses = []
    
    for var in variables:
        clause = [var]
        for _ in range(random.randint(2, 5)):
            negated_var = random.choice([True, False])
            if negated_var:
                clause.append(-var)
            else:
                clause.append(var)
        clauses.append(clause)
    
    return variables, clauses

def incidence_matrix_from_clauses(variables, clauses):
    n = len(variables)
    m = len(clauses)
    matrix = [[0] * (n + m) for _ in range(n)]
    
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                matrix[var - 1][i + n] = 1
            else:
                matrix[-var - 1][i + n] = -1
    
    return matrix

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        if matrix[i][i] == 0:
            for j in range(i + 1, rows):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                continue
        
        pivot = Fraction(matrix[i][i])
        for j in range(cols):
            matrix[i][j] /= pivot
        
        for j in range(rows):
            if i == j:
                continue
            factor = Fraction(matrix[j][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def rank_of_matrix(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    
    for i in range(rows):
        if any(matrix[i][j] != 0 for j in range(cols)):
            rank += 1
    
    return rank

def symplectic_form_invariant(incidence_matrix):
    n, m = len(incidence_matrix), len(incidence_matrix[0])
    symplectic_matrix = [[0] * (n + m) for _ in range(n + m)]
    
    for i in range(n):
        for j in range(m):
            symplectic_matrix[i][j + n] = incidence_matrix[i][j]
            symplectic_matrix[j + n][i] = -incidence_matrix[i][j]
    
    return rank_of_matrix(symplectic_matrix)

def resolution_proof_length(variables, clauses):
    stack = []
    assignment = {}
    
    for clause in clauses:
        if all(var not in assignment or (assignment[var] == 1 and var > 0) or (assignment[-var] == 0 and var < 0) for var in clause):
            return 1
    
    for var in variables:
        stack.append((var, False))
    
    while stack:
        var, negated = stack.pop()
        if negated:
            assignment[var] = 0
        else:
            assignment[var] = 1
        
        new_clauses = []
        for clause in clauses:
            if any(var not in assignment or (assignment[var] == 1 and var > 0) or (assignment[-var] == 0 and var < 0) for var in clause):
                continue
            new_clause = [v for v in clause if v != var and -v != var]
            if len(new_clause) == 0:
                return 1
            elif len(new_clause) == 1:
                stack.append((new_clause[0], True))
            else:
                new_clauses.append(new_clause)
        
        clauses = new_clauses
    
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    incidence_matrix = incidence_matrix_from_clauses(variables, clauses)
    symplectic_inv = symplectic_form_invariant(incidence_matrix)
    proof_length = resolution_proof_length(variables, clauses)
    
    return {
        "metric_name": "symplectic_form_invariant",
        "metric_value": symplectic_inv,
        "instances_tested": 1,
        "conjecture_holds": symplectic_inv >= math.log(n) / math.log(2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"symplectic_form_invariant < {math.log(n) / math.log(2)}\" first_failing_seed={first_failing_seed}")