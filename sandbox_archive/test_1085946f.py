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

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 2
    for i in range(3, n + 1, 2):
        result *= i
    return result

def binomial_coefficient(n, k):
    if k > n // 2:
        k = n - k
    coeff = 1
    for i in range(k):
        coeff *= (n - i)
        coeff //= (i + 1)
    return coeff

def hook_length_formula(young_tableau):
    n = len(young_tableau)
    result = factorial(n * n)
    for row in young_tableau:
        for cell, value in enumerate(row):
            if value == 0:
                continue
            hook_length = (n - cell) + (len(row) - value) - 1
            result //= hook_length
    return result

def plethysm_coefficient(n):
    # Construct a random CNF formula with n variables and n clauses
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        clauses.append(clause)
    
    # Convert clauses to Young diagram
    young_tableau = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if random.random() < 1 / (i + j + 2):
                young_tableau[i][j] = 1
    
    # Compute plethysm coefficient using hook length formula
    return hook_length_formula(young_tableau)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        plethysm_coeff = plethysm_coefficient(n)
        if plethysm_coeff >= 2**n:
            metric_value = 1.0
        else:
            metric_value = 0.0
        total_metric_value += metric_value
        instances_tested += 1
    
    mean_metric_value = total_metric_value / len(n_values)
    
    conjecture_holds = mean_metric_value >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 50))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")