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

def matrix_multiply(A, B, p):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % p
    return C

def gaussian_elimination(A, b, p):
    n = len(A)
    for i in range(n):
        pivot = i
        while pivot < n and A[pivot][i] == 0:
            pivot += 1
        if pivot == n:
            raise ValueError("No solution exists")
        A[i], A[pivot] = A[pivot], A[i]
        b[i], b[pivot] = b[pivot], b[i]
        for j in range(n):
            if j != i and A[j][i] != 0:
                factor = (A[j][i] * mod_inverse(A[i][i], p)) % p
                A[j] = [(A[j][k] - factor * A[i][k]) % p for k in range(n)]
                b[j] = (b[j] - factor * b[i]) % p
    return [b[i] for i in range(n)]

def tropical_add(a, b):
    if a == float('inf') or b == float('inf'):
        return float('inf')
    return max(a, b)

def tropical_multiply(a, b):
    if a == float('inf') or b == float('inf'):
        return float('inf')
    return a + b

def tropical_matrix_add(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = tropical_add(A[i][j], B[i][j])
    return C

def tropical_matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = tropical_add(C[i][j], tropical_multiply(A[i][k], B[k][j]))
    return C

def tropical_rank(matrix):
    n = len(matrix)
    A = [[matrix[i][j] if i != j else float('inf') for j in range(n)] for i in range(n)]
    b = [0] * n
    try:
        gaussian_elimination(A, b, 2)
        return sum(1 for row in A if any(x != float('inf') for x in row))
    except ValueError:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = random.randint(2, 100)
    
    A = [[random.randint(0, p-1) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(0, p-1) for _ in range(n)] for _ in range(n)]
    
    r1 = tropical_rank(A)
    r2 = tropical_rank(B)
    
    C = tropical_matrix_multiply(A, B)
    r3 = tropical_rank(C)
    
    metric_value = r3
    instances_tested = 1
    conjecture_holds = r3 <= r1 + r2
    counterexample = "" if conjecture_holds else "r3 > r1 + r2"
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")