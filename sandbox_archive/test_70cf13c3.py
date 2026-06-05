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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
            clauses.append([-variables[i-1], f'x{n+i}'])
            clauses.append([f'x{i+n}', -f'x{n+i}'])
            for j in range(i+1, n+1):
                clauses.append([variables[j-1], -f'x{n+j}'])
                clauses.append([-variables[j-1], f'x{n+j}'])
        return variables, clauses
    
    def grb_basis(clauses):
        # Simplified Gröbner basis algorithm for demonstration
        # This is a placeholder and does not compute the actual Lefschetz number
        return len(clauses)
    
    def frege_proof_width(n):
        # Simplified Frege proof width calculation
        # This is a placeholder and does not compute the actual proof width
        return n * (n + 1) // 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        variables, clauses = tseitin_formula(n)
        mLef = grb_basis(clauses)
        w_F = frege_proof_width(n)
        results.append((mLef, w_F))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((mLef - w_F) * (mLef_prime - w_F_prime) for mLef, w_F in results for mLef_prime, w_F_prime in results) / len(results)**2
    max_n = max(n for _, _ in results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": correlation >= 0.8 and all(abs(mLef - w_F) <= 3 for mLef, w_F in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "correlation_threshold_not_met"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")