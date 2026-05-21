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

def fraction_add(f1, f2):
    num1, den1 = f1
    num2, den2 = f2
    new_num = num1 * den2 + num2 * den1
    new_den = den1 * den2
    common_divisor = gcd(new_num, new_den)
    return (new_num // common_divisor, new_den // common_divisor)

def fraction_sub(f1, f2):
    num1, den1 = f1
    num2, den2 = f2
    new_num = num1 * den2 - num2 * den1
    new_den = den1 * den2
    common_divisor = gcd(new_num, new_den)
    return (new_num // common_divisor, new_den // common_divisor)

def fraction_mul(f1, f2):
    num1, den1 = f1
    num2, den2 = f2
    new_num = num1 * num2
    new_den = den1 * den2
    common_divisor = gcd(new_num, new_den)
    return (new_num // common_divisor, new_den // common_divisor)

def fraction_div(f1, f2):
    num1, den1 = f1
    num2, den2 = f2
    if den2 == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    new_num = num1 * den2
    new_den = den1 * num2
    common_divisor = gcd(new_num, new_den)
    return (new_num // common_divisor, new_den // common_divisor)

def fraction_to_float(f):
    return f[0] / f[1]

def build_ABP(N, w, d, prime):
    M = [[[random.randint(0, prime - 1) for _ in range(d + 1)] for _ in range(w)] for _ in range(w)]
    f = [[M[i][j][k] * M[(i + j) % w][k][l] for k in range(d + 1)] for j in range(w) for l in range(2)]
    return f

def compute_T(f, N, prime):
    T = [[(0, 1)] * (N * N) for _ in range(N * N)]
    monomials = [(i, j) for i in range(N) for j in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(d + 1):
                for l in range(2):
                    T[i * N + j][(k, l)] = fraction_add(T[i * N + j], (f[i][j][k] * M[(i + j) % w][k][l], prime))
    return T

def gaussian_elimination_mod_prime(matrix, prime):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(fraction_to_float(matrix[j][i])) > abs(fraction_to_float(matrix[max_row][i])):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = fraction_to_float(matrix[i][i])
        for j in range(i + 1, n):
            factor = fraction_div((0, 1), (matrix[j][i], prime))
            for k in range(n * n):
                matrix[j][k] = fraction_sub(matrix[j][k], fraction_mul(factor, matrix[i][k]))
    rank = sum(1 for row in matrix if any(fraction_to_float(x) != 0 for x in row[:n]))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    N_values = [8, 10, 12, 14]
    w_values = [2, 3]
    d_values = [3, 4]
    results = []
    
    for N in N_values:
        for w in w_values:
            for d in d_values:
                f = build_ABP(N, w, d, 2**30 - 1)
                T = compute_T(f, N, 2**30 - 1)
                rank = gaussian_elimination_mod_prime(T, 2**30 - 1)
                sigma_f = N * N - rank
                results.append(sigma_f >= N - 2 * w ** 2)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(results)
    counterexample = "" if conjecture_holds else "sigma(f) < N - 2w^2"
    
    return {
        "metric_name": "sigma(f)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if all(r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r for r in results):
        first_failing_seed = seeds[results.index(False)]
        print(f"RESULT: FALSIFIED counterexample=\"sigma(f) < N - 2w^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")