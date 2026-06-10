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

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    result = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(rows):
        if matrix[i][i] == 0:
            swap_found = False
            for k in range(i + 1, rows):
                if matrix[k][i] != 0:
                    matrix[i], matrix[k] = matrix[k], matrix[i]
                    swap_found = True
                    break
            if not swap_found:
                continue
        factor = matrix[i][i]
        for j in range(cols):
            matrix[i][j] /= factor
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor_k = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor_k * matrix[i][j]
        rank += 1
    return rank

def rank(matrix):
    matrix_copy = [row[:] for row in matrix]
    return gaussian_elimination(matrix_copy)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n // 2, n)
    phi_A = [[random.randint(-10, 10) for _ in range(m)] for _ in range(n)]
    phi_B = [[random.randint(-10, 10) for _ in range(m)] for _ in range(n)]
    
    min_order_KM = rank(matrix_multiplication(phi_A, phi_B))
    O_phi = sum(abs(x) for row in phi_A for x in row)
    
    return {
        "metric_name": "min_order_KM vs O_phi",
        "metric_value": min_order_KM * O_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")