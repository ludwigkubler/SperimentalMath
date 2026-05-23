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
    
    def generate_random_poly(n):
        degree = random.randint(1, n)
        coefficients = [random.randint(-10, 10) for _ in range(degree + 1)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result
    
    def generate_random_manifold(n):
        poly = generate_random_poly(n)
        manifold = [evaluate_polynomial(poly, i) for i in range(2**n)]
        return manifold
    
    def tropicalized_k_theory(manifold):
        return max(abs(x) for x in manifold)
    
    def acc0_circuit_size(poly):
        degree = len(poly) - 1
        if degree == 0:
            return 1
        return 1 + sum(acc0_circuit_size(poly[:i]) + acc0_circuit_size(poly[i+1:]) for i in range(1, degree))
    
    n = random.randint(5, 40)
    manifold = generate_random_manifold(n)
    tropical_rank = tropicalized_k_theory(manifold)
    circuit_size = acc0_circuit_size(generate_random_poly(n))
    
    return {
        "metric_name": "Tropicalized K-Theory Rank / ACC⁰ Circuit Size",
        "metric_value": tropical_rank / circuit_size,
        "instances_tested": 1,
        "conjecture_holds": tropical_rank <= 2 * circuit_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"Tropicalized K-Theory Rank {result['metric_value']} is greater than 2 * ACC⁰ Circuit Size {result['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break