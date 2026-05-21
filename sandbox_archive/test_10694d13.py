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
    common_den = lcm(den1, den2)
    new_num = num1 * (common_den // den1) + num2 * (common_den // den2)
    return (new_num, common_den)

def fraction_sub(f1, f2):
    num1, den1 = f1
    num2, den2 = f2
    common_den = lcm(den1, den2)
    new_num = num1 * (common_den // den1) - num2 * (common_den // den2)
    return (new_num, common_den)

def fraction_mul(f1, f2):
    num1, den1 = f1
    num2, den2 = f2
    return (num1 * num2, den1 * den2)

def fraction_div(f1, f2):
    num1, den1 = f1
    num2, den2 = f2
    if den2 == 0:
        raise ZeroDivisionError("Fraction division by zero")
    return (num1 * den2, den1 * num2)

def fraction_reduce(f):
    num, den = f
    common_div = gcd(num, den)
    return (num // common_div, den // common_div)

def fraction_matrix_mul(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Matrix dimensions do not match for multiplication")
    
    result = [[(0, 1)] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] = fraction_add(result[i][j], fraction_mul(A[i][k], B[k][j]))
    
    return result

def build_ABP(N, w, d, p):
    M = [[[random.randint(0, 2) - 1 for _ in range(d + 1)] for _ in range(w)] for _ in range(w)]
    f = [[M[i][j][k] * M[(i + j) % w][k][l] for k in range(d + 1)] for j in range(w) for l in range(2)]
    
    T = [[[0, 1]] * (N * d) for _ in range(N * d)]
    for i in range(N):
        for j in range(d):
            monomial_index = i * d + j
            for k in range(N):
                T[monomial_index][k] = fraction_add(T[monomial_index][k], (1, 1))
    
    return f, T

def gaussian_elimination(M):
    rows, cols = len(M), len(M[0])
    rank = 0
    for j in range(cols):
        i_max = rank
        for i in range(rank, rows):
            if abs(M[i][j]) > abs(M[i_max][j]):
                i_max = i
        
        M[rank], M[i_max] = M[i_max], M[rank]
        
        if M[rank][j] == 0:
            continue
        
        for i in range(rank + 1, rows):
            factor = fraction_div((0, 1), (M[i][j], M[rank][j]))
            for k in range(cols):
                M[i][k] = fraction_sub(M[i][k], fraction_mul(factor, M[rank][k]))
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    Ns = [8, 10, 12, 14]
    ws = [2, 3]
    ds = [3, 4]
    
    results = []
    for N in Ns:
        for w in ws:
            for d in ds:
                f, T = build_ABP(N, w, d, 2**30 - 1)
                
                sigma_f = N * N - gaussian_elimination(T)
                if sigma_f < N - 2 * w ** 2:
                    return {
                        "metric_name": "sigma(f)",
                        "metric_value": sigma_f,
                        "instances_tested": 1,
                        "conjecture_holds": False,
                        "counterexample": f"ABP with N={N}, w={w}, d={d} has sigma(f) < N - 2w^2"
                    }
                
                results.append(sigma_f)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([x for x in results if x >= N - 2 * w ** 2]) / len(results)
    
    return {
        "metric_name": "sigma(f)",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']:.6f}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_values = [x["metric_value"] for x in results]
    std_devs = [math.sqrt(sum((y - x["metric_value"]) ** 2 for y in mean_values) / len(mean_values)) for x in results]
    support_fractions = [sum(1 for y in x.values() if y >= N - 2 * w ** 2) / len(x.values()) for x in results]
    
    total_support_fraction = sum(support_fractions) / len(support_fractions)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_values[0]:.6f} std={std_devs[0]:.6f} support_fraction={total_support_fraction:.2f}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")