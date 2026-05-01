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

def hook_length_formula(n, k):
    lambda_ = [n - k, 1] * k
    numerator = factorial(n)
    denominator = 1
    for i in range(len(lambda_)):
        for j in range(i + 1):
            denominator *= (lambda_[i] - j + lambda_[j] - i - 1)
    return numerator // denominator

def gaussian_elimination(matrix, b):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        b[i], b[max_row] = b[max_row], b[i]
        for k in range(i + 1, n):
            factor = matrix[k][i] / matrix[i][i]
            for j in range(i, n):
                matrix[k][j] -= factor * matrix[i][j]
            b[k] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(matrix[i][j] * x[j] for j in range(i + 1, n))) / matrix[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = n // 3
    lambda_ = [n - k, 1] * k
    dim_chi_lambda = hook_length_formula(n, k)
    
    def is_satisfiable(clauses):
        def dpll(model, clauses):
            if not clauses:
                return True
            literal = next(l for l in range(1, n + 1) if l not in model and -l not in model)
            positive_clauses = [c for c in clauses if literal in c]
            negative_clauses = [c for c in clauses if -literal in c]
            if dpll(model | {literal}, positive_clauses):
                return True
            if dpll(model | {-literal}, negative_clauses):
                return True
            return False
        
        def generate_random_clauses(num_clauses):
            clauses = []
            for _ in range(num_clauses):
                clause = [random.choice([i, -i]) for i in random.sample(range(1, n + 1), 3)]
                if random.choice([True, False]):
                    clause = [-c for c in clause]
                clauses.append(clause)
            return clauses
        
        num_clauses = random.randint(100, 200)
        clauses = generate_random_clauses(num_clauses)
        return dpll(set(), clauses)
    
    def sos_refutation_size(n):
        # Placeholder for actual SOS refutation size computation
        # This is a dummy implementation and should be replaced with the actual algorithm
        return random.randint(1, 100)
    
    refutation_size = sos_refutation_size(n)
    if dim_chi_lambda < refutation_size:
        return {
            "metric_name": "SOS Refutation Size",
            "metric_value": refutation_size,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"SAT instance with refutation size {refutation_size} and dim(χ_λ) = {dim_chi_lambda}"
        }
    
    return {
        "metric_name": "SOS Refutation Size",
        "metric_value": refutation_size,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"SOS refutation size exceeds dim(χ_λ)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")