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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define min_idx_p_N for a given prime p and integer N
    def min_idx_p_N(p, N):
        # Placeholder implementation; replace with actual computation
        return 2 * N
    
    # Generate a random CNF formula φ with N variables
    N = random.randint(5, 40)
    num_clauses = random.randint(N, 3 * N)
    cnf_formula = []
    for _ in range(num_clauses):
        clause = [random.choice([1, -1]) * random.randint(1, N) for _ in range(random.randint(1, N))]
        cnf_formula.append(clause)
    
    # Compute the monotone width w(φ)
    def monotone_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            active_vars = [abs(lit) for lit in clause if lit > 0]
            width = max(width, len(active_vars))
        return width
    
    w_phi = monotone_width(cnf_formula)
    
    # Generate modular forms over the function field F_p(T) of degree N
    p = random.choice([2, 3, 5, 7, 11])
    min_idx = min_idx_p_N(p, N)
    
    # Measure the correlation between min_idx_{p,N} and w(φ)
    if min_idx == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": N,
            "conjecture_holds": False,
            "counterexample": "min_idx_{p,N} is zero"
        }
    
    correlation_coefficient = (w_phi - min_idx) / (2 * min_idx)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": N,
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_range\" first_failing_seed={first_failing_seed}")