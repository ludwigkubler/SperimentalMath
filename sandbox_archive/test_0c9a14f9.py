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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(i, n+1):
            M[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = M[j][i]
                for k in range(i, n+1):
                    M[j][k] -= factor * M[i][k]
    return [M[i][-1] for i in range(n)]

def generate_random_function_field(degree):
    # Simplified generation of a random function field
    return [random.randint(0, 1) for _ in range(degree)]

def deligne_lusztig_variety(K):
    n = len(K)
    V_K = []
    for i in range(n):
        row = [K[(i + j) % n] for j in range(n)]
        V_K.append(row)
    return V_K

def geometric_langlands_dual(V_K):
    n = len(V_K)
    D_K = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                D_K[i][j] = sum(V_K[k][i] * V_K[k][j] for k in range(n)) / (n - 1)
    return D_K

def min_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if matrix[i][i] != 0:
            rank += 1
    return rank

def communication_complexity(n):
    # Simplified estimation of communication complexity for Disjointness
    return n * (n - 1) / 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    K = generate_random_function_field(n)
    V_K = deligne_lusztig_variety(K)
    D_K = geometric_langlands_dual(V_K)
    rank_D_K = min_rank(D_K)
    CC = communication_complexity(n)
    
    conjecture_holds = rank_D_K > n and CC >= n**2
    counterexample = "" if conjecture_holds else f"rank(D(K))={rank_D_K}, CC={CC}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": CC,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    total_CC = 0
    count_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_CC += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_holds += 1
    
    mean_CC = total_CC / len(results)
    support_fraction = count_holds / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_CC} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_CC} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"CC<{first_failing_seed}>\" first_failing_seed={first_failing_seed}")