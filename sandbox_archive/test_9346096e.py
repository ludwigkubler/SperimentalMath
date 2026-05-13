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

def hook_length_formula(n):
    if n == 0:
        return 1
    product = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            product *= (i + j)
            product //= j
    return product

def plethysm_coefficient(n, k):
    if k == 0:
        return 1
    coeff = 0
    for i in range(k + 1):
        coeff += math.comb(k, i) * hook_length_formula(i) ** (n - k + i)
    return coeff

def permanent_like_polynomial(n):
    return sum(plethysm_coefficient(n, k) * x**k for k in range(n + 1))

def determinant_like_polynomial(m):
    return sum(plethysm_coefficient(m, k) * y**k for k in range(m + 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = math.isqrt(n ** 1.5) - 1
    perm_poly = permanent_like_polynomial(n)
    det_poly = determinant_like_polynomial(m)
    P_perm = sum(plethysm_coefficient(n, k) for k in range(n + 1))
    P_det = sum(plethysm_coefficient(m, k) for k in range(m + 1))
    
    result = {
        "metric_name": "Plethysm Coefficient Sum",
        "metric_value": P_perm - P_det,
        "instances_tested": 1,
        "conjecture_holds": P_perm > P_det,
        "counterexample": ""
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")
        results.append(run_trial(seed))
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"P(perm_n) <= P(det_m)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")