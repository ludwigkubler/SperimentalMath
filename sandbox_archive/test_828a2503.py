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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        b[i] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def noncommutative_Lp_norm(M, p):
    if p == 1:
        max_sum = 0
        for i in range(len(M)):
            row_sum = sum(abs(x) for x in M[i])
            col_sum = sum(abs(M[j][i]) for j in range(len(M)))
            max_sum = max(max_sum, row_sum, col_sum)
        return max_sum ** p
    elif p == float('inf'):
        max_norm = 0
        for i in range(len(M)):
            row_norm = sum(abs(x) for x in M[i])
            col_norm = sum(abs(M[j][i]) for j in range(len(M)))
            max_norm = max(max_norm, row_norm, col_norm)
        return max_norm ** p
    else:
        sum_val = 0
        n = len(M)
        for i in range(n):
            for j in range(i + 1, n):
                sum_val += abs(sum(M[i][k] * M[j][k] for k in range(n))) ** (p / (i + j - 2))
        return (sum_val / (n * n)) ** (1 / p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M = [[random.random() for _ in range(n)] for _ in range(n)]
    c = 2  # Example constant based on expected complexity class
    lower_bound = c * n
    
    norm_values = []
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            norm = noncommutative_Lp_norm(M, i + j - 2)
            norm_values.append(norm)
    
    mean_value = sum(norm_values) / len(norm_values)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in norm_values) / len(norm_values))
    
    conjecture_holds = all(lower_bound <= norm < lower_bound + 0.1 * n for norm in norm_values)
    counterexample = "" if conjecture_holds else "lower_bound not met"
    
    return {
        "metric_name": "Noncommutative L_p Norm",
        "metric_value": mean_value,
        "instances_tested": len(norm_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='lower_bound_not_met' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")