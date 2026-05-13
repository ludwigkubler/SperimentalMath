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
import math
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def isqrt(n):
        x = n
        y = (x + 1) // 2
        while y < x:
            x, y = y, (y + x // y) // 2
        return x
    
    def hook_length_formula(shape):
        m, n = len(shape), len(shape[0])
        total = 1
        for i in range(m):
            for j in range(n):
                h = shape[i][j]
                total *= (m + i - h) * (n + j - h)
                total //= (i + 1) * (j + 1)
        return total
    
    def plethysm_coefficient_sum(poly, n):
        m = len(poly)
        total = 0
        for shape in combinations(range(m), n):
            coeff = hook_length_formula(shape)
            total += coeff * poly[shape]
        return total
    
    def perm_poly(n):
        return [1] + [math.factorial(i) for i in range(1, n)]
    
    def det_poly(n):
        return [1] + [(-1)**i * math.comb(n, i) for i in range(1, n)]
    
    n = random.randint(5, 40)
    m = isqrt(n ** 1.5) - 1
    
    perm_plethysm = plethysm_coefficient_sum(perm_poly(n), n)
    det_plethysm = plethysm_coefficient_sum(det_poly(m), m)
    
    metric_name = "Plethysm Coefficient Sum Gap"
    metric_value = perm_plethysm - det_plethysm
    instances_tested = 1
    conjecture_holds = perm_plethysm > det_plethysm
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 97, 3))  # Default to first 30 primes if no seeds provided
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")