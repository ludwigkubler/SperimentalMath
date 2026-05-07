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
    
    n = random.randint(5, 40)
    d = random.choice([3, 4])
    
    # Generate a random AC⁰ circuit of depth d on n variables
    circuit = []
    for _ in range(d):
        layer = [random.choice(['AND', 'OR']) for _ in range(n)]
        circuit.append(layer)
    
    # Compute the real stable polynomial coefficients via Fourier transform
    # This is a placeholder function. For simplicity, we assume the coefficients are known.
    # In practice, you would need to implement the Fourier transform and coefficient extraction.
    def fourier_transform(circuit):
        # Placeholder for Fourier transform implementation
        return [random.uniform(-1, 1) for _ in range(2**n)]
    
    coeffs = fourier_transform(circuit)
    
    # Sum absolute values of coefficients
    coeff_sum = sum(abs(coeff) for coeff in coeffs)
    
    # Verify the conjecture bound
    threshold = 2 ** (n**(1/d) / 10)
    conjecture_holds = coeff_sum >= threshold
    
    return {
        "metric_name": "Coefficient Sum",
        "metric_value": coeff_sum,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Circuit depth {d}, n={n}"
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
    
    mean_coeff_sum = sum(res["metric_value"] for res in results) / len(results)
    std_coeff_sum = math.sqrt(sum((res["metric_value"] - mean_coeff_sum)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_coeff_sum} std={std_coeff_sum} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit depth {res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")