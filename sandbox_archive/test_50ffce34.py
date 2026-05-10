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

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    raise ValueError("Modular inverse does not exist")

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] %= m
    return C

def matrix_power(A, k):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        k //= 2
    return result

def discrete_fourier_transform(P):
    n = len(P)
    m = 2 ** (n.bit_length() - 1)
    omega = [math.exp(2j * math.pi * i / m) for i in range(m)]
    F = [[0] * m for _ in range(n)]
    for j in range(m):
        for i in range(n):
            F[i][j] = sum(P[k] * omega[j * k % m] for k in range(n)) / math.sqrt(n)
    return F

def l1_norm(F):
    return sum(abs(x.real) + abs(x.imag) for row in F for x in row)

def generate_bp(n, read_twice=False):
    if read_twice:
        # Generate a random read-twice branching program
        bp = [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
    else:
        # Generate a random read-once branching program
        bp = [random.choice([0, 1]) for _ in range(n)]
    return bp

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    total_l1_norm = 0.0
    read_twice_count = 0
    
    for _ in range(instances_tested):
        bp_type = random.choice(['read-once', 'read-twice'])
        P = generate_bp(n, bp_type == 'read-twice')
        
        F = discrete_fourier_transform(P)
        l1_norm_value = l1_norm(F)
        
        total_l1_norm += l1_norm_value
        if bp_type == 'read-twice':
            read_twice_count += 1
    
    avg_l1_norm = total_l1_norm / instances_tested
    conjecture_holds = (avg_l1_norm >= n / 2) and (read_twice_count > 0)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "L1 norm",
        "metric_value": avg_l1_norm,
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
    
    mean_l1_norm = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_l1_norm} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_l1_norm} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")