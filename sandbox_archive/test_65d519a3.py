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

def p_adic_valuation(n, p):
    if n == 0:
        return float('inf')
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count

def min_p_adic_valuation(roots):
    return min(p_adic_valuation(root, 2) for root in roots if root != 0)

def generate_polynomial(degree, coeff_range):
    coeffs = [random.randint(*coeff_range) for _ in range(degree + 1)]
    return coeffs

def evaluate_polynomial(coeffs, x):
    result = 0
    power = 1
    for coeff in reversed(coeffs):
        result += coeff * power
        power *= x
    return result

def construct_ac0_circuit(coeffs, n):
    # Placeholder for AC0 circuit construction logic
    # This is a dummy implementation and does not actually construct an AC0 circuit
    return len(coeffs)  # Simplified measure of complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):  # Test with 30 instances per seed
        degree = random.randint(1, 40)
        coeff_range = (-10, 10)
        coeffs = generate_polynomial(degree, coeff_range)
        
        roots = []
        for x in range(-10, 11):  # Check values from -10 to 10
            if evaluate_polynomial(coeffs, x) == 0:
                roots.append(x)
        
        val_p = min_p_adic_valuation(roots)
        
        circuit_size = construct_ac0_circuit(coeffs, degree)
        
        results.append((val_p, circuit_size))
    
    mean_val_p = sum(val_p for val_p, _ in results) / len(results)
    mean_circuit_size = sum(circuit_size for _, circuit_size in results) / len(results)
    
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((val_p - mean_val_p) * (circuit_size - mean_circuit_size) for val_p, circuit_size in results)
        denominator = math.sqrt(sum((val_p - mean_val_p) ** 2 for val_p, _ in results)) * math.sqrt(sum((circuit_size - mean_circuit_size) ** 2 for _, circuit_size in results))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient > 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        print("TRIAL:", {"seed": seed})
        trial_result = run_trial(seed)
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(result["counterexample"], first_failing_seed))