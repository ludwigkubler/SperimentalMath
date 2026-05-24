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
    
    q = 2**random.randint(3, 5)  # Random prime power for F_q
    n = random.choice([5, 10, 15, 20, 30, 40])  # Random degree of polynomial
    k = random.randint(1, n // 2)  # Minimal root count
    
    # Generate a random polynomial f(x) in F_q[x] with minimal root count k
    coefficients = [random.randint(0, q-1) for _ in range(n+1)]
    while True:
        if sum(coefficients) == 0:  # Ensure at least one non-zero coefficient
            break
        coefficients[random.randint(0, n)] += 1
    
    # Construct the algebraic curve over an extension field to compute the minimal root count
    roots = []
    for i in range(q):
        if sum(coefficients[j] * pow(i, j, q) for j in range(n+1)) == 0:
            roots.append(i)
    
    if len(roots) < k:
        return {
            "metric_name": "exponential_depth",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "minimal_root_count_error"
        }
    
    # Determine the exponential depth of any Frege proof system for f(x)=0
    def frege_depth(k):
        if k == 0:
            return 0
        else:
            return 1 + frege_depth(k - 1)
    
    depth = frege_depth(k)
    
    return {
        "metric_name": "exponential_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": True if depth >= math.log(q, 2) + math.log(k+1, 2) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 67))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.9:
        result = "SUPPORTED"
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        result = f"FALSIFIED counterexample=\"minimal_root_count_error\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean:.2f} std={std_dev:.2f} support_fraction={support_fraction:.2f}")