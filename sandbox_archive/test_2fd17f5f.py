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

def generate_k_sat_instance(n, m):
    instance = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            literal = random.randint(1, n)
            if random.choice([True, False]):
                literal = -literal
            clause.add(literal)
        instance.append(list(clause))
    return instance

def generate_primes(limit):
    sieve = [True] * (limit + 1)
    for start in range(2, int(math.sqrt(limit)) + 1):
        if sieve[start]:
            for multiple in range(start*start, limit + 1, start):
                sieve[multiple] = False
    return [num for num, is_prime in enumerate(sieve) if is_prime and num > 1]

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def p_adic_order(coeff, prime):
    order = 0
    abs_coeff = abs(coeff)
    while abs_coeff % prime == 0:
        abs_coeff //= prime
        order += 1
    return order

def resolution_width(instance):
    # Simplified version of resolution width calculation
    # This is a placeholder and should be replaced with actual logic
    return len(instance)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    instance = generate_k_sat_instance(n, m)
    
    primes = generate_primes(int(math.log(n)) + 1)
    if not primes:
        return {
            "metric_name": "p-adic order correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "no_primes_found"
        }
    
    p_adic_orders = []
    for prime in primes:
        coeff = random.randint(-100, 100)
        order = p_adic_order(coeff, prime)
        p_adic_orders.append(order)
    
    width = resolution_width(instance)
    
    if not p_adic_orders or width == 0:
        return {
            "metric_name": "p-adic order correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "invalid_resolution_width"
        }
    
    mean_order = sum(p_adic_orders) / len(p_adic_orders)
    correlation_coefficient = (sum((x - mean_order) * (y - width) for x, y in zip(p_adic_orders, p_adic_orders)) /
                               (len(p_adic_orders) * math.sqrt(sum((x - mean_order) ** 2 for x in p_adic_orders)) *
                                math.sqrt(sum((y - width) ** 2 for y in p_adic_orders))))
    
    return {
        "metric_name": "p-adic order correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "unknown"
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={first_failing_seed}")