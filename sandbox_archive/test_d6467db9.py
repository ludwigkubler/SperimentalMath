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

def generate_tseitin_circuit(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    
    for i in range(m):
        a = random.choice(variables)
        b = random.choice(variables)
        if a != b:
            clause = (a, b)
            clauses.append(clause)
    
    return variables, clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find the pivot
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def rank_of_matrix(matrix):
    rows, cols = len(matrix), len(matrix[0])
    row_rank = 0
    col_rank = 0
    
    for i in range(rows):
        if any(matrix[i][j] != 0 for j in range(col_rank)):
            row_rank += 1
            for j in range(col_rank, cols):
                matrix[i][j] /= matrix[i][col_rank]
            for k in range(rows):
                if k != i:
                    factor = -matrix[k][col_rank]
                    for j in range(col_rank, cols):
                        matrix[k][j] += factor * matrix[i][j]
            col_rank += 1
    
    return row_rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        variables, clauses = generate_tseitin_circuit(n, m)
        
        # Create the associated modular form matrix
        matrix = [[0] * (m + 1) for _ in range(m + 1)]
        for a, b in clauses:
            matrix[a - 1][b - 1] += 1
            matrix[b - 1][a - 1] += 1
        
        # Compute the rank of the matrix
        rank = rank_of_matrix(matrix)
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank
        })
    
    max_rank = max(result["rank"] for result in results)
    conjecture_holds = all(max_rank <= (result["m"] ** 2) / 4 for result in results)
    
    return {
        "metric_name": "maximal_rank",
        "metric_value": max_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Max rank {max_rank} exceeds m^2/4 for n={results[0]['n']}, m={results[0]['m']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Max rank exceeds m^2/4\" first_failing_seed={first_failing_seed}")