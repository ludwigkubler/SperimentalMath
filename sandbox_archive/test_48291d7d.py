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

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def generate_3cnf(num_vars, num_clauses):
    clauses = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, num_vars)
            sign = random.choice([-1, 1])
            if (var, sign) not in clause and (-var, -sign) not in clause:
                clause.add((var, sign))
        clauses.append(clause)
    return clauses

def p_adic_valuation(n, p):
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count

def dpll_tree_size(num_vars):
    return 2 ** (num_vars // 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    num_vars = random.randint(5, 40)
    num_clauses = random.randint(3 * num_vars // 2, 6 * num_vars // 2)
    formula = generate_3cnf(num_vars, num_clauses)
    
    p = 3
    solutions_mod_p = 0
    
    for assignment in range(1 << num_vars):
        is_valid = True
        for clause in formula:
            if all((assignment >> (var - 1) & 1 == sign) for var, sign in clause):
                break
        else:
            solutions_mod_p += 1
    
    valuation = p_adic_valuation(solutions_mod_p, p)
    expected_tree_size = dpll_tree_size(num_vars)
    
    return {
        "metric_name": "p-adic Valuation",
        "metric_value": valuation,
        "instances_tested": 1,
        "conjecture_holds": abs(valuation - math.log2(num_vars)) < 0.5 and abs(solutions_mod_p - expected_tree_size) < 1e-6,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_valuation = sum(result["metric_value"] for result in results) / len(results)
    std_valuation = math.sqrt(sum((result["metric_value"] - mean_valuation) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_valuation} std={std_valuation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")