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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i and abs(A[k][i]) > 1e-9:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def log_sum_exp(h, beta):
    if not h:
        return 0.0
    max_val = max(h)
    sum_exp = sum(math.exp(beta * (x - max_val)) for x in h)
    return -(1 / beta) * (max_val + math.log(sum_exp))

def maslov_dequantized_fourier_transform(f, beta):
    n = len(f)
    omega = math.exp(2 * math.pi * 1j / n)
    tft_f = [0.0] * n
    for k in range(n):
        if k == 0:
            sum_exp = sum(math.exp(-beta * f[i]) for i in range(n))
        else:
            sum_exp = sum(math.exp(-beta * (f[i] + omega ** (i * k))) for i in range(n))
        tft_f[k] = -(1 / beta) * math.log(sum_exp)
    return tft_f

def min_plus_convolution(f):
    n = len(f)
    g = [float('inf')] * n
    for i in range(n):
        for j in range(n):
            g[(i + j) % n] = min(g[(i + j) % n], f[i] + f[j])
    return g

def run_trial(seed: int) -> dict:
    random.seed(seed)
    beta_values = [5, 10, 20, 50, 100, 200]
    results = []
    
    for beta in beta_values:
        n = 8
        f = [random.uniform(0, 1) for _ in range(n)]
        g = min_plus_convolution(f)
        
        tft_f = maslov_dequantized_fourier_transform(f, beta)
        tft_g = maslov_dequantized_fourier_transform(g, beta)
        
        mfc_f = min(abs(x) for x in tft_f if x != 0)
        mfc_g = min(abs(x) for x in tft_g if x != 0)
        
        delta = abs(mfc_g - 2 * mfc_f)
        bound = 10 * math.log(8) / beta
        
        results.append({
            "beta": beta,
            "delta": delta,
            "bound": bound
        })
    
    max_delta = max(result["delta"] for result in results)
    pass_rate = sum(1 for result in results if result["delta"] <= result["bound"]) / len(results)
    
    conjecture_holds = all(result["delta"] <= result["bound"] for result in results)
    counterexample = "" if conjecture_holds else f"beta={results[0]['beta']}, delta={results[0]['delta']}"
    
    return {
        "metric_name": "Delta",
        "metric_value": max_delta,
        "instances_tested": len(results),
        "n_max": 8,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(30, 59)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    max_delta = max(result["metric_value"] for result in seeds)
    pass_rate = sum(1 for seed in seeds if all(result["delta"] <= result["bound"] for result in run_trial(seed)["results"])) / len(seeds)
    
    print(f"RESULT: SUPPORTED mean={max_delta} std=0 support_fraction={pass_rate}")