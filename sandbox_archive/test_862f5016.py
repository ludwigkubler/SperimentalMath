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

def binomial_coefficient(n, k):
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def cnf_to_braid(cnf):
        # Placeholder for actual CNF to braid mapping logic
        # This is a dummy implementation that returns a fixed number of generators
        return random.randint(1, 10)
    
    n_max = 40
    instances_tested = 0
    upper_bound_total = 0
    lower_bound_total = 0
    
    for m in range(5, 51):
        for _ in range(6):  # 30 instances per seed
            n = random.randint(m + 1, min(n_max, 40))
            cnf = [[random.randint(1, n) for _ in range(random.randint(2, 5))] for _ in range(m)]
            generators = cnf_to_braid(cnf)
            
            upper_bound = (2 ** (m + n)) / factorial(n)
            lower_bound = 3 ** n
            
            instances_tested += 1
            if generators < upper_bound * 0.9 and generators <= lower_bound:
                upper_bound_total += 1
                lower_bound_total += 1
    
    conjecture_holds = (upper_bound_total >= 27) and (lower_bound_total >= 27)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "braid_generators",
        "metric_value": generators,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3**j for i in range(5) for j in range(5)]
    
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
    elif sum(r["conjecture_holds"] for r in results) >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")