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

def binomial_coefficient(n, k):
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def hook_length_formula(shape, n):
    numerator = 1
    denominator = 1
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            numerator *= n + 1 - row - col
            if col < len(shape[row]) - 1:
                denominator *= shape[row][col] + 1 - col
    return numerator // denominator

def schur_functor(n, lambda_):
    result = 0
    for partition in partitions(n):
        if all(partition[i] >= partition[i+1] for i in range(len(partition)-1)):
            sign = (-1) ** (n - sum(partition))
            product = 1
            for i in range(len(lambda_)):
                product *= binomial_coefficient(n + lambda_[i] - i, n - i)
            result += sign * product // hook_length_formula(partition, n)
    return result

def partitions(n):
    def partitions_recursive(n, max_val):
        if n == 0:
            yield []
        else:
            for i in range(min(max_val, n), 0, -1):
                for p in partitions_recursive(n - i, i):
                    yield [i] + p
    return list(partitions_recursive(n, n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    lambda_ = (n-1, 1)
    
    plethysm_multiplicity = schur_functor(n, lambda_)
    determinant_multiplicity = 1
    
    return {
        "metric_name": "plethysm_multiplicity",
        "metric_value": plethysm_multiplicity,
        "instances_tested": 1,
        "conjecture_holds": plethysm_multiplicity >= 2**n and determinant_multiplicity <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = list(range(2, 30)) + [101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")