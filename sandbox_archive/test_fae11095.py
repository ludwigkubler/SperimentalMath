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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def norm_2(g_F, n):
    sum_squares = 0
    for x in range(1 << n):
        g_val = g_F(x)
        sum_squares += g_val ** 2
    return math.sqrt(sum_squares / (1 << n))

def norm_4(g_F, n):
    sum_fourth_powers = 0
    for x in range(1 << n):
        g_val = g_F(x)
        sum_fourth_powers += g_val ** 4
    return sum_fourth_powers ** 0.25 / (1 << n)

def is_unsat(F, n):
    for x in range(1 << n):
        satisfied = all((x >> j) & 1 == (c >> j) & 1 for c in F)
        if satisfied:
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12]
    alpha = 4.5
    m_min = 4 * n_values[0]
    
    def g_F(x):
        count = sum(1 for c in F if all((x >> j) & 1 == (c >> j) & 1 for j in range(n)))
        return count - 7 * m / 8
    
    results = []
    for n in n_values:
        m = int(alpha * n)
        while True:
            F = [random.getrandbits(m) for _ in range(2 ** n)]
            if is_unsat(F, n):
                break
        
        norm_4_val = norm_4(g_F, n)
        norm_2_val = norm_2(g_F, n)
        HC_F = norm_4_val / norm_2_val
        results.append((n, m, HC_F))
    
    w_values = []
    for n, m, HC_F in results:
        def close_under_resolution(F, width):
            while True:
                new_F = []
                for c in F:
                    if sum(1 for j in range(n) if (c >> j) & 1 == 1) <= width:
                        new_F.append(c)
                if len(new_F) == 0:
                    return False
                F = new_F
            return True
        
        w = 2
        while not close_under_resolution(F, w):
            w += 1
        w_values.append(w)
    
    pearson_corr = sum((w - n * math.log2(HC_F) / math.log2(n)) * (w - n * math.log2(HC_F) / math.log2(n)) for w, (_, _, HC_F) in zip(w_values, results)) / len(results)
    empirical_slope = min(w * math.log2(n) / (n * math.log2(HC_F)) for w, (_, _, HC_F) in zip(w_values, results) if HC_F > 1.2)
    
    conjecture_holds = pearson_corr >= 0.5 and empirical_slope >= 0.02
    counterexample = "" if conjecture_holds else "empirical_slope<0.02"
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
    
    results = []
    for seed in seeds:
        with open(f"trial_{seed}.json", "r") as f:
            data = json.load(f)
            results.append(data["TRIAL"])
    
    pearson_corr_avg = sum(r["metric_value"] for r in results) / len(results)
    empirical_slope_avg = min(r["counterexample"].split("<")[0] for r in results if "<" in r["counterexample"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={pearson_corr_avg} std=0 support_fraction={support_fraction}")
    elif any("<" in r["counterexample"] and float(r["counterexample"].split("<")[0]) < 0.02 for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if "<" in result["counterexample"] and float(result["counterexample"].split("<")[0]) < 0.02)
        print(f"RESULT: FALSIFIED counterexample=\"empirical_slope<0.02\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")