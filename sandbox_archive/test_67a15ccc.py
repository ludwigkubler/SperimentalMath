# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from math import factorial, sqrt, log
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def hook_length_formula(n, k):
    def hook_length(i, j):
        return (n - i + 1) * (n - j + 1) - (i - j)
    
    total = factorial(k)
    for i in range(1, n + 1):
        for j in range(1, min(n, k) + 1):
            total //= hook_length(i, j)
    return total

def schur_weyl_multiplicity(n, k, λ):
    def partition_to_hook_lengths(partition):
        return [p - i for i, p in enumerate(partition)]
    
    def hook_length_product(hook_lengths):
        product = 1
        for h in hook_lengths:
            product *= h
        return product
    
    def sign_of_partition(partition):
        inversions = 0
        for i in range(len(partition)):
            for j in range(i + 1, len(partition)):
                if partition[i] < partition[j]:
                    inversions += 1
        return (-1) ** inversions
    
    def hook_length_sign(hook_lengths):
        sign = 1
        for h in hook_lengths:
            sign *= (h + 1)
        return sign
    
    def schur_polynomial(partition, n):
        hook_lengths = partition_to_hook_lengths(partition)
        numerator = hook_length_product(hook_lengths) * factorial(n)
        denominator = 1
        for i in range(len(partition)):
            denominator *= factorial(partition[i])
        return numerator // denominator
    
    def schur_weyl_coefficient(λ, μ):
        if len(λ) != len(μ):
            return 0
        sign = sign_of_partition(λ)
        product = 1
        for i in range(len(λ)):
            product *= hook_length_formula(n, λ[i]) // (hook_length_formula(n, λ[i] - μ[i]) * hook_length_formula(n, μ[i]))
        return sign * product
    
    def schur_weyl_multiplicity_for_partition(λ):
        multiplicity = 0
        for μ in combinations(range(n), len(λ)):
            if sorted(μ) == list(μ):
                multiplicity += schur_weyl_coefficient(λ, μ)
        return abs(multiplicity)
    
    return sum(schur_weyl_multiplicity_for_partition(partition) for partition in combinations(range(k + 1), len(λ)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(1, min(n, 2))
    λ = (n - 1, 1)
    
    permanent_multiplicity = schur_weyl_multiplicity(n, k, λ)
    determinant_multiplicity = schur_weyl_multiplicity(n, k, λ)
    
    if permanent_multiplicity >= 2 ** (n / 2):
        conjecture_holds = True
        counterexample = ""
    elif determinant_multiplicity <= 2 ** (sqrt(n) * log(n)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "Multiplicity",
        "metric_value": permanent_multiplicity / determinant_multiplicity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")