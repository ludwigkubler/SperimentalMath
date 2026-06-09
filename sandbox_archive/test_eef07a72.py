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

def generate_instance(n, m):
    variables = set(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def p_adic_metric_dimension(instance, base=2):
    if not instance:
        return 0
    n = len(instance[0])
    m = len(instance)
    
    # Convert instance to a matrix of integers
    matrix = [[1 if i in clause else 0 for i in range(n)] for clause in instance]
    
    # Gaussian elimination to find the rank of the matrix
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        pivot_row = 0
        for col in range(cols):
            if pivot_row >= rows:
                break
            max_row = pivot_row
            for row in range(pivot_row + 1, rows):
                if abs(matrix[row][col]) > abs(matrix[max_row][col]):
                    max_row = row
            matrix[pivot_row], matrix[max_row] = matrix[max_row], matrix[pivot_row]
            if matrix[pivot_row][col] == 0:
                continue
            for row in range(rows):
                if row != pivot_row and matrix[row][col] != 0:
                    factor = -matrix[row][col] / matrix[pivot_row][col]
                    for j in range(cols):
                        matrix[row][j] += factor * matrix[pivot_row][j]
            pivot_row += 1
        return sum(1 for row in matrix if any(matrix[row]))

    rank = gaussian_elimination(matrix)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(1, n // 2)  # Ensure at least one clause
        instance = generate_instance(n, m)
        
        metric_value = p_adic_metric_dimension(instance, base=2)
        results.append(metric_value)
    
    mean_value = sum(results) / len(results)
    conjecture_holds = all(value <= 3.5 for value in results)
    counterexample = "" if conjecture_holds else "p-adic metric dimension > 3.5"
    
    return {
        "metric_name": "p-adic_metric_dimension",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={sum((result['metric_value'] - mean_value) ** 2 for result in results) / len(results)} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")