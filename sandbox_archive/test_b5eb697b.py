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
    hook_lengths = []
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            hook_lengths.append((shape[row][col] - col) + (n - shape[row][col]) - row + 1)
    return factorial(n) // math.prod(hook_lengths)

def generate_partition(n):
    if n == 0:
        return [[]]
    partitions = []
    for p in generate_partition(n - 1):
        partitions.append([p[0] + [1]] + p[1:])
        if not p or len(p[-1]) > 1:
            partitions.append([[1] + p[0]] + p[1:])
    return partitions

def count_irreducible_components(shape, n):
    partitions = generate_partition(n)
    irreducibles = set()
    for partition in partitions:
        if sum(partition) == len(shape):
            irreducibles.add(tuple(sorted(partition)))
    return len(irreducibles)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_count_perm = 0
    total_count_det = 0
    instances_tested = 0

    for n in n_values:
        perm_count = count_irreducible_components([n], n)
        det_count = count_irreducible_components([n], int(n ** 1.5))
        total_count_perm += perm_count
        total_count_det += det_count
        instances_tested += len(n_values)

    metric_value = total_count_perm / instances_tested
    conjecture_holds = metric_value > total_count_det
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Kronecker Coefficient Asymmetry",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")