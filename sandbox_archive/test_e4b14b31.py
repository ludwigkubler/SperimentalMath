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
    return abs(a*b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(young_tableau):
    n = len(young_tableau)
    hook_lengths = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            hook_lengths[i][j] = (n - i) + (n - j) - 1 - young_tableau[i].count(j)
    det = 1
    for i in range(n):
        for j in range(n):
            det *= hook_lengths[i][j]
    return det

def generate_matrix(n, m):
    matrix = [[random.randint(0, 10) for _ in range(m)] for _ in range(n)]
    return matrix

def permanent(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    result = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** (j % 2)
        result += sign * matrix[0][j] * permanent(submatrix)
    return result

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** (j % 2)
        det += sign * matrix[0][j] * determinant(submatrix)
    return det

def plethysm_coefficient(matrix, k):
    n = len(matrix)
    young_tableau = []
    for i in range(n):
        row = sorted([matrix[i][j] for j in range(n)], reverse=True)
        young_tableau.append(row)
    hook_lengths = hook_length_formula(young_tableau)
    return hook_lengths ** k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = math.floor(n ** 1.5)
    perm_matrix = generate_matrix(n, n)
    det_matrix = generate_matrix(m, m)
    perm_plethysm = plethysm_coefficient(perm_matrix, k=2)
    det_value = determinant(det_matrix)
    epsilon = 0.1
    if perm_plethysm > det_value + epsilon * n ** 2:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "plethysm_coefficient <= determinant_value + epsilon*n^2"
    return {
        "metric_name": "plethysm_coefficient_gap",
        "metric_value": perm_plethysm - det_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, {result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"plethysm_coefficient <= determinant_value + epsilon*n^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")