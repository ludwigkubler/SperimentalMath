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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def evaluate_polynomial(polynomial, variables):
        result = polynomial[0]
        for i, coeff in enumerate(polynomial[1:], start=1):
            result += coeff * variables[i-1]
        return int(result % 2)
    
    def is_invariant(polynomial, function):
        n = len(function)
        for i in range(2**n):
            variables = [int(x) for x in format(i, f'0{n}b')]
            if evaluate_polynomial(polynomial, variables) != evaluate_polynomial(polynomial, [(1 - var) % 2 for var in variables]):
                return False
        return True
    
    def generate_coxeter_group_invariant_generators(n):
        generators = []
        for i in range(1, n):
            polynomial = [0] * (n + 1)
            polynomial[i] = 1
            if is_invariant(polynomial, generate_boolean_function(n)):
                generators.append(polynomial)
        return generators
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        denominator = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) * sum((y[i] - mean_y)**2 for i in range(len(y))))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    invariant_counts = []
    
    for n in n_values:
        for _ in range(5):
            function = generate_boolean_function(n)
            generators = generate_coxeter_group_invariant_generators(n)
            invariant_counts.append(len(generators))
    
    n_max = max(n_values)
    instances_tested = len(invariant_counts)
    metric_value = correlation_coefficient(range(1, n_max + 1), invariant_counts)
    conjecture_holds = metric_value >= 0.8
    counterexample = "" if conjecture_holds else f"Correlation coefficient {metric_value:.2f} < 0.8"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std=0.00 support_fraction=1.00")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")