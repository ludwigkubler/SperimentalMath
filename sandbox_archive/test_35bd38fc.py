# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
import math

def max_plus_polynomial(degree, coefficients):
    return [coefficients[i] + i for i in range(degree)]

def evaluate_poly(poly, x):
    result = 0
    for coeff in poly:
        result = max(result, coeff + x)
    return result

def min_root_separation(poly):
    roots = []
    degree = len(poly) - 1
    if degree == 0:
        return float('inf')
    
    # Use a simple root-finding method (e.g., bisection)
    low, high = -100, 100
    while low < high:
        mid = (low + high) / 2
        value = evaluate_poly(poly, mid)
        if value == degree * mid:
            roots.append(mid)
            break
        elif value > degree * mid:
            high = mid
        else:
            low = mid
    
    return min(abs(r1 - r2) for r1, r2 in itertools.combinations(roots, 2)) if roots else float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    degree = n
    coefficients = [random.randint(-10, 10) for _ in range(degree + 1)]
    poly = max_plus_polynomial(degree, coefficients)
    
    min_separation = min_root_separation(poly)
    if min_separation == float('inf'):
        return {
            "metric_name": "min_root_separation",
            "metric_value": min_separation,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No distinct roots found"
        }
    
    # Placeholder for AC0 circuit complexity calculation
    # This is a stub and should be replaced with actual implementation
    circuit_size = degree ** 2
    
    return {
        "metric_name": "min_root_separation",
        "metric_value": min_separation,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "AC0 circuit complexity calculation not implemented"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"AC0 circuit complexity calculation not implemented\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")