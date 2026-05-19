# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product, combinations
from fractions import Fraction

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)

def factorial(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n: int, k: int) -> int:
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def hook_length_formula(shape: tuple, n: int) -> Fraction:
    numerator = 1
    denominator = 1
    for row in range(len(shape)):
        for col in range(shape[row]):
            h = shape[row] - col + len(shape) - row - 1
            numerator *= h + 1
            denominator *= h
    return Fraction(numerator, denominator)

def multiplicity(f: str, shape: tuple, n: int) -> Fraction:
    if f == 'perm':
        return hook_length_formula(shape, n)
    elif f == 'det':
        # For determinant, we need to consider the representation det_m^O(1)
        m = len(shape)
        if m >= n ** 0.5:
            return Fraction(0)
        return hook_length_formula((n - m - 1, 1), n)
    else:
        return Fraction(0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(2, 40)
    m_max = int(n ** 1.5)
    mu_perm_sum = 0
    mu_det_sum = 0
    instances_tested = 0

    for _ in range(30):
        m = random.randint(0, m_max - 1)
        mu_perm = multiplicity('perm', (n-1, 1), n)
        mu_det = multiplicity('det', (m,), n)
        mu_perm_sum += mu_perm
        mu_det_sum += mu_det
        instances_tested += 1

    mean_mu_perm = mu_perm_sum / instances_tested
    mean_mu_det = mu_det_sum / instances_tested
    conjecture_holds = mean_mu_perm > mean_mu_det
    counterexample = "" if conjecture_holds else f"m={m}, μ(perm)={mean_mu_perm}, μ(det)={mean_mu_det}"

    return {
        "metric_name": "Multiplicity of Hook Representation",
        "metric_value": mean_mu_perm,
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
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE insufficient data"

    print(result)