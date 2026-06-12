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
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        matrix = construct_matrix(cnf)
        minimal_rank = compute_minimal_rank(matrix)
        
        if minimal_rank is None:
            return {
                "metric_name": "minimal_rank",
                "metric_value": float('nan'),
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        expected_rank = math.sqrt(n)
        results.append((minimal_rank, expected_rank))
    
    mean_minimal_rank = sum(r[0] for r in results) / len(results)
    std_dev = math.sqrt(sum((r[0] - mean_minimal_rank) ** 2 for r in results) / len(results))
    
    support_fraction = sum(1 for r in results if abs(r[0] - r[1]) <= std_dev) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_minimal_rank,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

def generate_cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        clause = random.sample(range(1, n + 1), 3)
        clause.append(random.choice([-1, 1]))
        clauses.append(clause)
    return clauses

def construct_matrix(cnf: list) -> list:
    n = len(cnf[0]) - 1
    matrix = [[0] * (2 ** n) for _ in range(2 ** n)]
    
    def literal_to_index(literal):
        if literal > 0:
            return literal - 1
        else:
            return -(literal + 1)
    
    for clause in cnf:
        indices = [literal_to_index(lit) for lit in clause[:-1]]
        value = clause[-1]
        
        def set_clause(matrix, indices, value):
            if value == 1:
                matrix[indices[0]][indices[1]] = 1
                matrix[indices[1]][indices[0]] = 1
            elif value == -1:
                matrix[indices[0]][indices[1]] = -1
                matrix[indices[1]][indices[0]] = -1
        
        set_clause(matrix, indices[:2], value)
        if len(indices) > 2:
            for i in range(2, len(indices)):
                new_indices = [indices[j] for j in range(i) if j != i - 1]
                set_clause(matrix, new_indices, value)
    
    return matrix

def compute_minimal_rank(matrix: list) -> int:
    n = len(matrix)
    rank = 0
    
    def gaussian_elimination(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        
        for i in range(rows):
            if matrix[i][i] == 0:
                for j in range(i + 1, rows):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
        
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return sum(1 for row in matrix if any(row))
    
    rank = gaussian_elimination(matrix)
    return rank

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_minimal_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_minimal_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"] - math.sqrt(n)) <= std_dev for n in [5, 10, 15, 20, 30, 40]) / len(results)
    
    if all(math.isnan(r["metric_value"]) for r in results):
        print("RESULT: INCONCLUSIVE no_valid_data")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_minimal_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not math.isnan(r["metric_value"]) and abs(r["metric_value"] - math.sqrt(n)) > std_dev), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")