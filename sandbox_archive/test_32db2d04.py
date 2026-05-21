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
    
    def generate_polynomial(n):
        return [random.randint(0, 100) for _ in range(n+1)]
    
    def sum_of_powers(poly, r, p):
        total = 0
        for coeff in poly:
            total += pow(coeff, r, p)
        return total % p
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = random.randint(2, 100)
    poly = generate_polynomial(n)
    
    for r in range(1, n+1):
        if sum_of_powers(poly, r, p) < 1 / (p ** r):
            return {
                "metric_name": "sum_of_powers",
                "metric_value": sum_of_powers(poly, r, p),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"r={r}, poly={poly}"
            }
    
    return {
        "metric_name": "sum_of_powers",
        "metric_value": sum_of_powers(poly, r, p),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    if conjecture_holds:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values):.4f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values)):.4f} support_fraction={support_fraction:.4f}")
    elif any(not r["conjecture_holds"] for r in results if "conjecture_holds" in r):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")