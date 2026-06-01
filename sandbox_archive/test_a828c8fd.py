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

def generate_sat_instance(n, num_clauses):
    clauses = set()
    while len(clauses) < num_clauses:
        clause = tuple(sorted(random.sample(range(1, n + 1), 2)))
        if clause not in clauses:
            clauses.add(clause)
    return clauses

def polynomial_modulo(poly, p):
    return [coeff % p for coeff in poly]

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = next((i for i in range(rank, m) if A[i][j] != 0), None)
        if i_max is not None:
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(rank + 1, m):
                factor = -A[i][j] / A[rank][j]
                A[i][j:] = [x + factor * y for x, y in zip(A[i][j:], A[rank][j:])]
            rank += 1
    return rank

def modular_function_rank(poly, p):
    n = len(poly)
    A = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        A[i][:i+1] = poly[:i+1]
        A[i][n] = -poly[i]
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            num_clauses = random.randint(1, n)
            clauses = generate_sat_instance(n, num_clauses)
            poly = [0] * (num_clauses + 1)
            for clause in clauses:
                poly[clause[0]] += 1
                poly[clause[1]] += 1
            p = random.randint(2, n)
            mfr_value = modular_function_rank(polynomial_modulo(poly, p), p)
            results.append((mfr_value, num_clauses))
    
    if len(results) < 30:
        return {
            "metric_name": "modular_function_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mfr_values, unique_clauses = zip(*results)
    mean_mfr = sum(mfr_values) / len(mfr_values)
    std_mfr = math.sqrt(sum((x - mean_mfr) ** 2 for x in mfr_values) / len(mfr_values))
    correlation_coefficient = (sum((mfr_values[i] - mean_mfr) * (unique_clauses[i] - sum(unique_clauses) / len(unique_clauses)) for i in range(len(results))) /
                               (len(results) * std_mfr * math.sqrt(sum((x - sum(unique_clauses) / len(unique_clauses)) ** 2 for x in unique_clauses))))
    
    return {
        "metric_name": "modular_function_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction=1.0")
    elif any(not result["conjecture_holds"] and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")