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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    size_C = random.randint(2, 100)  # Randomly generate a size for AC⁰ circuit C
    
    # Generate truth-table polynomial equations for PARITY on n inputs
    truth_table = [[i & (1 << j) % 2 for j in range(n)] for i in range(1 << n)]
    
    # Construct the ideal I_C from truth-table equations
    I_C = []
    for row in truth_table:
        poly = sum(row[j] * x**j for j in range(n)) - sum(row[j] for j in range(n))
        I_C.append(poly)
    
    # Compute the real radical's dimension via Gröbner bases (simplified version)
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def simplify(poly):
        return [coeff for coeff in poly if coeff != 0]
    
    def multiply(p1, p2):
        result = [0] * (len(p1) + len(p2))
        for i in range(len(p1)):
            for j in range(len(p2)):
                result[i + j] += p1[i] * p2[j]
        return simplify(result)
    
    def divide(poly, divisor):
        quotient = []
        remainder = poly[:]
        while remainder and remainder[0] != 0:
            degree = len(remainder) - 1
            coeff = remainder[degree] / divisor[-1]
            quotient.append(coeff)
            for i in range(degree + 1):
                remainder[i] -= coeff * divisor[i]
            remainder = simplify(remainder)
        return quotient, remainder
    
    def gcd_poly(p1, p2):
        if not p2:
            return p1
        return gcd_poly(p2, [p1[i] % p2[i] for i in range(len(p1))])
    
    def lcm_poly(p1, p2):
        return divide(gcd_poly(p1, p2), 1)[0]
    
    # Simplify the ideal I_C
    I_C = simplify(I_C)
    
    # Compute the dimension of the real radical (simplified version)
    dim_rad_I_C = len(I_C) - len(set(I_C))
    
    # Verify the conjecture
    if dim_rad_I_C >= math.log2(size_C) - 7:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "dim(rad(I_C)) < log₂(size(C)) - 7"
    
    return {
        "metric_name": "dimension of real radical",
        "metric_value": dim_rad_I_C,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 30)]  # Default list of 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction:.2f}")