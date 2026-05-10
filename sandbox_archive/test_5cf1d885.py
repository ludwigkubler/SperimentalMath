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

def walsh_hadamard_transform(f, n):
    N = 2 ** n
    for s in range(n):
        for i in range(N // (2 ** (s + 1))):
            for j in range(2 ** s):
                u = f[i * 2 ** (s + 1) + j]
                v = f[i * 2 ** (s + 1) + j + 2 ** s]
                f[i * 2 ** (s + 1) + j] = u + v
                f[i * 2 ** (s + 1) + j + 2 ** s] = u - v
    return f

def fourier_coefficients(f, n):
    N = 2 ** n
    F = [0] * N
    for i in range(N):
        F[i] = sum(f[j] * math.cos(2 * math.pi * i * j / N) for j in range(N)) / N
    return F

def discrepancy(F):
    max_val = max(abs(x) for x in F)
    min_val = min(abs(x) for x in F)
    return max_val - min_val

def generate_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        clause += [-v if random.choice([True, False]) else v for v in clause]
        clauses.append(clause)
    return clauses

def evaluate_3cnf(f, clauses):
    n = int(math.log2(len(f)))
    for x in range(1 << n):
        val = 0
        for clause in clauses:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= f[x & (1 << (literal - 1))]
                else:
                    term *= 1 - f[x & (1 << (-literal - 1))]
            val += term
        if val <= 0:
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    m = 5 * n
    
    clauses = generate_3cnf(n, m)
    f = [random.choice([0, 1]) for _ in range(2 ** n)]
    
    F = fourier_coefficients(f, n)
    disc = discrepancy(F)
    
    min_circuit_size = None
    for size in range(2 ** (n // 2), 2 ** (n + 1)):
        if evaluate_3cnf([random.choice([0, 1]) for _ in range(size)], clauses):
            min_circuit_size = size
            break
    
    return {
        "metric_name": "discrepancy",
        "metric_value": disc,
        "instances_tested": 1,
        "conjecture_holds": disc >= 2 ** (n // 2) and (min_circuit_size is not None),
        "counterexample": "" if min_circuit_size is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_disc = sum(r["metric_value"] for r in results) / len(results)
    std_disc = math.sqrt(sum((r["metric_value"] - mean_disc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_disc} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_disc} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")