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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(young_diagram):
    n = len(young_diagram)
    hook_lengths = []
    for row in range(n):
        for col in range(row + 1):
            hook_lengths.append((young_diagram[row][col] - col) * (n - row - young_diagram[row][col]))
    return math.prod(hook_lengths)

def perm_n_hook_length():
    n = 5
    hook_lengths = [i * (n - i) for i in range(n)]
    return math.prod(hook_lengths)

def det_m_hook_length(m):
    m = int(math.sqrt(m))
    if m == 0:
        return 1
    hook_lengths = [(m - col) * (m - row) for row in range(m) for col in range(row + 1)]
    return math.prod(hook_lengths)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    H_perm_n = perm_n_hook_length()
    H_det_m_values = []
    
    for n in n_values:
        if n < 5 or n > 40:
            continue
        H_det_m = det_m_hook_length(n)
        H_det_m_values.append(H_det_m)
        
        if H_det_m >= H_perm_n:
            return {
                "metric_name": "Hook-Length Ratio",
                "metric_value": H_det_m,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"det_{n}={H_det_m}, perm_5={H_perm_n}"
            }
    
    return {
        "metric_name": "Hook-Length Ratio",
        "metric_value": H_det_m_values,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if isinstance(r["metric_value"], list)]
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"det_m >= perm_5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")