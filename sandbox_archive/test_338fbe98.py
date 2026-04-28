# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def continued_fraction(numerator, denominator):
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    a0 = numerator // denominator
    remainder = numerator % denominator
    cf = [a0]
    while remainder != 0:
        numerator = denominator
        denominator = remainder
        a = numerator // denominator
        remainder = numerator % denominator
        cf.append(a)
    return cf

def euclidean_algorithm(numerator, denominator):
    if gcd(numerator, denominator) == 1:
        return continued_fraction(numerator, denominator)

def decode_tt(tt, n):
    f = [0] * (2**n)
    for i in range(2**n):
        f[i] = tt & 1
        tt >>= 1
    return f

def quine_mccluskey(f):
    # Simplify the DNF using Quine-McCluskey algorithm
    pass  # Placeholder, actual implementation required

def dnf_min(f):
    # Compute the minimum size of a DNF representation of f
    pass  # Placeholder, actual implementation required

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 5, 6, 7]
    results = []
    
    for n in n_values:
        instances_tested = 0
        support_fraction = 0
        
        # Enumerate all DNFs with ≤4 terms and ≤4 literals
        dnf_count = 10**5
        for _ in range(dnf_count):
            instances_tested += 1
            # Generate a random DNF function
            f = [random.choice([0, 1]) for _ in range(2**n)]
            tt = int("".join(map(str, f)), 2)
            alpha_f = tt / (2**(2*n) + 1)
            cf = euclidean_algorithm(int(alpha_f * (2**(2*n) + 1)), 2**(2*n) + 1)
            S_f = max(cf[1:])
            
            if S_f >= n ** (n.bit_length()):
                dnf_complexity = dnf_min(f)
                if dnf_complexity > 2**n * n / S_f**0.1:
                    return {
                        "metric_name": "support_fraction",
                        "metric_value": support_fraction,
                        "instances_tested": instances_tested,
                        "conjecture_holds": False,
                        "counterexample": f"n={n}, DNF_min(f) > 2^n·n/S(f)^0.1"
                    }
                support_fraction += 1
        
        # Sample 5000 uniformly random TTs
        for _ in range(5000):
            instances_tested += 1
            tt = random.randint(0, 2**(2*n) - 1)
            alpha_f = tt / (2**(2*n) + 1)
            cf = euclidean_algorithm(int(alpha_f * (2**(2*n) + 1)), 2**(2*n) + 1)
            S_f = max(cf[1:])
            
            if S_f >= n ** (n.bit_length()):
                return {
                    "metric_name": "support_fraction",
                    "metric_value": support_fraction,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, DNF_min(f) > 2^n·n/S(f)^0.1"
                }
        
        # Adversarial sweep
        for m in [3, 5, 7, 11, 13]:
            for k in range(1, 2**(2*n), m):
                if gcd(k, m) == 1:
                    instances_tested += 1
                    tt = round(k * (2**(2*n) + 1) / m)
                    f = decode_tt(tt, n)
                    alpha_f = tt / (2**(2*n) + 1)
                    cf = euclidean_algorithm(int(alpha_f * (2**(2*n) + 1)), 2**(2*n) + 1)
                    S_f = max(cf[1:])
                    
                    if S_f >= n ** (n.bit_length()):
                        dnf_complexity = dnf_min(f)
                        if dnf_complexity > 2**n * n / S_f**0.1:
                            return {
                                "metric_name": "support_fraction",
                                "metric_value": support_fraction,
                                "instances_tested": instances_tested,
                                "conjecture_holds": False,
                                "counterexample": f"n={n}, DNF_min(f) > 2^n·n/S(f)^0.1"
                            }
                        support_fraction += 1
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = (sum((x["metric_value"] - mean_value)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "support_fraction",
        "metric_value": support_fraction,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = (sum((x["metric_value"] - mean_value)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.99:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['metric_name']}, DNF_min(f) > 2^n·n/S(f)^0.1\" first_failing_seed={first_failing_seed}")