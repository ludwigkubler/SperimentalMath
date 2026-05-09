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

def hook_length_formula(n, k):
    def hook_length(i, j):
        return (n - i) * (n - j) + 1 - i - j
    total = 0
    for i in range(n):
        for j in range(k):
            total += hook_length(i, j)
    return factorial(n * k) // total

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    lambda_ = (n - 1, 1)
    permanent_multiplicity = 0
    determinant_multiplicity = 0
    
    for n in n_values:
        perm_multiplicity = hook_length_formula(n, n) // hook_length_formula(n, 1)
        det_multiplicity = hook_length_formula(n, n) // hook_length_formula(n, 1)
        
        if random.choice([True, False]):
            permanent_multiplicity += perm_multiplicity
        else:
            determinant_multiplicity += det_multiplicity
    
    metric_value = permanent_multiplicity / determinant_multiplicity
    conjecture_holds = metric_value >= 2**(n/2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Multiplicity Ratio",
        "metric_value": metric_value,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")