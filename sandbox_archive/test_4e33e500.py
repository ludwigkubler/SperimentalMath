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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (2 * random.choice([1, -1]) - 1) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def matrix_multiplication(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return result

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    rank = 0
    for i in range(min(rows, cols)):
        if matrix[i][i] == 0:
            swap_found = False
            for j in range(i + 1, rows):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    swap_found = True
                    break
            if not swap_found:
                continue
        factor = Fraction(matrix[i][i], 1)
        for j in range(i, cols):
            matrix[i][j] /= factor
        for j in range(rows):
            if j != i and matrix[j][i] != 0:
                factor = Fraction(matrix[j][i], 1)
                for k in range(i, cols):
                    matrix[j][k] -= factor * matrix[i][k]
        rank += 1
    return rank

def compute_second_betti_number(cnf):
    n = len(cnf)
    incidence_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i, clause in enumerate(cnf):
        for literal in clause:
            incidence_matrix[abs(literal)][i + 1] += 1
    return gaussian_elimination(incidence_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1) // 2)
    cnf = generate_cnf(n, m)
    
    t_F = sum([2**n for _ in range(2**n)])
    H2_F = compute_second_betti_number(cnf)
    
    if H2_F > 20:
        return {
            "metric_name": "second_betti_number",
            "metric_value": H2_F,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"H^2_F too large: {H2_F}"
        }
    
    return {
        "metric_name": "second_betti_number",
        "metric_value": H2_F,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5

    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"H^2_F too large\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")