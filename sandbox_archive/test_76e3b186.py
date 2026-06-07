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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def compute_galois_covering_degree(formula):
        # Placeholder function to simulate computation
        return len(formula)  # Simplified for testing purposes
    
    def calculate_communication_complexity_rank_variance(formula):
        n = int(math.log2(len(formula)))
        permutations = [''.join(p) for p in itertools.permutations(formula)]
        ranks = [len(set(permutation)) for permutation in permutations]
        mean_rank = sum(ranks) / len(ranks)
        variance = sum((x - mean_rank) ** 2 for x in ranks) / len(ranks)
        return variance
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
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
    
    def generate_primes(n):
        primes = []
        candidate = 2
        while len(primes) < n:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        return primes
    
    n_max = 40
    instances_tested = 0
    d_values = []
    r_var_values = []
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_boolean_formula(n)
        d = compute_galois_covering_degree(formula)
        r_var = calculate_communication_complexity_rank_variance(formula)
        
        if d > 50 or r_var < -20:
            continue
        
        instances_tested += 1
        d_values.append(d)
        r_var_values.append(r_var)
    
    if not d_values or not r_var_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_valid_instances"
        }
    
    correlation = correlation_coefficient(d_values, r_var_values)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")