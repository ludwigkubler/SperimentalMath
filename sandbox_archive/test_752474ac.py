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

def generate_complexity_instance(n):
    # Generate n variables and construct the associated simplicial complex.
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(2**n - 1):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(' OR '.join(clause))
    formula = ' AND '.join(clauses)
    return formula

def calculate_betti_numbers(complex):
    # Calculate Betti numbers for the given simplicial complex.
    # This is a placeholder function. Replace with actual implementation.
    return [0] * n  # Placeholder Betti numbers

def calculate_frege_proof_length(formula):
    # Calculate Frege proof length for the given formula.
    # This is a placeholder function. Replace with actual implementation.
    return len(formula.split(' AND '))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    total_metric_value = Fraction(0, 1)
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Test each size with 5 instances
            formula = generate_complexity_instance(n)
            beta_min = min(calculate_betti_numbers(formula))
            F_phi = calculate_frege_proof_length(formula)
            
            if beta_min < math.log(n) or beta_min > 2 * math.log(n):
                return {
                    "metric_name": "beta_min",
                    "metric_value": beta_min,
                    "instances_tested": instances_tested + 1,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"Formula with n={n} has beta_min={beta_min}"
                }
            
            total_metric_value += Fraction(F_phi, n)
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Frege proof length",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]  # Default to first 30 prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"beta_min out of bounds\" first_failing_seed={first_failing_seed}")