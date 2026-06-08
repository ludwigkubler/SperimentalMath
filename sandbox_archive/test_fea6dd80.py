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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate clauses for each variable
        for i in range(n):
            clauses.append([variables[i]])
            clauses.append([-variables[i], variables[0], variables[i]])
            
        # Generate clauses to link all variables together
        for i in range(1, n):
            clauses.append([-variables[i-1], -variables[i], variables[i]])
        
        return variables, clauses
    
    def incidence_matrix(clauses):
        m = len(clauses)
        n = len(clauses[0])
        matrix = [[0] * n for _ in range(m)]
        
        for i, clause in enumerate(clauses):
            for var in clause:
                if var.startswith('x'):
                    j = int(var[1:]) - 1
                    matrix[i][j] = 1
                else:
                    j = int(var[1:]) - 1
                    matrix[i][j] = -1
        
        return matrix
    
    def ehrhart_polynomial_degree(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        
        # Gaussian elimination to find the rank of the matrix
        for i in range(n):
            # Find a pivot
            pivot_row = next((j for j in range(i, n) if matrix[j][i] != 0), None)
            if pivot_row is None:
                return 0  # Matrix is singular
        
            # Swap rows to put the pivot at the diagonal
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            
            # Eliminate entries below the pivot
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        
        return n - sum(1 for row in matrix if all(x == 0 for x in row))
    
    def resolution_proof_width(clauses):
        # Simplified heuristic to estimate resolution proof width
        return len(max(set(sum(clause, [])), key=len))
    
    variables, clauses = generate_tseitin_formula(5)  # Start with n=5 for simplicity
    matrix = incidence_matrix(clauses)
    degree = ehrhart_polynomial_degree(matrix)
    width = resolution_proof_width(clauses)
    
    return {
        "metric_name": "ratio",
        "metric_value": degree / width if width != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": 5,
        "conjecture_holds": degree >= width,
        "counterexample": "" if degree >= width else "resolution_width_exceeds_degree"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")