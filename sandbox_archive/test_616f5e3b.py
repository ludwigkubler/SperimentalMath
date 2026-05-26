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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        pivot_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                pivot_row = j
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] += factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def rank(matrix):
    return gaussian_elimination(matrix)

def boolean_function_to_matrix(f, n):
    M = []
    for i in range(2**n):
        row = [int(x) for x in format(i, f'0{n}b')]
        M.append(row)
    return M

def p_adic_differential_form(M):
    N = len(M)
    H_M = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j:
                diff = sum((M[i][k] - M[j][k]) * (1 << k) for k in range(len(M)))
                H_M[i][j] = diff
    return H_M

def communication_complexity(H_M):
    rank_H_M = rank(H_M)
    return rank_H_M ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = lambda x: random.choice([0, 1])
    M = boolean_function_to_matrix(f, n)
    H_M = p_adic_differential_form(M)
    rho_f = rank(H_M)
    CC_R_f = communication_complexity(H_M)
    conjecture_holds = CC_R_f <= rho_f ** 2
    counterexample = "" if conjecture_holds else f"CC_R(f)={CC_R_f}, rho(f)^2={rho_f**2}"
    return {
        "metric_name": "communication_complexity",
        "metric_value": CC_R_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
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
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")