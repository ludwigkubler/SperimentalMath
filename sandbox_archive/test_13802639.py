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
    while n < len(f):
        n *= 2
    f.extend([0] * (n - len(f)))
    return fast_walsh_hadamard_transform(f)

def fourier_coefficient_sum(f, log_n):
    n = len(f)
    transform = walsh_hadamard_transform(f)
    mu = sum(abs(coeff) for i, coeff in enumerate(transform) if i.bit_count() <= log_n)
    return mu

def generate_monotone_dnf(n):
    variables = list(range(n))
    clauses = []
    for _ in range(random.randint(1, n)):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def evaluate_dnf(dnf, assignment):
    for clause in dnf:
        if all(assignment[var] for var in clause):
            return 1
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    log_n = math.ceil(math.log2(n))
    
    f = generate_monotone_dnf(n)
    g = generate_monotone_dnf(n)
    
    mu_f = fourier_coefficient_sum(f, log_n)
    mu_g = fourier_coefficient_sum(g, log_n)
    mu_fg = fourier_coefficient_sum([evaluate_dnf(f, assignment) * evaluate_dnf(g, assignment) for assignment in product([0, 1], repeat=n)], log_n)
    mu_f_or_g = fourier_coefficient_sum([evaluate_dnf(f, assignment) + evaluate_dnf(g, assignment) - evaluate_dnf(f, assignment) * evaluate_dnf(g, assignment) for assignment in product([0, 1], repeat=n)], log_n)
    
    conjecture_holds = mu_fg >= mu_f + mu_g - mu_f_or_g
    
    return {
        "metric_name": "mu",
        "metric_value": mu_fg,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    from itertools import product
    
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    total_mu = 0.0
    count_supporting = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        total_mu += result["metric_value"]
        if result["conjecture_holds"]:
            count_supporting += 1
    
    mean_mu = total_mu / len(seeds)
    std_mu = math.sqrt(sum((x - mean_mu) ** 2 for x in [r["metric_value"] for r in results]) / len(results))
    support_fraction = count_supporting / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[0]}")