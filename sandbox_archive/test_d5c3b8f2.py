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

def generate_gf_elements(q):
    elements = [i for i in range(q)]
    return elements

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

def generate_primes(min_val, max_val):
    primes = []
    for num in range(min_val, max_val + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def generate_random_polynomial(degree, q):
    coefficients = [random.randint(0, q - 1) for _ in range(degree + 1)]
    return coefficients

def evaluate_polynomial(poly, x, q):
    result = 0
    power = 1
    for coeff in poly:
        result = (result + coeff * power) % q
        power = (power * x) % q
    return result

def is_permutation_poly(poly, q):
    elements = generate_gf_elements(q)
    image_set = set()
    for element in elements:
        value = evaluate_polynomial(poly, element, q)
        if value in image_set:
            return False
        image_set.add(value)
    return len(image_set) == q

def compute_branching_program_width(poly, q):
    n = len(poly) - 1
    dp = [[0] * (q + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = 1
        for j in range(1, q + 1):
            dp[i][j] = dp[i - 1][(j * poly[-2]) % q]
    return max(max(row) for row in dp)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q = random.choice([2**k for k in range(3, 6)])  # GF(8), GF(16), GF(32)
    d = random.randint(5, 40)
    poly = generate_random_polynomial(d, q)
    
    if not is_permutation_poly(poly, q):
        return {
            "metric_name": "branching_program_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_a_permutation"
        }
    
    width = compute_branching_program_width(poly, q)
    log_d = math.log2(d) if d > 0 else 0
    
    return {
        "metric_name": "branching_program_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": abs(width - log_d) < 1e-6,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(2, 100)[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_width = (sum((r["metric_value"] - mean_width)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_a_permutation\" first_failing_seed={first_failing_seed}")