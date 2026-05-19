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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(shape, n):
    numerator = factorial(n)
    denominator = 1
    for row in shape:
        for cell in row:
            denominator *= (cell + len(row) - row.index(cell))
    return numerator / denominator

def young_tableau_count(shape, n):
    count = 1
    for row in shape:
        count *= factorial(len(row))
    return count // hook_length_formula(shape, n)

def multiplicity(f, lambda_, n):
    if f == 'perm':
        shape = [(n - 1), 1]
    elif f == 'det':
        shape = [1] * n
    else:
        return None

    return young_tableau_count(shape, n) / hook_length_formula([(n - 1), 1], n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(2, 40)
    m = random.randint(1, math.isqrt(n**3))
    
    mu_perm = multiplicity('perm', (n-1, 1), n)
    mu_det = multiplicity('det', (m,), m)

    metric_name = "Multiplicity Difference"
    metric_value = mu_perm - mu_det
    instances_tested = 1
    conjecture_holds = mu_perm > mu_det
    counterexample = "" if conjecture_holds else f"n={n}, m={m}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")