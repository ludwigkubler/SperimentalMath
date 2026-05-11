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
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(n, partition):
    numerator = factorial(n * (n + 1) // 2)
    denominator = 1
    for row in range(n):
        for col in range(row + 1):
            denominator *= (n - row + col) // (col + 1)
    return numerator // denominator

def trivial_representation_multiplicity(partition, n):
    if len(partition) != n or sum(partition) != n:
        return 0
    result = 1
    for part in partition:
        result *= factorial(n - part) // (factorial(part) * factorial(n))
    return result

def generate_random_matrix(n):
    matrix = []
    for _ in range(n):
        row = [random.randint(0, 10) for _ in range(n)]
        matrix.append(row)
    return matrix

def permanent(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    result = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        result += sign * matrix[0][j] * permanent(submatrix)
        sign *= -1
    return result

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    result = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        result += sign * matrix[0][j] * determinant(submatrix)
        sign *= -1
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_multiplicity_permanent = 0
    total_multiplicity_determinant = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            matrix = generate_random_matrix(n)
            perm = permanent(matrix)
            det = determinant(matrix)
            total_multiplicity_permanent += trivial_representation_multiplicity([n], n)
            total_multiplicity_determinant += trivial_representation_multiplicity([n], n)
            instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "trivial_representation_multiplicity_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    ratio = total_multiplicity_permanent / total_multiplicity_determinant
    return {
        "metric_name": "trivial_representation_multiplicity_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": ratio > 10,  # Exponential gap for n = 5 is 10^2 = 100
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")