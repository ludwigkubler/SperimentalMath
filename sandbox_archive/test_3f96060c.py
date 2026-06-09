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
    variables = [random.randint(0, 1) for _ in range(n)]
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) == 0:
            var = random.randint(0, n - 1)
            if variables[var] == 1:
                clause.add(var)
        clauses.append(list(clause))
    return variables, clauses

def p_adic_metric_dimension(instance, base=2):
    n = len(instance[0])
    m = len(instance)
    polytope = []
    for i in range(n):
        row = [0] * m
        for j in range(m):
            if instance[j][i] == 1:
                row[j] = 1
        polytope.append(row)
    
    # Gaussian elimination to find the rank of the polytope
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
            denom = matrix[i][i]
            for j in range(i, cols):
                matrix[i][j] /= denom
            for j in range(rows):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(i, cols):
                        matrix[j][k] -= factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    rank = gaussian_elimination(polytope)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m_values = [int(m * (n / 10)) for m in range(1, 6)]
        for m in m_values:
            instance = generate_instance(n, m)
            metric_value = p_adic_metric_dimension(instance, base=2)
            results.append(metric_value)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    conjecture_holds = all(value <= 3.5 for value in results)
    counterexample = "" if conjecture_holds else "p-adic metric dimension exceeds bound"
    
    return {
        "metric_name": "p-adic_metric_dimension",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max(n_values + [m * (n / 10) for n in n_values for m in range(1, 6)]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 3.5) / len(results)
    
    if all(r <= 3.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r > 3.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > 3.5)
        print(f"RESULT: FALSIFIED counterexample='p-adic metric dimension exceeds bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")