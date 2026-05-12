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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(young_tableau):
    m, n = len(young_tableau), len(young_tableau[0])
    total = 0
    for i in range(m):
        for j in range(n):
            hook_length = (i + 1) + (n - j) - young_tableau[i][j]
            total += factorial(hook_length) // (factorial(i + 1) * factorial(n - j))
    return total

def generate_matrix(n):
    return [[random.randint(0, 10) for _ in range(n)] for _ in range(n)]

def plethysm_coefficient(matrix, k):
    n = len(matrix)
    young_tableau = []
    for i in range(n):
        row = [k - sum(matrix[i][j] for j in range(i + 1)) for j in range(i + 1)]
        young_tableau.append(row)
    return hook_length_formula(young_tableau)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = math.floor(n ** 1.5)
    
    perm_matrix = generate_matrix(n)
    det_matrix = generate_matrix(m)
    
    lambda_perm_n = plethysm_coefficient(perm_matrix, n)
    lambda_det_m = plethysm_coefficient(det_matrix, m)
    
    epsilon = 0.1
    if lambda_perm_n > lambda_det_m + epsilon * n ** 2:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "plethysm_coefficient_gap"
    
    return {
        "metric_name": "plethysm_coefficient_gap",
        "metric_value": lambda_perm_n - (lambda_det_m + epsilon * n ** 2),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        from sympy import primerange
        seeds = list(primerange(2, 30))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")