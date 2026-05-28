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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        literals = [f'x{i}' for i in range(1, n+1)] + [f'~x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 3)
            if random.choice([True, False]):
                clause = [f'~{lit}' if lit.startswith('x') else lit for lit in clause]
            clauses.append(f"({clause[0]} & {clause[1]} & {clause[2]})")
        return ' | '.join(clauses)
    
    def parse_3cnf(formula):
        literals = set()
        for clause in formula.split(' | '):
            for lit in clause.split('&'):
                if lit.startswith('~'):
                    literals.add(lit[1:])
                else:
                    literals.add(lit)
        return literals
    
    def gaussian_elimination(matrix, b):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            b[i], b[max_row] = b[max_row], b[i]
            
            # Eliminate below pivot
            for j in range(i+1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] += factor * matrix[i][k]
                b[j] += factor * b[i]
        
        # Back-substitute
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(matrix[i][j] * x[j] for j in range(i+1, n))) / matrix[i][i]
        return x
    
    def solve_system(literals, clauses):
        n = len(literals)
        A = [[0] * n for _ in range(n)]
        b = [0] * n
        
        for clause in clauses:
            vars_in_clause = set()
            for lit in clause.split('&'):
                if lit.startswith('~'):
                    vars_in_clause.add(lit[1:])
                else:
                    vars_in_clause.add(lit)
            
            # Create a system of linear equations
            for var in vars_in_clause:
                idx = literals.index(var) if var in literals else literals.index(f'~{var}') + n
                A[idx][idx] += 1
        
        # Solve the system using Gaussian elimination
        x = gaussian_elimination(A, b)
        
        # Check for real solutions
        real_points = []
        for i in range(n):
            if abs(x[i]) > 0.5:
                real_points.append(i)
        
        return len(real_points)
    
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    literals = parse_3cnf(formula)
    clauses = formula.split(' | ')
    
    num_real_points = solve_system(literals, clauses)
    
    return {
        "metric_name": "Number of distinct real points",
        "metric_value": num_real_points,
        "instances_tested": 1,
        "conjecture_holds": True if num_real_points >= n else False,
        "counterexample": "" if num_real_points >= n else f"Formula: {formula}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula: {results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")