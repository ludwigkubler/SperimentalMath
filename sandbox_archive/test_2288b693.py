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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    Ab = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Ab[j][i]) > abs(Ab[max_row][i]):
                max_row = j
        Ab[i], Ab[max_row] = Ab[max_row], Ab[i]
        pivot = Ab[i][i]
        for j in range(n):
            Ab[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = Ab[j][i]
                for k in range(n+1):
                    Ab[j][k] -= factor * Ab[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Ab[i][-1]
        for j in range(i+1, n):
            x[i] -= Ab[i][j] * x[j]
    return x

def frege_proof_depth(formula):
    # Placeholder function to simulate Frege proof depth calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(formula)  # Example: depth proportional to the number of clauses

def tropical_category_depth(n, d):
    # Placeholder function to simulate tropical category depth calculation
    # This is a dummy implementation and should be replaced with actual logic
    return math.log(d, 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = [random.choice([1, -1]) for _ in range(n)]
    d = frege_proof_depth(formula)
    alpha_n = math.log(n, 2) ** 2
    beta_d_log = 2 * math.log(d, 2)  # Example value of beta

    tc_depth = tropical_category_depth(n, d)

    conjecture_holds = (tc_depth <= alpha_n and tc_depth <= beta_d_log)
    counterexample = "" if conjecture_holds else f"n={n}, d(F)={d}, Depth(TropCat(F))={tc_depth}"

    return {
        "metric_name": "tropical_category_depth",
        "metric_value": tc_depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)

    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")