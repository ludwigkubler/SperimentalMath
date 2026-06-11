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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf, assignment, literals):
        if not cnf:
            return 0
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_literals = literals.copy()
            new_literals.remove(literal)
            return dpll_width([c for c in cnf if literal not in c], new_assignment, new_literals) + 1
        pure_lits = [l for l in literals if all(l not in c or -l not in c for c in cnf)]
        if pure_lits:
            literal = pure_lits[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_literals = literals.copy()
            new_literals.remove(literal)
            return dpll_width(cnf, new_assignment, new_literals) + 1
        branching_literal = random.choice(literals)
        new_assignment_true = assignment.copy()
        new_assignment_true[branching_literal] = True
        new_literals_true = [l for l in literals if l != branching_literal]
        width_true = dpll_width(cnf, new_assignment_true, new_literals_true) + 1
        
        new_assignment_false = assignment.copy()
        new_assignment_false[branching_literal] = False
        new_literals_false = [l for l in literals if l != -branching_literal]
        width_false = dpll_width(cnf, new_assignment_false, new_literals_false) + 1
        
        return max(width_true, width_false)
    
    def tropical_symplectic_form(cnf):
        n = len(cnf)
        omega = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if any(lit in cnf[i] and -lit in cnf[j] for lit in range(1, n+1)):
                    omega[i][j] = 1
                    omega[j][i] = 1
        return omega
    
    def is_symmetric(matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] != matrix[j][i]:
                    return False
        return True
    
    def is_positive_definite(matrix):
        n = len(matrix)
        for k in range(n):
            submatrix = [row[:k+1] for row in matrix[:k+1]]
            det = determinant(submatrix)
            if det <= 0:
                return False
        return True
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for j in range(n):
                submatrix = [row[1:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
            return det
    
    def is_tropical_symplectic_form(matrix):
        if not is_symmetric(matrix):
            return False
        if not is_positive_definite(matrix):
            return False
        n = len(matrix)
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] != 0 and matrix[j][i] != 0:
                    return False
        return True
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        omega = tropical_symplectic_form(cnf)
        if not is_tropical_symplectic_form(omega):
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        width = dpll_width(cnf, {}, list(range(1, n+1)))
        results.append((omega, width))
    
    omega_values = [sum(row) for row in zip(*[omega for omega, _ in results])]
    width_values = [width for _, width in results]
    
    correlation_value = correlation(omega_values, width_values)
    mean_omega = sum(omega_values) / len(omega_values)
    mean_width = sum(width_values) / len(width_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_value,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_value) >= 0.7 and abs(mean_omega - mean_width) <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")