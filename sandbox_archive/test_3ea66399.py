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
    
    def generate_polynomial(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_minimal_local_index(poly):
        n = len(poly)
        if n == 0:
            return 0
        count = sum(poly)
        return abs(count - (n - count))
    
    def compute_communication_complexity(poly):
        n = len(poly)
        return sum(1 for i in range(n) if poly[i] != poly[(i + 1) % n])
    
    mli_values = []
    c_values = []
    instances_tested = 0
    n_max = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        poly = generate_polynomial(n)
        mli = compute_minimal_local_index(poly)
        c = compute_communication_complexity(poly)
        
        if mli is None or c is None:
            continue
        
        mli_values.append(mli)
        c_values.append(c)
        instances_tested += 1
        n_max = max(n_max, n)
    
    if not mli_values or not c_values:
        return {
            "metric_name": "mli_vs_c",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((x - mean_mli) * (y - mean_c) for x, y in zip(mli_values, c_values)) / (len(mli_values) * std_mli * std_c)
    
    return {
        "metric_name": "mli_vs_c",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.95,  # Arbitrary threshold for linear correlation
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_correlation = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_correlation = math.sqrt(sum((r["metric_value"] - mean_correlation) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")