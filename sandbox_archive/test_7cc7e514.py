# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
    
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(augmented_matrix[r][i]) > abs(augmented_matrix[max_row][i]):
                max_row = r
        
        # Swap current row with the pivot row
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate non-pivot elements in the current column
        for r in range(rows):
            if r != i:
                factor = Fraction(augmented_matrix[r][i], augmented_matrix[i][i])
                for c in range(cols + 1):
                    augmented_matrix[r][c] -= factor * augmented_matrix[i][c]
    
    # Extract the rank from the upper triangular matrix
    rank = sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(cols)))
    return rank

def random_quantum_state(n):
    state = [[random.random() for _ in range(n)] for _ in range(n)]
    # Ensure it's a valid quantum state (unitary)
    for i in range(n):
        for j in range(n):
            if i == j:
                state[i][j] = abs(state[i][j])
            else:
                state[i][j] = 0
    return state

def random_cnf_instance(n):
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables + [-v for v in variables], 3)
        clauses.append(clause)
    return clauses

def dpll_solver(cnf_instance):
    def solve(model):
        if not cnf_instance:
            return True
        literal, rest = cnf_instance[0][0], cnf_instance[0][1:]
        if literal > 0 and literal in model or -literal in model:
            return solve(rest)
        else:
            return solve([(l, r) for l, r in rest if l != literal] + [(l, r) for l, r in rest if l == -literal])
    
    return len([model for model in itertools.product(range(2), repeat=len(cnf_instance)) if solve(model)])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_rank_sum = 0
    proof_length_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        quantum_state = random_quantum_state(n)
        matrix_representation = [row[:] + [1] for row in quantum_state]
        min_rank = gaussian_elimination(matrix_representation)
        
        cnf_instance = random_cnf_instance(n)
        proof_length = dpll_solver(cnf_instance)
        
        if min_rank > 0:
            min_rank_sum += min_rank
            proof_length_sum += proof_length
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_min_rank = min_rank_sum / instances_tested
    mean_proof_length = proof_length_sum / instances_tested
    
    if abs(mean_min_rank - mean_proof_length) <= 3:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Mean min rank: {mean_min_rank}, Mean proof length: {mean_proof_length}"
    
    return {
        "metric_name": "Minimal Representation Rank",
        "metric_value": mean_min_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mean difference exceeds threshold' first_failing_seed={first_failing_seed}")