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

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def resultant(poly1, poly2):
    n = len(poly1)
    m = len(poly2)
    if n != m:
        raise ValueError("Polynomials must have the same degree")
    
    R = [[0] * (n + m - 1) for _ in range(n + m - 1)]
    for i in range(n):
        for j in range(m):
            R[i + j][i + j] += poly1[i] * poly2[j]
    
    b = [0] * (n + m - 1)
    for i in range(n + m - 1):
        b[i] = R[i][i]
    
    x = gaussian_elimination(R, b)
    return abs(x[-1])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(50):  # Sample 50 instances per seed
        clauses = []
        for _ in range(n):
            literals = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(2, n))]
            clauses.append(literals)
        
        polynomials = []
        for clause in clauses:
            poly = 1
            for literal in clause:
                if literal > 0:
                    poly *= (x - literal)
                else:
                    poly *= (x + abs(literal))
            polynomials.append(poly)
        
        degree = resultant(polynomials[0], polynomials[1])
        instances_tested += 1
        
        if degree < 2 ** (n / 2):
            conjecture_holds = False
            counterexample = f"Degree {degree} is less than 2^{n/2}"
    
    return {
        "metric_name": "Resultant Degree",
        "metric_value": degree,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")