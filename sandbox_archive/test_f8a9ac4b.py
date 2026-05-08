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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def evaluate_boolean_function(f, x):
    n = int(math.log2(len(f)))
    result = f[0]
    for i in range(1, len(x)):
        if x[i] == 1:
            result ^= f[i]
    return result

def fourier_coefficient_magnitude(n, f):
    sum_abs_coeffs = 0
    for x in range(2**n):
        sum_abs_coeffs += abs(evaluate_boolean_function(f, [int(b) for b in bin(x)[2:].zfill(n)]))
    return sum_abs_coeffs / (2**n)

def circuit_complexity(f):
    n = int(math.log2(len(f)))
    # Simplistic estimate based on the number of terms
    return len(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        avg_coeff_magnitude = fourier_coefficient_magnitude(n, f)
        if avg_coeff_magnitude < 1 / math.sqrt(n):
            circuit_comp = circuit_complexity(f)
            if circuit_comp > 2**n:  # Simplistic criterion for hardness
                results.append((n, True))
            else:
                results.append((n, False))
        else:
            results.append((n, False))
    
    avg_metric_value = sum(result[1] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result[1] for result in results)
    counterexample = "" if conjecture_holds else "circuit_complexity_not_exponential"
    
    return {
        "metric_name": "average_fourier_coeff_magnitude",
        "metric_value": avg_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 3 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"circuit_complexity_not_exponential\" first_failing_seed={first_failing_seed}")