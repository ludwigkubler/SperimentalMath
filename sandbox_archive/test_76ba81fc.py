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
    n = len(shape)
    total = 0
    for i in range(n):
        for j in range(len(shape[i])):
            total += shape[i][j] + (n - i) + (len(shape[i]) - j) - 1
    return factorial(total)

def kronecker_coefficient(lambda_, mu, nu, n):
    if len(lambda_) != n or len(mu) != n or len(nu) != n:
        raise ValueError("Shape dimensions must match n")
    
    lambda_sum = sum(lambda_)
    mu_sum = sum(mu)
    nu_sum = sum(nu)
    
    if lambda_sum + mu_sum != nu_sum:
        return 0
    
    numerator = hook_length_formula([lambda_])
    denominator = 1
    for i in range(n):
        denominator *= hook_length_formula([mu[i]])
        denominator *= hook_length_formula([nu[i]])
    
    return numerator / denominator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        permanent_coeff_sum = 0
        determinant_coeff_sum = 0
        
        for _ in range(30):
            # Generate random Young diagrams with at most n rows/columns
            lambda_ = [random.randint(1, min(n, i + 1)) for i in range(n)]
            mu = [random.randint(1, min(n, i + 1)) for i in range(n)]
            nu = [random.randint(1, min(n, i + 1)) for i in range(n)]
            
            permanent_coeff = kronecker_coefficient(lambda_, mu, nu, n)
            determinant_coeff = kronecker_coefficient(mu, lambda_, nu, n)
            
            permanent_coeff_sum += permanent_coeff
            determinant_coeff_sum += determinant_coeff
        
        metric_value = permanent_coeff_sum / 30 - determinant_coeff_sum / 30
        total_metric_value += metric_value
        instances_tested += len(n_values) * 30
    
    conjecture_holds = all(metric_value > 0 for n in n_values for _ in range(30))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Kronecker Coefficient Asymmetry",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")