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

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def hook_length_formula(shape):
    n = len(shape)
    total = 0
    for row in range(n):
        for col in range(len(shape[row])):
            total += shape[row][col] + 1 - row - col
    return binomial_coefficient(total, n)

def generate_irreducible_components(n):
    if n == 2:
        return [1]
    components = []
    for i in range(1, n):
        components.extend(generate_irreducible_components(i))
    components.append(n)
    return components

def count_irreducible_representations(shape):
    components = generate_irreducible_components(len(shape))
    return len(components)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(4, 40)
    permanent_shape = [[n - i - j for j in range(i + 1)] for i in range(n)]
    determinant_shape = [[1] * (i + 1) for i in range(n)]
    
    permanent_components = count_irreducible_representations(permanent_shape)
    determinant_components = count_irreducible_representations(determinant_shape)
    
    metric_name = "irreducible_components"
    metric_value = permanent_components - determinant_components
    instances_tested = 1
    conjecture_holds = metric_value >= 2**(n // 2)
    counterexample = "" if conjecture_holds else f"Permanent: {permanent_components}, Determinant: {determinant_components}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 100))[:30]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Permanent exceeds determinant by less than 2^{n // 2}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")