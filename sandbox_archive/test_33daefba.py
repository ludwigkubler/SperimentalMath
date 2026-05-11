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
    else:
        return n * factorial(n - 1)

def hook_length_formula(n, k):
    numerator = factorial(n + k)
    denominator = (factorial(k) ** 2) * factorial(n - k)
    return numerator // denominator

def plethysm_coefficient(n, k):
    return hook_length_formula(n, k) / hook_length_formula(n, 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = math.ceil(n ** 1.5)
    
    permanent_coeff = plethysm_coefficient(n, k)
    determinant_coeff = plethysm_coefficient(n, 1)
    
    gap = permanent_coeff - determinant_coeff
    expected_gap = n ** 1.5
    
    conjecture_holds = gap >= expected_gap
    counterexample = "" if conjecture_holds else f"Gap {gap} < {expected_gap}"
    
    return {
        "metric_name": "plethysm_coefficient_gap",
        "metric_value": gap,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gap = sum(r["metric_value"] for r in results) / len(results)
    std_gap = math.sqrt(sum((r["metric_value"] - mean_gap) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gap} std={std_gap} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Gap too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")