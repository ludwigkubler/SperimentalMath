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
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def murnaghan_nakayama(lam, beta):
    if not lam:
        return 1
    a = len(lam)
    b = sum(lam)
    result = 0
    for i in range(a):
        term = math.pow(-1, i) * binomial_coefficient(b - 1, lam[i] - 1) * murnaghan_nakayama(lam[:i] + lam[i+1:], beta)
        if i == 0:
            result += term
        else:
            result -= term
    return result

def irreducible_character(lam, sigma):
    n = len(lam)
    result = 1
    for i in range(n):
        result *= murnaghan_nakayama(lam[:i] + lam[i+1:], sigma[i])
    return result

def specht_coefficient(f, lam):
    n = len(lam)
    alpha = 0
    for sigma in itertools.permutations(range(n)):
        alpha += f(sigma) * irreducible_character(lam, sigma)
    return alpha / factorial(n)

def effective_specht_support(f, lam):
    n = len(lam)
    dim_V_lam = sum(binomial_coefficient(n, i) ** 2 for i in lam)
    numerator = sum(dim_V_lam * specht_coefficient(f, lam) ** 2 for lam in partitions(n))
    denominator = sum(dim_V_lam * specht_coefficient(f, lam) ** 4 for lam in partitions(n))
    return (numerator / denominator) ** 0.5

def generate_random_formula(n, s):
    if s == 1:
        leaves = [(random.sample(range(n), n // 2), random.sample(range(n), n // 2), lambda x: 1)]
    else:
        left = generate_random_formula(n, s // 2)
        right = generate_random_formula(n, s - s // 2)
        leaves = []
        for l in left:
            for r in right:
                leaves.append((l[0] + r[0], l[1] + r[1], lambda x: l[2](x) * r[2](x)))
    return leaves

def partitions(n):
    def partitions_recursive(n, k):
        if n == 0:
            yield []
        elif k == 0:
            yield [n]
        else:
            for i in range(min(k, n), -1, -1):
                for p in partitions_recursive(n - i, i):
                    yield [i] + p
    return partitions_recursive(n, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in {4, 5, 6, 7}:
        for s in {1, 2, 4, 8, 16, 32}:
            if len(results) >= 720:
                break
            f = generate_random_formula(n, s)
            lam = [n]
            r = effective_specht_support(f, lam)
            results.append({"metric_name": "effective_specht_support", "metric_value": r, "instances_tested": 1, "conjecture_holds": r <= s, "counterexample": "" if r <= s else f"Formula with |supp_eff| > {s}"})
    
    mean_r = sum(result["metric_value"] for result in results) / len(results)
    max_r = max(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_r": mean_r,
        "max_r": max_r,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 30
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["mean_r"] for r in results) / len(results)
    max_r = max(r["max_r"] for r in results)
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / len(results)
    
    if all(r["support_fraction"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=NA support_fraction={support_fraction}")
    elif any(r["max_r"] > 1.05 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["max_r"] > 1.05)
        print(f"RESULT: FALSIFIED counterexample=\"|supp_eff| > s\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")