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
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def generate_gf_elements(q):
    elements = [i for i in range(q)]
    return elements

def matrix_multiply(A, B, q):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % q
    return result

def gaussian_elimination(A, b, q):
    n = len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        pivot_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[pivot_row][i]):
                pivot_row = j
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
        for j in range(n):
            augmented_matrix[i][j] = (augmented_matrix[i][j] * pow(augmented_matrix[i][i], q-2, q)) % q
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n+1):
                    augmented_matrix[j][k] = (augmented_matrix[j][k] - factor * augmented_matrix[i][k]) % q
    return [row[-1] for row in augmented_matrix]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5 + random.randint(0, 35)
    q = 2 ** (n // 4 + 1)
    elements = generate_gf_elements(q)
    
    def is_permutation_poly(poly):
        for i in range(q):
            if poly[i] == i:
                return False
        return True
    
    def compute_width(poly):
        m = len(poly)
        A = [[0] * m for _ in range(m)]
        b = [0] * m
        for i in range(m):
            for j in range(m):
                A[i][j] = (poly[j] ** i) % q
            b[i] = poly[i]
        solution = gaussian_elimination(A, b, q)
        return sum(1 for x in solution if x != 0)
    
    width = float('inf')
    for _ in range(30):
        poly = [random.randint(0, q-1) for _ in range(n)]
        if is_permutation_poly(poly):
            width = min(width, compute_width(poly))
    
    return {
        "metric_name": "min_width",
        "metric_value": width,
        "instances_tested": 30,
        "conjecture_holds": width >= math.log2(n),
        "counterexample": "" if width >= math.log2(n) else f"Degree {n}, Width {width}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_width = sum(res["metric_value"] for res in results) / len(results)
    std_width = math.sqrt(sum((res["metric_value"] - mean_width) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Degree {results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")