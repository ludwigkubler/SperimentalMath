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
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formulas(n, k):
    def hook_length(i, j):
        return (n - i) * (n - j) + 1 - i - j
    
    total = 0
    for partition in partitions(k, n):
        product = 1
        for part in partition:
            for i in range(part):
                for j in range(n - i):
                    product *= hook_length(i, j)
        total += factorial(k) // product
    return total

def partitions(k, n):
    if k == 0 or n == 0:
        yield []
        return
    for p in partitions(k-1, n):
        yield [p[0]+1] + p[1:]
    for p in partitions(k, n-1):
        yield [1] + p

def plethysm_coefficient(n, k):
    perm = hook_length_formulas(n, k)
    det = hook_length_formulas(n, k)
    return perm - det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    formula = [random.choice([1, 2]) for _ in range(3 * n)]
    clause_lengths = [formula.count(1), formula.count(2)]
    
    perm_coeff = plethysm_coefficient(n, n)
    det_coeff = plethysm_coefficient(n, n)
    
    gap = perm_coeff - det_coeff
    
    metric_value = gap
    conjecture_holds = gap >= 2 ** (n / 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "plethysm_gap",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")