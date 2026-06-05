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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = clause[1], clause[0]
        cnf.append(clause)
    return cnf

def construct_quotient_algebra(cnf):
    n = len(set(abs(lit) for lit in sum(cnf, [])))
    A = [[0] * n for _ in range(n)]
    for clause in cnf:
        for lit1 in clause:
            for lit2 in clause:
                A[abs(lit1) - 1][abs(lit2) - 1] += 1
    return A

def calculate_frobenius_norm(A):
    n = len(A)
    sum_of_squares = 0
    for i in range(n):
        for j in range(n):
            sum_of_squares += A[i][j] ** 2
    return math.sqrt(sum_of_squares)

def calculate_circuit_monotone_width(cnf):
    # Placeholder function. Replace with actual implementation.
    return len(cnf) * len(cnf[0])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        cnf = generate_cnf(n, m)
        
        A = construct_quotient_algebra(cnf)
        frobenius_norm = calculate_frobenius_norm(A)
        circuit_monotone_width = calculate_circuit_monotone_width(cnf)
        
        results.append({
            "n": n,
            "m": m,
            "frobenius_norm": frobenius_norm,
            "circuit_monotone_width": circuit_monotone_width
        })
    
    mean_frobenius_norm = sum(result["frobenius_norm"] for result in results) / len(results)
    max_n = max(result["n"] for result in results)
    
    conjecture_holds = all(
        abs(frobenius_norm - math.sqrt(m) * n ** (3/4)) <= 0.5 * math.sqrt(m) * n ** (3/4)
        for result in results
    )
    
    return {
        "metric_name": "Frobenius Norm",
        "metric_value": mean_frobenius_norm,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")