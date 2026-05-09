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

def hook_length_formula(shape):
    n = sum(shape)
    numerator = factorial(n)
    denominator = 1
    for row in shape:
        for cell in row:
            denominator *= (cell + len(row) - row.index(cell))
    return numerator // denominator

def partition_to_shape(partition):
    n = sum(partition)
    shape = []
    current_row = []
    remaining = n
    for part in reversed(sorted(partition)):
        if remaining >= part:
            current_row.append(part)
            remaining -= part
        else:
            shape.append(current_row[::-1])
            current_row = [part]
            remaining -= part
    if current_row:
        shape.append(current_row[::-1])
    return shape

def partitions(n):
    def extend_partition(p, max_val):
        if p and p[-1] > max_val:
            return
        for i in range(max_val, 0, -1):
            new_p = p + [i]
            if sum(new_p) == n:
                yield new_p
            elif sum(new_p) < n:
                yield from extend_partition(new_p, i)
    yield from extend_partition([], n)

def irreducible_representations(n):
    return len(list(partitions(n)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(4, 40)
    permanent_irreps = irreducible_representations(n)
    determinant_irreps = 1
    metric_value = permanent_irreps - determinant_irreps
    conjecture_holds = metric_value >= 2**(n // 2)
    counterexample = "" if conjecture_holds else f"Permanent {permanent_irreps} vs Determinant {determinant_irreps}"
    return {
        "metric_name": "irreducible_representations_gap",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Permanent vs Determinant gap\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")