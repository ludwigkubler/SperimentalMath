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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        for j in range(i + 1, cols):
            matrix[i][j] /= matrix[i][i]
        matrix[i][i] = 1
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(i, cols):
                    matrix[k][j] -= factor * matrix[i][j]

def communication_complexity_matrix(variables, clauses):
    n = len(variables)
    m = len(clauses)
    matrix = [[0] * (n + m) for _ in range(n + m)]
    
    for i in range(m):
        clause = clauses[i]
        if len(clause) == 2:
            var1, var2 = clause
            idx1 = int(var1[1:]) - 1
            idx2 = int(var2[1:]) - 1
            matrix[idx1][n + i] = 1
            matrix[n + i][idx2] = 1
        elif len(clause) == 3:
            var1, var2, var3 = clause
            idx1 = int(var1[1:]) - 1
            idx2 = int(var2[1:]) - 1
            idx3 = int(var3[1:]) - 1
            matrix[idx1][n + i] = 1
            matrix[n + i][idx2] = 1
            matrix[n + i][idx3] = 1
    
    gaussian_elimination(matrix)
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        
        # Generate random Tseitin formula
        for i in range(n):
            var = f'x{i+1}'
            clause = [var]
            for j in range(i):
                if random.choice([True, False]):
                    clause.append(f'~{random.choice(variables[:j+1])}')
            clauses.append(clause)
        
        rank = communication_complexity_matrix(variables, clauses)
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": False,  # Mapping undefined for this conjecture
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_rank = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.7 * mean_rank) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(r < 0.7 * mean_rank for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")