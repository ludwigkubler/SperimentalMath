# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations, product

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i + matrix[i:].index(max(abs(row[i]) for row in matrix[i:]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def is_singular(matrix):
    rows, cols = len(matrix), len(matrix[0])
    if rows != cols:
        return True
    identity = [[Fraction(1) if i == j else Fraction(0) for j in range(cols)] for i in range(rows)]
    reduced_matrix = gaussian_elimination([row[:] + col for row, col in zip(matrix, identity)])
    return any(row[i] != Fraction(0) for row, i in zip(reduced_matrix, range(cols)))

def dpll(cnf):
    def dpll_helper(model, clause_index):
        if clause_index == len(cnf):
            return True
        literals = set(lit for clause in cnf[clause_index:] for lit in clause)
        for literal in literals:
            new_model = model.copy()
            if literal not in new_model and -literal not in new_model:
                new_model[literal] = True
                if dpll_helper(new_model, clause_index + 1):
                    return True
            elif literal in new_model and new_model[literal]:
                continue
            else:
                new_model[literal] = False
                if dpll_helper(new_model, clause_index + 1):
                    return True
        return False
    
    return dpll_helper({}, 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(2**n):
            clause = [var if (i >> j) & 1 else -var for j, var in enumerate(variables)]
            clauses.append(clause)
        return clauses
    
    def arithmetic_hierarchy_depth(cnf):
        depth = 0
        for clause in cnf:
            depth = max(depth, len(set(abs(lit) for lit in clause)))
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        path_length = dpll(cnf)
        depth = arithmetic_hierarchy_depth(cnf)
        results.append({"n": n, "depth": depth, "path_length": path_length})
    
    correlation_coefficient = 0
    if len(results) > 1:
        x_mean = sum(result["depth"] for result in results) / len(results)
        y_mean = sum(result["path_length"] for result in results) / len(results)
        
        numerator = sum((result["depth"] - x_mean) * (result["path_length"] - y_mean) for result in results)
        denominator = sum((result["depth"] - x_mean)**2 * (result["path_length"] - y_mean)**2 for result in results)**0.5
        
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Arithmetic Hierarchy Depth vs DPLL Proof Path Length",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "Correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")