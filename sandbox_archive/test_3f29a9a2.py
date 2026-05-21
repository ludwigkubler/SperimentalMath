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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(M, p):
    n = len(M)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    A = [row[:] + col[:] for row, col in zip(M, I)]
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            return None
        for j in range(i, n * 2):
            A[i][j] *= mod_inverse(pivot, p)
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n * 2):
                    A[k][j] -= factor * A[i][j]
    return [row[n:] for row in A]

def matrix_multiply(A, B, p):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += (A[i][k] * B[k][j]) % p
    return C

def rank_nc(M, p):
    n = len(M)
    A = [row[:] + [1] for row in M]
    for i in range(n):
        pivot_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if A[pivot_row][i] == 0:
            return None
        A[i], A[pivot_row] = A[pivot_row], A[i]
        for j in range(n * 2):
            if i != j:
                factor = (A[j][i] * mod_inverse(A[i][i], p)) % p
                for k in range(i, n * 2):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % p
    return sum(1 for row in A if any(row[j] != 0 for j in range(n))) // n

def generate_bp(n, read_twice=False):
    bp = []
    for _ in range(n):
        if read_twice:
            bp.append(random.choice([0, 1]))
        else:
            bp.append(random.choice([0]))
    return bp

def tensor_product(bp1, bp2):
    n1, n2 = len(bp1), len(bp2)
    M = [[0] * (n1 * n2) for _ in range(n1 * n2)]
    for i in range(n1):
        for j in range(n2):
            if bp1[i] == 0 and bp2[j] == 0:
                M[i * n2 + j][i * n2 + j] = 1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 101  # Prime number for modular arithmetic
    results = []
    
    for _ in range(30):
        read_twice = bool(random.choice([True, False]))
        bp = generate_bp(20, read_twice)
        M = tensor_product(bp, bp)
        rank = rank_nc(M, p)
        
        if rank is None:
            continue
        
        results.append(rank)
    
    metric_value = sum(results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(r >= math.log(20, 2) for r in results)
    counterexample = "" if conjecture_holds else "read-twice BP with rank < log(n)"
    
    return {
        "metric_name": "Noncommutative Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"read-twice BP with rank < log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")