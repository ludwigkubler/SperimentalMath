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

def generate_random_cnf(n: int, m: int) -> list:
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        cnf.append(clause)
    return cnf

def construct_symmetric_matrix(cnf: list, n: int) -> list:
    matrix = [[0] * (2 * n) for _ in range(2 * n)]
    for clause in cnf:
        i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
        matrix[i][j + n] = 1
        matrix[j + n][i] = 1
    return matrix

def gaussian_elimination(matrix: list) -> list:
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find a non-zero pivot in the current column
        pivot_row = next((r for r in range(i, rows) if matrix[r][i] != 0), None)
        if pivot_row is None:
            continue
        # Swap rows to move the pivot to the diagonal
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        # Eliminate non-zero entries below the pivot
        for r in range(i + 1, rows):
            factor = Fraction(matrix[r][i], matrix[i][i])
            for c in range(cols):
                matrix[r][c] -= factor * matrix[i][c]
    return matrix

def min_index_of_quotients(matrix: list) -> int:
    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(row))
    return rank

def dpll_proof_depth(cnf: list, n: int) -> int:
    def dpll(clause_set, assignment):
        if not clause_set:
            return 0
        unit_clauses = [c for c in clause_set if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll([c for c in clause_set if literal not in c], new_assignment)
        pure_literals = [l for l in range(1, n + 1) if (l not in assignment and -l not in assignment)]
        if not pure_literals:
            return float('inf')
        literal = pure_literals[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        return dpll([c for c in clause_set if literal not in c], new_assignment)
    return dpll(cnf, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_indices = []
    proof_depths = []
    
    for n in n_values:
        cnf = generate_random_cnf(n, n * (n - 1) // 2)
        matrix = construct_symmetric_matrix(cnf, n)
        min_index = min_index_of_quotients(matrix)
        proof_depth = dpll_proof_depth(cnf, n)
        
        if min_index == 0 or proof_depth == float('inf'):
            return {
                "metric_name": "log_min_index",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "min_index_zero_or_infinite_proof_depth"
            }
        
        min_indices.append(math.log(min_index))
        proof_depths.append(proof_depth)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(min_indices, proof_depths)) / \
                               math.sqrt(sum((x - mean_x)**2 for x in min_indices) * sum((y - mean_y)**2 for y in proof_depths))
    mean_log_min_index = sum(min_indices) / len(min_indices)
    
    return {
        "metric_name": "log_min_index",
        "metric_value": mean_log_min_index,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_log_min_index = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_log_min_index} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_log_min_index} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_met\" first_failing_seed={first_failing_seed}")