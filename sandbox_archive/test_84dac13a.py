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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    rank = sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(cols)))
    return rank

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_communication_matrix(f, n):
    matrix = []
    for i in range(2**n):
        row = []
        for j in range(2**n):
            input1 = tuple((i >> k) & 1 for k in range(n))
            input2 = tuple((j >> k) & 1 for k in range(n))
            output = f(input1, input2)
            row.append(output)
        matrix.append(row)
    return matrix

def abp_size_bound(f):
    # Placeholder function. Replace with actual bound calculation.
    n = len(f[0])
    return n * (n + 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    f = generate_boolean_function(n)
    M_f = compute_communication_matrix(f, n)
    rank_M_f = rank(M_f)
    abp_size = abp_size_bound(f)
    
    conjecture_holds = abp_size >= rank_M_f
    counterexample = "" if conjecture_holds else f"ABP size {abp_size} < rank {rank_M_f}"
    
    return {
        "metric_name": "ABP Size",
        "metric_value": abp_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"ABP size < rank\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE mapping_undefined"
    
    print(result)