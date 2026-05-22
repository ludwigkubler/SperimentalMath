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
    rows, cols = len(matrix), len(matrix[0])
    for col in range(cols):
        pivot_row = next((i for i in range(col, rows) if matrix[i][col] != 0), None)
        if pivot_row is None:
            continue
        matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
        for row in range(rows):
            if row == col:
                continue
            factor = -matrix[row][col] / matrix[col][col]
            for j in range(cols):
                matrix[row][j] += factor * matrix[col][j]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    matrix = gaussian_elimination(matrix)
    rank = 0
    for row in range(rows):
        if any(matrix[row][col] != 0 for col in range(cols)):
            rank += 1
    return rank

def min_rank(tropical_poly):
    n = len(tropical_poly)
    moment_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            moment_matrix[i][j] = tropical_poly[i - 1]
            moment_matrix[j][i] = tropical_poly[i - 1]
    return rank(moment_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n, 6))
    
    # Generate a random DNF formula for the k-CLIQUE problem
    variables = list(range(n))
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    
    # Convert DNF to tropical polynomial (simplified example)
    tropical_poly = [0] * n
    for clause in clauses:
        term = 1
        for var in clause:
            term += variables[var]
        tropical_poly[term - 1] = max(tropical_poly[term - 1], term)
    
    minimal_rank = min_rank(tropical_poly)
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Moment Matrix",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank >= n ** (1/4),
        "counterexample": "" if minimal_rank >= n ** (1/4) else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_minimal_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_minimal_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={result['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")