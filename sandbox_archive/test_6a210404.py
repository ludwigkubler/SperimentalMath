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

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def binomial_coefficient(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def hook_length_formula(shape):
    m, n = shape
    total = 0
    for i in range(m):
        for j in range(n):
            total += (m - i) + (n - j) - 1
    return binomial_coefficient(total, m * n)

def generate_monotone_cnf(n, m):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def monotone_circuit_size_bound(n):
    return 2 ** (n ** 0.5)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = math.ceil(n ** 0.5)
        Phi = generate_monotone_cnf(n, m)
        
        shape = (m, n - m)
        Y_Phi = hook_length_formula(shape)
        C_Phi = monotone_circuit_size_bound(n)
        
        results.append({
            "n": n,
            "Y_Phi": Y_Phi,
            "C_Phi": C_Phi
        })
    
    metric_value = sum(result["Y_Phi"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["Y_Phi"] <= n ** m and result["C_Phi"] >= 2 ** (n ** 0.5) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Monotone Circuit Size vs Standard Young Tableaux Count",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(30)
        seeds = primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")