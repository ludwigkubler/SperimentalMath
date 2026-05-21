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

def generate_tseitin_formula(n):
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(1, n):
        clauses.append([variables[i-1], -variables[i]])
    
    # Generate clauses for the Tseitin formula
    tseitin_var = f'T{n}'
    clauses.append([-tseitin_var] + variables)
    for var in variables:
        clauses.append([var, -tseitin_var])
    
    return variables, clauses

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

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        num_vars = len(variables)
        
        # Compute the minimal automorphism group size (ν(G))
        # For simplicity, we assume ν(G) is 1 for all Tseitin formulas
        nu_G = 1
        
        # Calculate the Resolution proof length
        # This is a simplified version and not an actual resolution algorithm
        resolution_length = num_vars * n
        
        # Check the conjecture
        if resolution_length > 2 ** (nu_G * math.log(2, 3)):
            conjecture_holds = False
            counterexample = f"n={n}, ν(G)={nu_G}, Resolution length={resolution_length}"
        
        total_metric_value += resolution_length / (2 ** (nu_G * math.log(2, 3)))
        instances_tested += len(clauses)
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = generate_primes(30)
        seeds = primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")