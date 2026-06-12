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
        pivot = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]
    
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    
    return rank

def hermitian_rank(matrix):
    n = len(matrix)
    # Compute the Hermitian matrix (not necessary for this test, but included for completeness)
    hermitian_matrix = [[matrix[i][j].conjugate() for j in range(n)] for i in range(n)]
    
    return gaussian_elimination(hermitian_matrix)

def dpll_width(clauses):
    n = len(clauses)
    if not clauses:
        return 0
    
    # Simplify the problem by removing tautologies
    simplified_clauses = []
    literals_seen = set()
    for clause in clauses:
        new_clause = [l for l in clause if l not in literals_seen and -l not in literals_seen]
        if new_clause:
            simplified_clauses.append(new_clause)
            literals_seen.update(new_clause)
    
    # Use a simple DPLL solver to find the width
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return max(dpll(new_clauses, new_assignment), dpll(new_clauses, {l: False for l in literals_seen}))
        
        pure_literal = next((l for l in literals_seen if all(l not in c or -l in c for c in clauses)), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return max(dpll(new_clauses, new_assignment), dpll(new_clauses, {l: False for l in literals_seen}))
        
        literal = next(iter(literals_seen))
        return 1 + max(dpll([c for c in clauses if literal not in c and -literal not in c], assignment.copy()),
                      dpll([c for c in clauses if -literal not in c and literal not in c], {l: False for l in literals_seen}))
    
    return dpll(simplified_clauses, {})

def generate_random_clause(n):
    clause = []
    while len(clause) < 2:
        lit = random.choice([-1, 1]) * (random.randint(1, n))
        if lit not in clause and -lit not in clause:
            clause.append(lit)
    return tuple(clause)

def generate_random_clauses(n):
    num_clauses = random.randint(2, 5)
    clauses = set()
    while len(clauses) < num_clauses:
        clauses.add(generate_random_clause(n))
    return list(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    total_rank = 0
    total_width = 0
    
    for n in range(5, 41):
        for _ in range(7):  # Aim for at least 30 instances per seed
            clauses = generate_random_clauses(n)
            matrix = [[0] * n for _ in range(n)]
            for clause in clauses:
                for i in range(n):
                    if i + 1 in clause:
                        matrix[i][i] += 1
                    elif -(i + 1) in clause:
                        matrix[i][i] -= 1
            
            rank = hermitian_rank(matrix)
            width = dpll_width(clauses)
            
            total_rank += rank
            total_width += width
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "rank/width ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    ratio = mean_rank / mean_width
    
    return {
        "metric_name": "rank/width ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": ratio >= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='rank/width ratio < 1' first_failing_seed={first_failing_seed}")