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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def p_adic_expansion(x, p, n):
    expansion = []
    while len(expansion) < n and x > 0:
        expansion.append(x % p)
        x //= p
    return expansion[::-1]

def minimal_rank(p_adic_coeffs):
    rank = 0
    for coeff in p_adic_coeffs:
        if coeff != 0:
            rank += 1
    return rank

def generate_bp(n):
    bp = []
    for i in range(2 * n - 1):
        bp.append(random.choice([0, 1]))
    return bp

def construct_p_adic_series(bp, p):
    coeffs = [0] * (len(bp) + 1)
    for i in range(len(bp)):
        if bp[i] == 1:
            coeffs[i // 2] += 1
    return coeffs

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 3  # Prime number for p-adic expansion
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_bp(n)
        coeffs = construct_p_adic_series(bp, p)
        rank = minimal_rank(coeffs)
        expected_rank = n * math.log(n)
        
        if rank > expected_rank or rank < 0.5 * expected_rank:
            return {
                "metric_name": "min_rank",
                "metric_value": rank,
                "instances_tested": len(bp),
                "conjecture_holds": False,
                "counterexample": f"BP size {n} with rank {rank}"
            }
    
    return {
        "metric_name": "min_rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_rank = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.5 * n_values[-1] * math.log(n_values[-1])) / len(results)
    
    if all(r >= 0.5 * n_values[-1] * math.log(n_values[-1]) for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(r < 0.5 * n_values[-1] * math.log(n_values[-1]) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.5 * n_values[-1] * math.log(n_values[-1]))
        print(f"RESULT: FALSIFIED counterexample=\"rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")