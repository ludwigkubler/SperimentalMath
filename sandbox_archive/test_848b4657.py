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
        if k > n:
            return 0
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def braid_complexity(m, n):
        upper_bound = 2 ** (m + n) / factorial(n)
        lower_bound = 3 ** n
        return upper_bound, lower_bound
    
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for m in range(1, 6):
        for n in range(m + 1, min(n_max, 41)):
            upper_bound, lower_bound = braid_complexity(m, n)
            instances_tested += 1
            n_max = max(n_max, n)
            
            # Simulate a random CNF with m clauses and n variables
            cnf = []
            for _ in range(m):
                clause = [random.randint(1, n), random.randint(-n, -1)]
                cnf.append(clause)
            
            # Compute the minimal number of non-commuting generators (simplified)
            # This is a placeholder; replace with actual computation
            computed_value = len(cnf) * 2
            
            if not (lower_bound <= computed_value <= upper_bound):
                conjecture_holds = False
                counterexample = f"m={m}, n={n}: Computed {computed_value} outside bounds [{lower_bound}, {upper_bound}]"
    
    return {
        "metric_name": "Braid Monoid Complexity",
        "metric_value": computed_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")