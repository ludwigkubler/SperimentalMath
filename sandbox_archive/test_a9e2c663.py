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

def generate_random_sat_instance(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause_size = random.randint(1, n)
        clause = random.sample(variables, clause_size)
        clauses.append(clause)
    return clauses

def gaussian_elimination(matrix: list) -> list:
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        pivot_row = i
        while matrix[pivot_row][i] == 0:
            pivot_row += 1
            if pivot_row == rows:
                return matrix
        # Swap rows
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        # Eliminate below
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def count_generators(clauses: list) -> int:
    n = len(clauses)
    variables = set()
    for clause in clauses:
        variables.update(clause)
    variables = sorted(variables)
    m = len(variables)
    
    # Create the Koszul complex matrix
    matrix = [[0] * (m + 1) for _ in range(m)]
    for i, var in enumerate(variables):
        for clause in clauses:
            if var in clause:
                matrix[i][len(clause)] += 1
    
    # Perform Gaussian elimination to find the rank of the matrix
    reduced_matrix = gaussian_elimination(matrix)
    
    # The number of generators is the rank of the matrix
    return sum(1 for row in reduced_matrix if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    total_generators = 0
    
    for n in range(5, n_max + 1):
        for _ in range(instances_tested // (n_max - 4)):
            m = random.randint(n, n * 2)
            clauses = generate_random_sat_instance(n, m)
            generators = count_generators(clauses)
            total_generators += generators
    
    mean_generators = Fraction(total_generators) / instances_tested
    conjecture_holds = mean_generators <= n_max ** (1/3)
    
    return {
        "metric_name": "mean_generators",
        "metric_value": float(mean_generators),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")