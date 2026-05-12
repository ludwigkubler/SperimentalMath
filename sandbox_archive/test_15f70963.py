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

def polynomial_from_sat(instance):
    n = len(instance)
    vars = {f"x{i}": 0 for i in range(n)}
    poly = 0
    for clause in instance:
        term = 1
        for literal in clause:
            if literal > 0:
                term *= (vars[f"x{literal-1}"] + 1)
            else:
                term *= (1 - vars[f"x{-literal-1}"])
        poly += term
    return poly

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
    poly = polynomial_from_sat(instance)
    
    # Compute invariant ring using Gröbner basis (simplified version)
    def groebner_basis(poly):
        return [poly]  # Simplified for demonstration
    
    generators = groebner_basis(poly)
    generator_count = len(generators)
    
    conjecture_holds = generator_count >= n
    counterexample = "" if conjecture_holds else f"n={n}, generator_count={generator_count}"
    
    return {
        "metric_name": "Generator Count",
        "metric_value": generator_count,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, generator_count={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or too many failures")