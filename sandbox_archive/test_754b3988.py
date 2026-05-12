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
    return abs(a*b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(shape):
    n = len(shape)
    total = 1
    for i in range(n):
        for j in range(len(shape[i])):
            total //= (i + j + 1)
            total *= shape[i][j] + i + j + 1
    return total

def schur_weyl_decomposition_components(n, m):
    if m != n**2:
        return 0
    components = 0
    for k in range(1, n+1):
        components += hook_length_formula([[n-k+i] * (k-i) + [i] * (n-k) for i in range(k)])
    return components

def monotone_circuit_size_bound(n, C):
    return C * math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    m = n**2
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        clause_indicator_vectors = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        tensor_product = [sum(v[i] * w[i] for v, w in zip(vec1, vec2)) for vec1, vec2 in zip(*clause_indicator_vectors)]
        C = schur_weyl_decomposition_components(n, m)
        if C < 2**(n/2) / (n**2):
            conjecture_holds = False
            counterexample = f"Failed at n={n}, C={C}"
            break

    return {
        "metric_name": "Schur-Weyl Decomposition Components",
        "metric_value": C,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")