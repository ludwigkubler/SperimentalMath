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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find max pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        # Eliminate column i
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def min_plus_convolution(f, g, n):
    result = [0] * (2*n - 1)
    for i in range(n):
        for j in range(n):
            result[(i + j) % (2*n - 1)] += f[i] + g[j]
    return result

def maslov_dft(f, beta, n):
    omega = math.exp(2 * math.pi / n)
    mfc = [0] * n
    for k in range(n):
        sum_val = 0
        for x in range(n):
            sum_val += math.exp(-beta * f[x]) * (omega ** (k * x))
        mfc[k] = abs(sum_val)
    return min(mfc)

def delta(f, g, beta, n):
    mfc_f = maslov_dft(f, beta, n)
    mfc_g = maslov_dft(g, beta, n)
    return abs(mfc_g - 2 * mfc_f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 12, 16, 20, 24, 28, 32]
    results = []
    
    for n in n_values:
        deltas = []
        for _ in range(200):
            f = [random.random() for _ in range(n)]
            g = min_plus_convolution(f, f, n)
            delta_value = delta(f, g, 5, n)
            deltas.append(delta_value)
        
        mean_delta = sum(deltas) / len(deltas)
        max_delta = max(deltas)
        R_n = max_delta / mean_delta
        bound = 3 + math.log2(n) / 4
        
        results.append({
            "n": n,
            "mean_delta": mean_delta,
            "max_delta": max_delta,
            "R_n": R_n,
            "bound": bound
        })
    
    if any(result["R_n"] > result["bound"] for result in results):
        conjecture_holds = False
        counterexample = f"n={result['n']}, R(n)={result['R_n']}, bound={result['bound']}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "R(n)",
        "metric_value": sum(result["R_n"] for result in results) / len(results),
        "instances_tested": 200 * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    mean_R_n = sum(result["R_n"] for result in results) / len(results)
    std_R_n = (sum((result["R_n"] - mean_R_n) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["R_n"] <= result["bound"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean_R_n:.6f} std={std_R_n:.6f} support_fraction={support_fraction:.2f}")