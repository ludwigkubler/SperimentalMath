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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def softmax(x, beta):
    e_x = [math.exp((xi + xj) / beta) for xi in x for xj in x]
    sum_e_x = sum(e_x)
    return [v / sum_e_x for v in e_x]

def logsumexp(x, beta):
    max_val = max(x)
    return max_val + math.log(sum(math.exp((xi - max_val) / beta) for xi in x))

def TFT_beta(h, beta):
    n = len(h)
    k_values = range(1, n // 2)
    return max(beta * logsumexp([math.exp(h[x] / beta) * math.exp(-2 * math.pi * k * x / n) for x in range(n)], beta) for k in k_values)

def MFC_beta(h, beta):
    n = len(h)
    k_values = range(1, n // 2)
    return min(beta * logsumexp([math.exp(h[x] / beta) * math.exp(-2 * math.pi * k * x / n) for x in range(n)], beta) for k in k_values)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    beta = 5
    n_values = [8, 12, 16, 20, 24, 28, 32, 36, 40]
    results = []
    
    for n in n_values:
        f = [random.randint(0, 9) for _ in range(n)]
        g = softmax(f, beta)
        
        MFC_f = MFC_beta(f, beta)
        TFT_g = TFT_beta(g, beta)
        MFC_2MFC_f = 2 * MFC_f
        
        Delta = abs(MFC_g - MFC_2MFC_f)
        B_n = 3 * beta * math.log(n)
        
        results.append({
            "n": n,
            "Delta": Delta,
            "B_n": B_n
        })
    
    max_Delta_over_B = max(result["Delta"] / result["B_n"] for result in results)
    mean_Delta = sum(result["Delta"] for result in results) / len(results)
    std_Delta = math.sqrt(sum((result["Delta"] - mean_Delta) ** 2 for result in results) / len(results))
    
    conjecture_holds = max_Delta_over_B <= 1.0
    counterexample = "" if conjecture_holds else "max(Delta/B) > 1"
    
    return {
        "metric_name": "Delta over B",
        "metric_value": mean_Delta,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_Delta = sum(result["metric_value"] for result in results) / len(results)
    std_Delta = math.sqrt(sum((result["metric_value"] - mean_Delta) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_Delta:.6f} std={std_Delta:.6f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_Delta:.6f} std={std_Delta:.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max(Delta/B) > 1\" first_failing_seed={first_failing_seed}")