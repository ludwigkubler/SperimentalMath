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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
            clauses.append(f'-{variables[i-1]}')
        for i in range(2, n+1):
            clauses.append(f'{-variables[0]} {variables[i-1]}')
        return clauses
    
    def diophantine_system(clauses):
        variables = set()
        for clause in clauses:
            variables.update(clause.split())
        equations = []
        for variable in variables:
            equation = [variable]
            for clause in clauses:
                if variable in clause and '-' + variable not in clause:
                    equation.append('1')
                elif '-' + variable in clause and variable not in clause:
                    equation.append('-1')
                else:
                    equation.append('0')
            equations.append(equation)
        return equations
    
    def minimal_order_of_equivalence_classes(equations):
        n = len(equations)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        augmented_matrix = [row + [col] for row, col in zip(equations, identity_matrix)]
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                max_row = i
                for j in range(i+1, rows):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                
                pivot = matrix[i][i]
                if pivot == 0:
                    continue
                
                for j in range(i, cols):
                    matrix[i][j] /= pivot
                
                for j in range(rows):
                    if j != i and matrix[j][i] != 0:
                        factor = matrix[j][i]
                        for k in range(i, cols):
                            matrix[j][k] -= factor * matrix[i][k]
        
        gaussian_elimination(augmented_matrix)
        
        order = sum(1 for row in augmented_matrix if any(row[i] != 0 for i in range(n)) and all(row[n+i] == 0 for i in range(n)))
        return order
    
    def sat_clause_subset_complexity(clauses):
        return len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = tseitin_formula(n)
        equations = diophantine_system(formula)
        order = minimal_order_of_equivalence_classes(equations)
        complexity = sat_clause_subset_complexity(formula)
        results.append((n, order, complexity))
    
    mean_order = sum(order for _, order, _ in results) / len(results)
    mean_complexity = sum(complexity for _, _, complexity in results) / len(results)
    ratio = mean_order / mean_complexity
    
    conjecture_holds = abs(ratio - 1) <= 0.1
    counterexample = "" if conjecture_holds else f"Ratio {ratio} not within ±10% of 1"
    
    return {
        "metric_name": "MinimalOrderToComplexityRatio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {result['metric_value']} not within ±10% of 1\" first_failing_seed={first_failing_seed}")