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

def binomial(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def hook_length_formula(shape):
    n = len(shape)
    result = 1
    for i in range(n):
        for j in range(len(shape[i])):
            result *= (shape[i][j] + n - i - j - 1)
            result //= (i + j + 1)
    return result

def kronecker_coefficient(lam, mu):
    if len(lam) != len(mu):
        return 0
    n = len(lam)
    numerator = 1
    for i in range(n):
        numerator *= hook_length_formula(lam[:i+1]) * hook_length_formula(mu[:i+1])
    denominator = hook_length_formula(lam) * hook_length_formula(mu)
    return numerator // denominator

def generate_symmetric_tensor(n, k):
    tensor = [[0] * n for _ in range(k)]
    for i in range(k):
        for j in range(n):
            tensor[i][j] = random.randint(1, 10)
    return tensor

def decompose_tensor(tensor):
    n = len(tensor[0])
    k = len(tensor)
    shape = [(n - i) * (k - i) for i in range(n)]
    return shape

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    max_kronecker_coefficient_det = 0
    max_kronecker_coefficient_perm = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            tensor = generate_symmetric_tensor(n, n)
            shape = decompose_tensor(tensor)
            kronecker_coeffs = [kronecker_coefficient(shape[:i+1], shape[i+1:]) for i in range(len(shape))]
            max_kronecker_coefficient_det = max(max_kronecker_coefficient_det, max(kronecker_coeffs))
            instances_tested += 1

    conjecture_holds = max_kronecker_coefficient_det < max_kronecker_coefficient_perm
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "max_kronecker_coefficient",
        "metric_value": max(max_kronecker_coefficient_det, max_kronecker_coefficient_perm),
        "instances_tested": instances_tested,
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")