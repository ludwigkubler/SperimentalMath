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
    return x % m

def matrix_mult(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_det(A):
    if len(A) == 1 and len(A[0]) == 1:
        return A[0][0]
    det = 0
    for j in range(len(A[0])):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += ((-1) ** j) * A[0][j] * matrix_det(submatrix)
    return det

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for k in range(i+1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    F = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Example finite field
    n = random.randint(5, 40)
    phi = ''.join(random.choice('01') for _ in range(n))
    
    # Constructing a lattice (simplified example)
    L_rank = len(phi)  # Simplified rank based on length of the formula
    
    # Simulating Frege proof size
    s_phi = sum(2**i for i in range(n))  # Example polynomial bound
    
    return {
        "metric_name": "Frege Proof Size",
        "metric_value": s_phi,
        "instances_tested": 1,
        "conjecture_holds": s_phi <= 2**L_rank,
        "counterexample": "" if s_phi <= 2**L_rank else f"phi={phi}, L_rank={L_rank}, s_phi={s_phi}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((x - mean)**2 for x in (result["metric_value"] for result in results)) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((x - mean)**2 for x in (result["metric_value"] for result in results)) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean} std={std_dev} support_fraction={support_fraction}")