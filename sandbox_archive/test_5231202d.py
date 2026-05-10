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
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_multiply(A, B, p):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % p
    return C

def gaussian_elimination(A, b, p):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = (A[j][i] * mod_inverse(A[i][i], p)) % p
            for k in range(i, n):
                A[j][k] = (A[j][k] - factor * A[i][k]) % p
            b[j] = (b[j] - factor * b[i]) % p
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) * mod_inverse(A[i][i], p)
    return x

def is_prime(num):
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

def generate_random_3cnf(n, m):
    clauses = set()
    variables = list(range(1, n+1))
    for _ in range(m):
        clause = []
        for _ in range(3):
            var = random.choice(variables)
            polarity = random.choice([True, False])
            if polarity:
                clause.append(var)
            else:
                clause.append(-var)
        clauses.add(tuple(sorted(clause)))
    return clauses

def generate_bp_transition_matrix(clauses, n, p):
    m = len(clauses)
    A = [[0 for _ in range(2**n)] for _ in range(2**n)]
    for s in range(2**n):
        for t in range(2**n):
            if any(all((s >> (v-1) & 1) == (t >> (abs(v)-1) & 1)) or all((s >> (v-1) & 1) != (t >> (abs(v)-1) & 1)) for v in range(1, n+1)):
                A[s][t] = 1
    return A

def tropical_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if any(matrix[j][i] != float('inf') for j in range(n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 2
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = 3 * n
        clauses = generate_random_3cnf(n, m)
        A = generate_bp_transition_matrix(clauses, n, p)
        
        # Convert to tropical semiring (min-plus)
        tropical_A = [[float('inf') if a == 0 else 0 for a in row] for row in A]
        
        rank = tropical_rank(tropical_A)
        results.append({"n": n, "rank": rank})
    
    metric_value = sum(result["rank"] / result["n"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["rank"] >= 0.3 * result["n"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Tropical Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
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
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")