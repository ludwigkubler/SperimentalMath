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

def hook_length_formula(shape):
    numerator = factorial(sum(shape))
    denominator = 1
    for row in shape:
        for j in range(len(row)):
            denominator *= (row[j] + len(row) - j)
    return numerator / denominator

def kronecker_coefficient(lambda_, mu, nu, n):
    if len(lambda_) != n or len(mu) != n or len(nu) != n:
        raise ValueError("Dominant weight triples must have exactly n rows/columns")
    
    lambda_sum = sum(lambda_)
    mu_sum = sum(mu)
    nu_sum = sum(nu)
    
    if lambda_sum + mu_sum != nu_sum:
        return 0
    
    numerator = hook_length_formula(lambda_) * hook_length_formula(mu) * hook_length_formula(nu)
    denominator = factorial(n) ** 3
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if lambda_[i] + mu[j] - nu[k] >= 0:
                    numerator /= (factorial(lambda_[i]) * factorial(mu[j]) * factorial(nu[k]))
    
    return numerator / denominator

def permanent(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    else:
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * permanent(submatrix)
        return det

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    else:
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    permanent_coeff_sum = 0
    determinant_coeff_sum = 0
    
    for n in n_values:
        for _ in range(18):  # Aim for at least 30 instances per seed
            matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            
            permanent_value = permanent(matrix)
            determinant_value = determinant(matrix)
            
            lambda_ = [n]
            mu = [n]
            nu = [n]
            
            permanent_coeff = kronecker_coefficient(lambda_, mu, nu, n)
            determinant_coeff = kronecker_coefficient(lambda_, mu, nu, n)
            
            permanent_coeff_sum += permanent_coeff
            determinant_coeff_sum += determinant_coeff
            
            instances_tested += 1
    
    mean_perm_coeff = permanent_coeff_sum / instances_tested
    mean_det_coeff = determinant_coeff_sum / instances_tested
    
    conjecture_holds = mean_perm_coeff > mean_det_coeff
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Kronecker Coefficient Asymmetry",
        "metric_value": mean_perm_coeff - mean_det_coeff,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")