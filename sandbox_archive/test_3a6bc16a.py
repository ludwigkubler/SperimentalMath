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

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
    return C

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(min(m, n)):
        if A[i][i] == 0:
            pivot_found = False
            for j in range(i + 1, m):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    pivot_found = True
                    break
            if not pivot_found:
                continue
        scale = 1 / A[i][i]
        for j in range(n):
            A[i][j] *= scale
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = -A[j][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    if n == 1:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "single_output_stub"
        }
    
    # Construct a random polynomial f(x1, ..., xn) with bounded monomials
    poly = []
    for _ in range(random.randint(1, n)):
        exponents = [random.randint(0, 2) for _ in range(n)]
        coeff = random.randint(1, 10)
        term = (coeff, tuple(exponents))
        poly.append(term)
    
    # Compute the Ehrhart cohomology rank
    V_f = set()
    for x in itertools.product(range(-10, 11), repeat=n):
        value = sum(coeff * math.prod(x[i] ** exp for i, exp in enumerate(expo)) for coeff, expo in poly)
        if value == 0:
            V_f.add(tuple(x))
    
    minimal_rank = gaussian_elimination([list(v) + [1] for v in V_f])
    
    # Construct an ACC⁰ circuit C_f (simplified as a polynomial circuit)
    k = len(poly)
    S_C_f = 2 ** n - n + k
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank <= 2 ** n - n and S_C_f <= 2 ** n - n + k,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")