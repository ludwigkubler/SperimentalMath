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
    return abs(a * b) // gcd(a, b)

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
    rows, cols = len(shape), len(shape[0])
    total = 0
    for r in range(rows):
        for c in range(cols):
            total += shape[r][c] + 1 - r - c
    return binomial_coefficient(total, sum(sum(row) for row in shape))

def trivial_representation_multiplicity(n, k):
    # The multiplicity of the trivial representation in Sym^k(A) is given by the hook-length formula
    # applied to the partition (n-k, n-k, ..., n-k) repeated k times.
    shape = [[n - k] * k for _ in range(k)]
    return hook_length_formula(shape)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        permanent_multiplicity = trivial_representation_multiplicity(n, n)
        determinant_multiplicity = trivial_representation_multiplicity(n, n)
        
        if permanent_multiplicity < determinant_multiplicity:
            conjecture_holds = False
            counterexample = f"n={n}, perm_mult={permanent_multiplicity}, det_mult={determinant_multiplicity}"
            break
        
        total_metric_value += permanent_multiplicity / determinant_multiplicity
        instances_tested += 1

    return {
        "metric_name": "multiplicity_ratio",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")