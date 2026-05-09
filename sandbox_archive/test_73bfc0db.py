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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(num):
    primes = []
    candidate = 2
    while len(primes) < num:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                max_row = j
        A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
        factor = 1 / A_b[i][i]
        for j in range(i, n+1):
            A_b[i][j] *= factor
        for j in range(n):
            if i != j:
                factor = A_b[j][i]
                for k in range(i, n+1):
                    A_b[j][k] -= factor * A_b[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A_b[i][-1]
        for j in range(i+1, n):
            x[i] -= A_b[i][j] * x[j]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def hook_length_formula(shape, n):
    numerator = math.factorial(n)
    denominator = 1
    for row in shape:
        for cell in range(row):
            denominator *= (n + 1 - cell)
    return numerator / denominator

def plethysm_coefficient(char_poly, n):
    # Simplified approximation using hook-length formula for demonstration
    return sum(hook_length_formula(shape, n) * char_poly[shape] for shape in generate_partitions(n))

def generate_partitions(n):
    partitions = []
    def partition_helper(n, k, current_partition):
        if n == 0:
            partitions.append(current_partition)
        else:
            for i in range(min(k, n), -1, -1):
                partition_helper(n - i, i, current_partition + [i])
    partition_helper(n, n, [])
    return partitions

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    m = 40
    char_poly = {(): 1}
    for _ in range(m):
        literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        clause = sum(literals) % n
        if clause not in char_poly:
            char_poly[clause] = 0
        char_poly[clause] += 1
    
    plethysm = plethysm_coefficient(char_poly, n)
    det_plethysm = determinant([[i**2 for i in range(1, n+1)]])
    
    metric_value = plethysm / det_plethysm
    conjecture_holds = plethysm >= 2**(n/2) * m
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "plethysm_too_low"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"plethysm_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_below_threshold")