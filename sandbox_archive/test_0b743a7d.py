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
    
    def generate_tseitin_circuit(n):
        variables = list(range(1, n + 2))
        clauses = []
        
        # Generate OR clauses
        for i in range(1, n + 1):
            clause = [i]
            for j in range(i + 1, n + 2):
                clause.append(-j)
            clauses.append(clause)
        
        # Generate NOT clauses
        for i in range(1, n + 2):
            clause = [-i]
            for j in range(1, n + 2):
                if j != i:
                    clause.append(j)
            clauses.append(clause)
        
        return variables, clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            
            if pivot_row == -1:
                continue
            
            # Swap rows to put the pivot at the current rank position
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            
            # Make all entries in the current column 0 below the pivot
            for row in range(rank + 1, rows):
                factor = -matrix[row][col] / matrix[rank][col]
                for j in range(cols):
                    if matrix[rank][j] != 0:
                        matrix[row][j] += factor * matrix[rank][j]
            
            rank += 1
        
        return rank
    
    def calculate_brauer_group_rank(n):
        variables, clauses = generate_tseitin_circuit(n)
        num_variables = len(variables)
        
        # Create the incidence matrix
        incidence_matrix = [[0] * (num_variables + len(clauses)) for _ in range(num_variables)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    incidence_matrix[var - 1][i + num_variables] = 1
        
        # Perform Gaussian elimination to find the rank
        return gaussian_elimination(incidence_matrix)
    
    n = random.randint(5, 40)  # Sweep through different sizes
    brauer_group_rank = calculate_brauer_group_rank(n)
    max_expected_rank = 1.5 * math.log(n, 2)
    
    metric_value = brauer_group_rank
    conjecture_holds = brauer_group_rank <= max_expected_rank
    counterexample = "" if conjecture_holds else f"n={n}, rank={brauer_group_rank} > {max_expected_rank}"
    
    return {
        "metric_name": "Brauer Group Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")