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

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate lower entries
        pivot = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= pivot
        for k in range(i+1, n):
            factor = matrix[k][i]
            for j in range(i, n):
                matrix[k][j] -= factor * matrix[i][j]

def rank(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0] * (n - len(row)) for row in matrix]
    gaussian_elimination(augmented_matrix)
    rank = 0
    for row in augmented_matrix:
        if any(x != 0 for x in row):
            rank += 1
    return rank

def quasi_plurality_matrix(cnf):
    n = len(cnf[0])
    matrix = [[0] * (2*n) for _ in range(2*n)]
    
    for clause in cnf:
        literals = set()
        for literal in clause:
            if literal > 0:
                literals.add(literal)
            else:
                literals.add(-literal)
        
        for lit1 in literals:
            for lit2 in literals:
                matrix[lit1-1][lit2-1] += 1
    
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random CNF formula
    n = random.randint(5, 30)
    cnf = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n+1)]
        cnf.append(clause)
    
    # Compute the quasi-plurality matrix
    try:
        matrix = quasi_plurality_matrix(cnf)
    except IndexError:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Determine the minimal rank
    min_rank = rank(matrix)
    
    return {
        "metric_name": "rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": False,  # This will be updated later
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and standard deviation of metric_value
    if all(result["metric_value"] is not None for result in results):
        values = [result["metric_value"] for result in results]
        mean = sum(values) / len(values)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
        
        # Compute fraction of seeds where conjecture_holds
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={seeds[results.index(next((r for r in results if not r['conjecture_holds']), None))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_value_none")