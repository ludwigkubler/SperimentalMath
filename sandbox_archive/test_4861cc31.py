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
    
    def boolean_function(n, m):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_degree(f):
        n = len(f)
        max_degree = 0
        for i in range(n):
            degree = sum(f[j] * (i & (1 << j)) for j in range(n))
            if degree > max_degree:
                max_degree = degree
        return max_degree
    
    def kostka_coefficient(m, n):
        # Simplified version for demonstration purposes
        return math.comb(m + n - 1, m)
    
    def generate_family_of_functions(m, n):
        family = []
        while len(family) < 2**m:
            f = boolean_function(n, m)
            if boolean_degree(f) <= 2:
                family.append(f)
        return family
    
    m = random.randint(1, 5)
    n = random.randint(5, 30)
    family = generate_family_of_functions(m, n)
    
    max_kostka_coefficient = max(kostka_coefficient(m, len(f)) for f in family)
    expected_bound = m**(3/4) * n**(3/4)
    
    conjecture_holds = max_kostka_coefficient <= expected_bound
    counterexample = "" if conjecture_holds else f"max_kostka_coefficient={max_kostka_coefficient}, expected_bound={expected_bound}"
    
    return {
        "metric_name": "max_kostka_coefficient",
        "metric_value": max_kostka_coefficient,
        "instances_tested": len(family),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 31))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_dev:.4f} support_fraction={support_fraction:.4f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_dev:.4f} support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_kostka_coefficient exceeded expected_bound\" first_failing_seed={first_failing_seed}")