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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def log_base(x, base):
    if x <= 0 or base <= 0 or base == 1:
        return float('inf')
    return math.log(x) / math.log(base)

def tropical_rank(orbit_set):
    if not orbit_set:
        return 0
    max_length = 0
    for row in orbit_set:
        unique_elements = set(map(tuple, row))
        max_length = max(max_length, len(unique_elements))
    return max_length

def generate_random_resolution_proof(n):
    clauses = []
    for _ in range(n):
        literals = [random.choice([1, -1]) * random.randint(1, n) for _ in range(n)]
        clauses.append(literals)
    return clauses

def generate_random_dpll_proof(n):
    clauses = []
    variables = set(range(1, n + 1))
    while variables:
        literal = random.choice(list(variables)) * random.choice([1, -1])
        clauses.append([literal])
        if literal > 0:
            variables.remove(literal)
        else:
            variables.remove(-literal)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    resolution_ranks = []
    dpll_ranks = []
    
    for n in n_values:
        resolution_proof = generate_random_resolution_proof(n)
        dpll_proof = generate_random_dpll_proof(n)
        
        # Compute tropical rank of Weyl group orbit for resolution proof
        resolution_orbit = [[1] * n]
        for clause in resolution_proof:
            new_orbit = []
            for row in resolution_orbit:
                newRow = [row[i] + literal for i, literal in enumerate(clause)]
                new_orbit.append(newRow)
            resolution_orbit.extend(new_orbit)
        resolution_rank = tropical_rank(resolution_orbit)
        resolution_ranks.append(resolution_rank)
        
        # Compute tropical rank of Weyl group orbit for DPLL proof
        dpll_orbit = [[1] * n]
        for literal in dpll_proof:
            new_orbit = []
            for row in dpll_orbit:
                newRow = [row[i] + literal for i in range(n)]
                new_orbit.append(newRow)
            dpll_orbit.extend(new_orbit)
        dpll_rank = tropical_rank(dpll_orbit)
        dpll_ranks.append(dpll_rank)
    
    resolution_mean = sum(resolution_ranks) / len(resolution_ranks)
    dpll_mean = sum(dpll_ranks) / len(dpll_ranks)
    kappa_n = log_base(factorial(n), 2) - log_base((factorial(n // 2)) ** 2, 2)
    
    if resolution_mean > dpll_mean + kappa_n:
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "tropical_rank_difference",
        "metric_value": resolution_mean - dpll_mean,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"resolution_mean={resolution_mean}, dpll_mean={dpll_mean}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    resolution_means = [r["metric_value"] for r in results]
    dpll_means = [r["metric_value"] + (log_base(factorial(n), 2) - log_base((factorial(n // 2)) ** 2, 2)) for n in [5, 10, 15, 20, 30, 40]]
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(resolution_means) / len(resolution_means)} std={math.sqrt(sum((x - sum(resolution_means) / len(resolution_means)) ** 2 for x in resolution_means) / len(resolution_means))} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_mean < dpll_mean + kappa_n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")