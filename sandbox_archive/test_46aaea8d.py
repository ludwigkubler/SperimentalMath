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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def inverse_mod(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse does not exist")
    else:
        return x % m

def p_adic_valuation(n, p):
    val = 0
    while n % p == 0 and n != 0:
        n //= p
        val += 1
    return val

def min_p_adic_valuation(roots):
    return min(p_adic_valuation(root, 2) for root in roots if root != 0)

def generate_polynomial(degree, coeff_range):
    coefficients = [random.randint(*coeff_range) for _ in range(degree + 1)]
    return coefficients

def evaluate_polynomial(poly, x):
    result = 0
    power = 1
    for coeff in poly:
        result += coeff * power
        power *= x
    return result

def construct_ac0_circuit(poly, degree):
    # This is a placeholder for constructing an AC0 circuit.
    # For simplicity, we'll just count the number of terms in the polynomial.
    return len(poly)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_tests = 30
    total_val_p = 0
    total_circuit_size = 0
    
    for _ in range(n_tests):
        degree = random.randint(1, 40)
        coeff_range = (-10, 10)
        poly = generate_polynomial(degree, coeff_range)
        
        roots = []
        for x in range(-10, 11):  # Check for integer roots in a small range
            if evaluate_polynomial(poly, x) == 0:
                roots.append(x)
        
        val_p = min_p_adic_valuation(roots)
        circuit_size = construct_ac0_circuit(poly, degree)
        
        total_val_p += val_p
        total_circuit_size += circuit_size
    
    mean_val_p = total_val_p / n_tests
    mean_circuit_size = total_circuit_size / n_tests
    
    correlation_coefficient = (n_tests * sum(val_p * circuit_size for val_p, circuit_size in zip(roots, roots)) -
                               n_tests * mean_val_p * mean_circuit_size) / math.sqrt(
        (n_tests * sum(val_p ** 2 for val_p in roots) - n_tests * mean_val_p ** 2) *
        (n_tests * sum(circuit_size ** 2 for circuit_size in roots) - n_tests * mean_circuit_size ** 2))
    
    conjecture_holds = correlation_coefficient > 0
    counterexample = "" if conjecture_holds else "Correlation coefficient is non-positive"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n_tests,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_val_p = sum(result["metric_value"] for result in results) / len(results)
    std_val_p = math.sqrt(sum((result["metric_value"] - mean_val_p) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_val_p} std={std_val_p} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient is non-positive\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")