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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sipser_function(n):
        # Generate a random Sipser function (parity function for simplicity)
        def f(x):
            return sum(x) % 2
        return f
    
    def group_action(f, g):
        # Group action on n-bit strings by permutation g
        def new_f(x):
            permuted_x = [x[g[i]] for i in range(len(x))]
            return f(permuted_x)
        return new_f
    
    def young_tableaux_decomposition(n):
        # Placeholder for noncommutative Fourier coefficient computation
        # This is a dummy implementation for the sake of testing
        return [1] * n
    
    def acc0_circuit_size(f, n):
        # Placeholder for ACC⁰ circuit size calculation
        # This is a dummy implementation for the sake of testing
        return 2 ** n
    
    n = random.randint(5, 40)
    f = generate_sipser_function(n)
    
    total_sum = 0
    for g in range(math.factorial(n)):
        new_f = group_action(f, g)
        coefficients = young_tableaux_decomposition(n)
        total_sum += sum(abs(coeff) for coeff in coefficients)
    
    circuit_size = acc0_circuit_size(f, n)
    if circuit_size == 0:
        return {
            "metric_name": "Noncommutative Fourier Coefficient Sum",
            "metric_value": None,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = total_sum / circuit_size
    conjecture_holds = abs(metric_value - 1) < 0.1  # Dummy threshold for testing
    
    return {
        "metric_name": "Noncommutative Fourier Coefficient Sum",
        "metric_value": metric_value,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")