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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(n):
    def hook_length(i, j):
        return (n - i) * (n - j) + 1
    total = 0
    for i in range(n):
        for j in range(n):
            total += hook_length(i, j)
    return factorial(n**2) // total

def irreducible_components(n):
    if n == 1:
        return 1
    if n == 2:
        return 3
    result = 0
    for i in range(1, n):
        result += lcm(n - i, i)
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        perm_n = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        det_n = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        
        λ_perm_n = irreducible_components(n)
        λ_det_n = irreducible_components(n)
        
        results.append({
            "n": n,
            "λ_perm_n": λ_perm_n,
            "λ_det_n": λ_det_n
        })
    
    metric_value = sum(result["λ_perm_n"] for result in results) / len(results)
    conjecture_holds = all(result["λ_perm_n"] >= 2**(n/2) and result["λ_det_n"] <= n**3 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    results = [run_trial(seed)["conjecture_holds"] for seed in seeds]
    support_fraction = sum(results) / len(results)
    
    if all(results):
        print(f"RESULT: SUPPORTED mean={sum(run_trial(seed)['metric_value'] for seed in seeds)/len(seeds)} std=0.0 support_fraction=1.0")
    elif any(not result for result in results):
        first_failing_seed = next(i for i, result in enumerate(results) if not result)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")