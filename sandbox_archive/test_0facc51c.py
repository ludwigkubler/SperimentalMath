# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def zeckendorf_length(n):
    if n == 0:
        return 0
    length = 0
    while n > 0:
        n -= fibonacci(length)
        length += 1
    return length

def generate_design(d, m, k, t):
    design = []
    for _ in range(m):
        row = [random.randint(0, d-1) for _ in range(k)]
        if len(set(row)) == k:
            design.append(sorted(row))
    return design

def fourier_coefficient(f, U):
    total = 0
    n = len(f)
    for i in range(n):
        total += f[i] * (-1)**sum(1 << j for j in U if (i >> j) & 1)
    return abs(total / n)

def generate_boolean_function(k, eta):
    while True:
        f = [random.choice([0, 1]) for _ in range(2**k)]
        if fourier_coefficient(f, range(k)) == eta:
            return f

def compute_bias(d, design, f, T):
    bias = 0
    for s in range(1 << d):
        bitstring = [s >> j & 1 for j in range(d)]
        parity = sum(bitstring[i] for i in T) % 2
        bias += (-1)**parity * f[s]
    return abs(bias / (2**d))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k_values = [3, 4, 5]
    m_values = [4, 5, 6, 7, 8]
    t_values = [1, 2]
    eta_values = [0.25, 0.5]
    
    results = []
    
    for k in k_values:
        d = 2 * k
        for m in m_values:
            for t in t_values:
                design = generate_design(d, m, k, t)
                if len(design) < m:
                    continue
                for eta in eta_values:
                    f = generate_boolean_function(k, eta)
                    T_values = [set(range(1, i+1)) for i in range(1, min(m, 4))]
                    for T in T_values:
                        bias = compute_bias(d, design, f, T)
                        z_i = sum(zeckendorf_length(sum(1 << j for j in S if (i >> j) & 1)) for S in design)
                        Z_D = z_i / m
                        bound = eta**len(T) * 2**(t * math.comb(len(T), 2)) * (1 + Z_D / k)**-1
                        results.append({
                            "metric_name": "bias",
                            "metric_value": bias,
                            "instances_tested": 1,
                            "conjecture_holds": bias <= bound,
                            "counterexample": "" if bias <= bound else f"eta={eta}, T={T}, bias={bias}, bound={bound}"
                        })
    
    metric_values = [result["metric_value"] for result in results]
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    
    return {
        "seed": seed,
        "metric_name": "bias",
        "mean_metric_value": sum(metric_values) / len(metric_values),
        "std_metric_value": math.sqrt(sum((x - sum(metric_values) / len(metric_values))**2 for x in metric_values) / len(metric_values)),
        "fraction_conjecture_holds": sum(1 for result in results if result["conjecture_holds"]) / len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))
    
    results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["std_metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    fraction_conjecture_holds = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if fraction_conjecture_holds >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={fraction_conjecture_holds}")
    elif any(result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE no clear support or counterexamples found")