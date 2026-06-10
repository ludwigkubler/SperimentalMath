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
from itertools import product

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = Fraction(matrix[i][i], 1)
        for j in range(i, cols):
            matrix[i][j] /= factor
        
        for r in range(rows):
            if r != i:
                factor = Fraction(matrix[r][i], 1)
                for j in range(i, cols):
                    matrix[r][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    num_rows, num_cols = len(reduced_matrix), len(reduced_matrix[0])
    rank = 0
    for i in range(num_rows):
        if any(reduced_matrix[i][j] != 0 for j in range(num_cols)):
            rank += 1
    return rank

def k_group_order(vector_space):
    n = len(vector_space)
    identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    augmented_matrix = [row + identity[i] for i, row in enumerate(vector_space)]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    rank_value = rank(reduced_matrix)
    return 2 ** (n - rank_value)

def sat_instance_to_vector_space(instance):
    n = len(instance)
    vector_space = []
    for assignment in product([0, 1], repeat=n):
        vector = [Fraction(0) for _ in range(n)]
        for i in range(n):
            if instance[i] == 'A':
                vector[i] += Fraction(assignment[i])
            elif instance[i] == 'B':
                vector[i] -= Fraction(assignment[i])
        vector_space.append(vector)
    return vector_space

def dpll_solver(instance):
    n = len(instance)
    def backtrack(assignment, clause_index):
        if clause_index == n:
            return True
        for value in [0, 1]:
            assignment[clause_index] = value
            if all(any(assignment[i] != 0 for i in clause) for clause in instance):
                if backtrack(assignment, clause_index + 1):
                    return True
            assignment[clause_index] = None
        return False
    
    assignment = [None] * n
    return backtrack(assignment, 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances_tested = 0
    total_length = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if time.time() + 20 > 240:
            return {
                "metric_name": "Frege proof length",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": max_n,
                "conjecture_holds": False,
                "counterexample": "budget_exceeded"
            }
        
        for _ in range(5):
            instance = ['A' if random.randint(0, 1) else 'B' for _ in range(n)]
            vector_space = sat_instance_to_vector_space(instance)
            k_group_order_value = k_group_order(vector_space)
            
            if not dpll_solver(instance):
                continue
            
            length = len(dpll_solver(instance))
            total_length += length
            instances_tested += 1
            max_n = max(max_n, n)
            
            if conjecture_holds and abs(length - k_group_order_value) > 2 * min(length, k_group_order_value):
                conjecture_holds = False
                counterexample = f"Instance size {n}, length {length}, K-group order {k_group_order_value}"
    
    return {
        "metric_name": "Frege proof length",
        "metric_value": total_length / instances_tested if instances_tested > 0 else None,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_length = (sum((r["metric_value"] - mean_length) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")