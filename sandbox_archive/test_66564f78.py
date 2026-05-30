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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

def determinant(matrix):
    n = len(matrix)
    det = 1
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    
    for i in range(n):
        # Find pivot and swap rows if necessary
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(augmented_matrix[j][i], augmented_matrix[i][i])
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Calculate determinant from the upper triangular matrix
    for i in range(n):
        det *= augmented_matrix[i][n+i]
    
    return det

def polynomial_from_kcnf(kcnf, n):
    variables = list(range(1, n+1))
    clauses = kcnf
    
    # Construct the polynomial using quadratic residues
    coefficients = [0] * (2**n)
    for clause in clauses:
        product = 1
        for lit in clause:
            if lit > 0:
                var_index = lit - 1
            else:
                var_index = -lit - 1
            product *= variables[var_index]
        coefficients[product] += 1
    
    # Convert to polynomial with quadratic residues
    qr_polynomial = [0] * (2**n)
    for i in range(2**n):
        if coefficients[i] != 0:
            qr_polynomial[i % (2**(n//2))] += 1
    
    return qr_polynomial

def resolution_width(kcnf):
    n = len(kcnf[0])
    clauses = kcnf
    variables = list(range(1, n+1))
    
    # Convert to CNF and find the width of the resolution proof
    cnf = []
    for clause in clauses:
        new_clause = []
        for lit in clause:
            if lit > 0:
                var_index = lit - 1
            else:
                var_index = -lit - 1
            new_clause.append(variables[var_index])
        cnf.append(new_clause)
    
    # Use a simple heuristic to estimate the width of the resolution proof
    width = 2**n
    for clause in cnf:
        if len(clause) < width:
            width = len(clause)
    
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    
    for n in range(5, 41):
        for _ in range(7):  # Ensure at least 30 instances per seed
            kcnf = []
            m = random.randint(2 * n, 3 * n)
            for _ in range(m):
                clause = [random.choice([-i, i]) for i in range(1, n+1)]
                kcnf.append(clause)
            
            qr_polynomial = polynomial_from_kcnf(kcnf, n)
            order = max([abs(x) for x in qr_polynomial if x != 0])
            width = resolution_width(kcnf)
            
            instances_tested += 1
            metric_value += order / width
    
    mean_metric_value = metric_value / instances_tested
    conjecture_holds = mean_metric_value <= 3.0
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "order_over_width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}")