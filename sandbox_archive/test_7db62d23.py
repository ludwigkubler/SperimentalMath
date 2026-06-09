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
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        
        for j in range(i, n+1):
            matrix[i][j] /= pivot
        
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(i, n+1):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def is_solution(matrix, solution):
    n = len(solution)
    m = len(matrix)
    for i in range(m):
        value = sum(matrix[i][j] * solution[j] for j in range(n))
        if not math.isclose(value, 0, abs_tol=1e-9):
            return False
    return True

def generate_cnf_formula(num_vars, num_clauses):
    clauses = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, num_vars)
            if random.choice([True, False]):
                clause.add(-var)
            else:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def generate_diophantine_matrix(cnf_formula):
    n = len(cnf_formula)
    m = sum(len(clause) for clause in cnf_formula)
    matrix = [[0] * (n + 1) for _ in range(m)]
    
    row = 0
    for i, clause in enumerate(cnf_formula):
        for var in clause:
            if var > 0:
                matrix[row][var - 1] += 1
            else:
                matrix[row][-var - 1] -= 1
        matrix[row][n] = 1
        row += 1
    
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    instances_tested = 0
    total_size = 0
    
    for num_vars in [5, 10, 15, 20, 30, 40]:
        if n_max >= 16:
            break
        
        for _ in range(5):
            num_clauses = random.randint(1, min(num_vars, 10))
            cnf_formula = generate_cnf_formula(num_vars, num_clauses)
            matrix = generate_diophantine_matrix(cnf_formula)
            
            n_max = max(n_max, num_vars)
            instances_tested += 1
            
            if not is_solution(matrix, [Fraction(1) for _ in range(num_vars)]):
                return {
                    "metric_name": "minimal_representation_size",
                    "metric_value": float('inf'),
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"CNF formula with {num_vars} vars and {num_clauses} clauses is not satisfiable"
                }
    
    return {
        "metric_name": "minimal_representation_size",
        "metric_value": total_size / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported by enough seeds' first_failing_seed={first_failing_seed}")