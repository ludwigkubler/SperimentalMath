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

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(M, p):
    result = [[1 if i == j else 0 for j in range(len(M))] for i in range(len(M))]
    while p > 0:
        if p % 2 == 1:
            result = matrix_mult(result, M)
        M = matrix_mult(M, M)
        p //= 2
    return result

def noncommutative_fourier_transform(P):
    n = len(P)
    F = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            F[i][j] = P[i][j] / (n**2)
    return F

def spread_of_coefficients(F):
    coeffs = [abs(F[i][j]) for i in range(len(F)) for j in range(len(F))]
    return max(coeffs) - min(coeffs)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 5 + (seed % 30) * 5
    P = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    F = noncommutative_fourier_transform(P)
    spread = spread_of_coefficients(F)
    
    if n == 5:
        expected_spread = "Ω(n)"
    else:
        expected_spread = "O(log size(P))"
    
    conjecture_holds = (spread >= n) if n == 5 else (spread <= math.log(len(P)))
    counterexample = "" if conjecture_holds else f"n={n}, spread={spread}"
    
    return {
        "metric_name": "spread",
        "metric_value": spread,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_spread = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_spread)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_spread} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")