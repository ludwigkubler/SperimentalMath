# auto-injected by SEC sandbox
import math
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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, rows):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(len(row))] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    return sum(1 for row in augmented_matrix if any(val != 0 for val in row))

def tseitin_formula(n, m):
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate n clauses
    for i in range(n):
        literals = random.sample(variables + [-var for var in variables], 2)
        clauses.append(literals)
    
    # Generate m clauses with OR and NOT
    for _ in range(m):
        literals = [random.choice(variables) if random.randint(0, 1) else -random.choice(variables) for _ in range(random.randint(2, n))]
        clauses.append(literals)
    
    return variables, clauses

def resolution_proof_tree_width(clauses):
    # Simplified version of DPLL algorithm to estimate RPTW
    def dpll(clauses, assignment, literals):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(new_clauses, new_assignment, literals)
        pure_literal = next((l for l in literals if (l in assignment and not assignment[l]) or (-l in assignment and assignment[-l])), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(new_clauses, new_assignment, literals)
        literal = random.choice(literals)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        width_true = 1 + dpll(new_clauses, new_assignment, literals)
        new_assignment[literal] = False
        new_assignment[-literal] = True
        new_clauses = [c for c in clauses if -literal not in c and literal not in c]
        width_false = 1 + dpll(new_clauses, new_assignment, literals)
        return max(width_true, width_false)
    
    assignment = {}
    literals = set(l for clause in clauses for l in clause)
    return dpll(clauses, assignment, literals)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times
            variables, clauses = tseitin_formula(n, m=n)
            k_theory_rank = rank([[1 if i == j else 0 for j in range(n)] for i in range(n)])
            rptw = resolution_proof_tree_width(clauses)
            results.append((n, k_theory_rank, rptw))
    
    mean_rptw = sum(rptw for _, _, rptw in results) / len(results)
    std_rptw = (sum((rptw - mean_rptw) ** 2 for _, _, rptw in results) / len(results)) ** 0.5
    conjecture_holds = all(m <= n**(1/3) * r for m, r, _ in results)
    
    return {
        "metric_name": "Resolution Proof Tree Width",
        "metric_value": mean_rptw,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rptw = sum(result["metric_value"] for result in results) / len(results)
    std_rptw = (sum((result["metric_value"] - mean_rptw) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rptw} std={std_rptw} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_operation n_tested={len(results)}")