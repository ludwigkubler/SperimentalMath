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

def fast_walsh_hadamard_transform(f):
    n = len(f)
    if n == 1:
        return f
    even = fast_walsh_hadamard_transform(f[0::2])
    odd = fast_walsh_hadamard_transform(f[1::2])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def walsh_hadamard_transform(f):
    n = len(f)
    while n > 1:
        f = fast_walsh_hadamard_transform(f)
        n //= 2
    return f

def fourier_coefficient_sum(f, log_n):
    transform = walsh_hadamard_transform(f)
    mu = sum(abs(coeff) for coeff in transform[:2**log_n])
    return mu

def generate_monotone_dnf(n):
    num_clauses = random.randint(1, n // 2)
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice([0, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] == 0 or clause[i] == clause[0] for i in range(1, n)):
            clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    log_n = math.ceil(math.log2(n))
    
    f = generate_monotone_dnf(n)
    g = generate_monotone_dnf(n)
    
    mu_f = fourier_coefficient_sum(f, log_n)
    mu_g = fourier_coefficient_sum(g, log_n)
    mu_fg = fourier_coefficient_sum([x and y for x in f for y in g], log_n)
    mu_fog = fourier_coefficient_sum([x or y for x in f for y in g], log_n)
    
    conjecture_holds = (mu_fg >= mu_f + mu_g - mu_fog)
    counterexample = "" if conjecture_holds else "counterexample"
    
    return {
        "metric_name": "μ(f) + μ(g) - μ(f ∨ g)",
        "metric_value": mu_fg - mu_f - mu_g + mu_fog,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 7 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")