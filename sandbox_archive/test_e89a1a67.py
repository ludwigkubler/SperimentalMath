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
    
    def characteristic_polynomial(cnf):
        n = len(cnf[0])
        poly = 1
        for clause in cnf:
            term = 1
            for var in range(n):
                if var + 1 not in clause and var - 1 not in clause:
                    return None  # Avoid division by zero
                if var + 1 in clause:
                    term *= (var + 1) / (var - 1)
                else:
                    term *= -(var + 1) / (var - 1)
            poly += term
        return poly
    
    def count_integral_points(poly):
        n = len(poly)
        count = 0
        for x in range(-10, 11):  # Limit search to a reasonable range
            if all((poly[i] + x**i) % (x - i) == 0 for i in range(n)):
                count += 1
        return count
    
    def upper_bound(m, n):
        return m**(1/4) * n**(3/2)
    
    results = []
    for _ in range(30):  # Test with 30 instances per seed
        m = random.randint(5, 40)
        n = random.randint(5, 40)
        cnf = [[random.randint(1, n) for _ in range(random.randint(1, m))] for _ in range(m)]
        poly = characteristic_polynomial(cnf)
        if poly is None:
            continue
        integral_points = count_integral_points(poly)
        upper_bound_value = upper_bound(m, n)
        results.append({
            "m": m,
            "n": n,
            "integral_points": integral_points,
            "upper_bound": upper_bound_value,
            "conjecture_holds": integral_points <= upper_bound_value
        })
    
    if not results:
        return {
            "metric_name": "Integral Points",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid CNF found"
        }
    
    metric_values = [result["integral_points"] for result in results]
    conjecture_holds_all = all(result["conjecture_holds"] for result in results)
    counterexample = next((f"m={result['m']}, n={result['n']}" for result in results if not result["conjecture_holds"]), "")
    
    return {
        "metric_name": "Integral Points",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds_all,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    results = [run_trial(seed) for seed in seeds]
    metric_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
    conjecture_holds_all = all(result["conjecture_holds"] for result in results)
    
    if conjecture_holds_all:
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m={result['m']}, n={result['n']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_CNFs_found")