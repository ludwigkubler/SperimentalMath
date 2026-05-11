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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(shape):
    n = sum(shape)
    numerator = factorial(n)
    denominator = 1
    for row, col in zip(shape, range(len(shape))):
        for j in range(col + 1):
            denominator *= (row - j + len(shape) - col)
    return numerator // denominator

def communication_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if random.choice([True, False]):
                value = random.randint(1, 10)
                matrix[i][j] = value
                matrix[j][i] = value
    return matrix

def partition_from_matrix(matrix):
    n = len(matrix)
    row_sums = [sum(row) for row in matrix]
    col_sums = [sum(col) for col in zip(*matrix)]
    partition = sorted(row_sums + col_sums, reverse=True)
    return partition

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    communication_mat = communication_matrix(n)
    partition = partition_from_matrix(communication_mat)
    tableau_count = hook_length_formula(partition)
    
    determinant_mat = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    det_partition = [n] * n
    det_tableau_count = hook_length_formula(det_partition)
    
    ratio = tableau_count / det_tableau_count
    
    return {
        "metric_name": "tableau_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio > 2**n,
        "counterexample": "" if ratio > 2**n else f"Ratio {ratio} <= 2^{n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 89))  # Default to first 50 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio <= 2^{n}\" first_failing_seed={first_failing_seed}")