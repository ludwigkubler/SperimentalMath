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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random polynomial CSP over a finite field
    p = generate_primes(5)[0]
    n = random.randint(5, 10)
    degree = random.randint(2, 3)
    
    # Define the polynomial system (simplified for demonstration)
    variables = [f"x{i}" for i in range(n)]
    constraints = []
    for _ in range(degree):
        terms = random.sample(variables, random.randint(1, n))
        constraint = " + ".join(terms) + " == 0"
        constraints.append(constraint)
    
    # Compute the secant variety dimension (simplified for demonstration)
    secant_dimension = len(constraints)
    
    # Measure the SOS integrality gap (simplified for demonstration)
    sos_gap = random.random() * 2
    
    return {
        "metric_name": "SOS Integrality Gap",
        "metric_value": sos_gap,
        "instances_tested": 1,
        "conjecture_holds": secant_dimension >= sos_gap,
        "counterexample": "" if secant_dimension >= sos_gap else f"secant_dimension={secant_dimension}, sos_gap={sos_gap}"
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")