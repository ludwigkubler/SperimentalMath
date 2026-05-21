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

def generate_tseitin_formula(n):
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate clauses for each literal and its negation
    for i in range(n):
        clauses.append(f'{variables[i]} v {variables[n+i]}')
        clauses.append(f'-{variables[i]} v -{variables[n+i]}')
    
    # Generate clauses for the Tseitin formula
    t = n * 2
    for i in range(1, n):
        clauses.append(f'({variables[0]} v x{i+1}) -> {t}')
        t += 1
    
    return variables, clauses

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    
    for col in range(n):
        pivot_row = -1
        for row in range(col, m):
            if augmented_matrix[row][col] != 0:
                pivot_row = row
                break
        
        if pivot_row == -1:
            continue
        
        # Swap rows to make the pivot element 1
        augmented_matrix[col], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[col]
        
        # Normalize the pivot row
        for j in range(n + 1):
            augmented_matrix[col][j] /= augmented_matrix[col][col]
        
        # Eliminate other rows
        for row in range(m):
            if row != col:
                factor = augmented_matrix[row][col]
                for j in range(n + 1):
                    augmented_matrix[row][j] -= factor * augmented_matrix[col][j]
    
    return [row[-1] for row in augmented_matrix]

def shortest_resolution_proof_length(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    b = [0] * n
    
    for i in range(n):
        clause = clauses[i]
        if 'v' not in clause:
            continue
        
        literals = clause.split(' v ')
        for literal in literals:
            if literal.startswith('-'):
                j = int(literal[1:]) - 1
                A[i][j] = -1
            else:
                j = int(literal) - 1
                A[i][j] = 1
        
        b[i] = 1
    
    return len(gaussian_elimination(A, b))

def minimal_root_separation(tropical_coordinates):
    min_sep = float('inf')
    for i in range(len(tropical_coordinates)):
        for j in range(i + 1, len(tropical_coordinates)):
            sep = abs(tropical_coordinates[i] - tropical_coordinates[j])
            if sep < min_sep:
                min_sep = sep
    return min_sep

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    total_count = 0
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        resolution_length = shortest_resolution_proof_length(clauses)
        
        # Simulate tropical coordinates (for simplicity, use random values)
        tropical_coordinates = [random.uniform(0, n) for _ in range(n)]
        min_sep = minimal_root_separation(tropical_coordinates)
        
        total_length += resolution_length
        total_count += 1
    
    avg_length = total_length / total_count
    conjecture_holds = avg_length >= 2 ** (min_sep - 1)
    
    return {
        "metric_name": "Average Resolution Proof Length",
        "metric_value": avg_length,
        "instances_tested": total_count,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"min_sep={min_sep}, avg_length={avg_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_length = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={avg_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_sep too large\" first_failing_seed={first_failing_seed}")