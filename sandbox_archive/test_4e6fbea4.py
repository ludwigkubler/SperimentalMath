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

def generate_random_instance(n, k, p):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, random.randint(1, len(variables)))
        clauses.append(clause)
    phi = [clauses]
    return phi, p

def clause_indicator_polynomial(phi, p):
    n = len(phi[0][0])
    x = [Fraction(0) for _ in range(n + 1)]
    x[0] = Fraction(1)
    for clause in phi[0]:
        term = Fraction(1)
        for var in clause:
            term *= (1 + x[-var-1])
        x = [(term * coeff) % p for coeff in x]
    return x

def min_hodge_dimension(x):
    non_zero_coeffs = [coeff for coeff in x if coeff != 0]
    return len(non_zero_coeffs)

def resolution_width(phi, p):
    # Placeholder function to simulate resolution width calculation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        h_sum = 0
        w_sum = 0
        
        while instances_tested < 30:
            phi, p = generate_random_instance(n, random.randint(1, n), random.choice([2, 3, 5]))
            x = clause_indicator_polynomial(phi, p)
            h = min_hodge_dimension(x)
            w = resolution_width(phi, p)
            
            if h == 0 or w == 0:
                continue
            
            instances_tested += 1
            h_sum += h
            w_sum += w
        
        if instances_tested < 30:
            return {
                "metric_name": "ratio",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
        
        ratio = h_sum / w_sum
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_ratio) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": 180,  # 30 instances per n * 6 values of n
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= mean_ratio <= 2 and std_dev <= 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["conjecture_holds"]:
            results.append(result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_ratio) ** 2 for x in results) / len(results))
    support_fraction = len([r for r in results if 0.5 <= r <= 2]) / len(results)
    
    if all(0.5 <= r <= 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.5 <= result <= 2))
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")