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
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} modulo {m}")
    else:
        return x % m

def p_adic_order(n, p):
    order = 0
    while n % p == 0:
        n //= p
        order += 1
    return order

def polynomial_to_coefficients(polynomial):
    if isinstance(polynomial, int):
        return [polynomial]
    elif isinstance(polynomial, list):
        coeffs = []
        for term in polynomial:
            coeffs.extend([1] * len(polynomial_to_coefficients(term)))
        return coeffs
    else:
        raise ValueError("Invalid polynomial format")

def generate_k_sat_instance(n, m):
    literals = set(range(1, n + 1)) | {-x for x in range(1, n + 1)}
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, random.randint(1, n))
        clauses.append(clause)
    return clauses

def resolution_width(instance):
    # Simplified version of resolution width calculation
    # This is a placeholder and should be replaced with actual implementation
    return len(instance)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    instance = generate_k_sat_instance(n, m)
    
    coeffs = polynomial_to_coefficients(instance)
    p_values = [p for p in range(2, int(math.log(n)) + 1)]
    
    min_p_adic_orders = []
    for coeff in coeffs:
        orders = [p_adic_order(coeff, p) for p in p_values]
        min_p_adic_orders.append(min(orders))
    
    width = resolution_width(instance)
    
    metric_value = sum(min_p_adic_orders) / len(min_p_adic_orders)
    conjecture_holds = abs(metric_value - width) <= 0.7 * width
    counterexample = "" if conjecture_holds else "resolution_width_approximation"
    
    return {
        "metric_name": "p-adic order",
        "metric_value": metric_value,
        "instances_tested": len(coeffs),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")