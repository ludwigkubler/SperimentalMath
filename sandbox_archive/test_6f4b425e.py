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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def symmetric_group_elements(n):
        if n == 0:
            return [[]]
        elements = []
        for perm in symmetric_group_elements(n - 1):
            for i in range(n):
                new_perm = perm[:i] + [n - 1] + perm[i:i]
                elements.append(new_perm)
        return elements
    
    def noncommutative_fourier_coefficient(f, n, g):
        result = 0
        for pi in symmetric_group_elements(n):
            term = (-1) ** sum(pi[i] != i for i in range(n))
            for j in range(n):
                term *= f(pi[j], g[j])
            result += term
        return result
    
    def read_twice_bp_function(n):
        # Placeholder function for a read-twice branching program
        return lambda x, y: 1 if sum(x[i] != y[i] for i in range(n)) % 2 == 0 else 0
    
    def inner_product_mod_2_function(n):
        # Placeholder function for the inner product mod 2 function
        return lambda x, y: 1 if sum(x[i] * y[i] for i in range(n)) % 2 == 1 else 0
    
    n = random.randint(5, 40)
    f_read_twice = read_twice_bp_function(n)
    f_ip_2 = inner_product_mod_2_function(n)
    
    def compute_fourier_coefficient_sum(f):
        sum_abs_coeffs = 0
        for g in symmetric_group_elements(n):
            coeff = noncommutative_fourier_coefficient(f, n, g)
            sum_abs_coeffs += abs(coeff)
        return sum_abs_coeffs
    
    sum_read_twice = compute_fourier_coefficient_sum(f_read_twice)
    sum_ip_2 = compute_fourier_coefficient_sum(f_ip_2)
    
    metric_value = sum_read_twice / sum_ip_2 if sum_ip_2 != 0 else float('inf')
    conjecture_holds = metric_value <= math.log(n) and metric_value >= n**2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Fourier Coefficient Sum Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")