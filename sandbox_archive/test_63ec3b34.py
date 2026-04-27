# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def hadamard_matrix(n):
    if n == 1:
        return [[1]]
    H = hadamard_matrix(n // 2)
    top_left = H
    top_right = H
    bottom_left = H
    bottom_right = [-x for x in H]
    return [
        [a + b for a, b in zip(top_left, top_right)],
        [a - b for a, b in zip(bottom_left, bottom_right)]
    ]

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    A = [[matrix[i][j] for j in range(m)] for i in range(n)]
    pivot_row = 0
    pivot_col = 0
    while pivot_row < n and pivot_col < m:
        if matrix[pivot_row][pivot_col] == 0:
            swap_found = False
            for i in range(pivot_row + 1, n):
                if matrix[i][pivot_col] != 0:
                    matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
                    swap_found = True
                    break
            if not swap_found:
                pivot_col += 1
                continue
        for i in range(pivot_row + 1, n):
            factor = -matrix[i][pivot_col] / matrix[pivot_row][pivot_col]
            for j in range(m):
                matrix[i][j] += factor * matrix[pivot_row][j]
        pivot_row += 1
        pivot_col += 1
    return min(pivot_row, m)

def dyadic_discrepancy(M, n):
    max_discrepancy = 0
    for i in range(n):
        for j in range(n):
            box_sum = sum(M[x][y] for x in range(i, min(i + (1 << int(math.log2(n))), n)) for y in range(j, min(j + (1 << int(math.log2(n))), n)))
            discrepancy = abs(box_sum) / math.sqrt((1 << int(math.log2(n))) ** 2)
            if discrepancy > max_discrepancy:
                max_discrepancy = discrepancy
    return max_discrepancy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 8, 16]
    results = []
    
    for n in n_values:
        H_n = hadamard_matrix(n)
        D_H_n = dyadic_discrepancy(H_n, n)
        R_H_n_n2 = rank(H_n + [[random.choice([-1, 1]) for _ in range(n)] for _ in range(int(n / 2))])
        
        results.append({
            "n": n,
            "D_H_n": D_H_n,
            "R_H_n_n2": R_H_n_n2
        })
    
    return {
        "metric_name": "R(M, n/2) * log(n) / D^2",
        "metric_value": sum(result["R_H_n_n2"] * math.log(result["n"]) / result["D_H_n"] ** 2 for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["R_H_n_n2"] * math.log(result["n"]) / result["D_H_n"] ** 2 >= 0.05 for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")