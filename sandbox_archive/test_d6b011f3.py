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
import math
from itertools import combinations

def fibonacci(n):
    fib = [0, 1]
    for i in range(2, n+1):
        fib.append(fib[-1] + fib[-2])
    return fib

def zeckendorf_length(n):
    if n == 0:
        return 0
    fib = fibonacci(n)
    length = 0
    while n > 0:
        for i in range(len(fib)-1, -1, -1):
            if fib[i] <= n:
                n -= fib[i]
                length += 1
                break
    return length

def generate_design(d, m, k, t):
    design = []
    for _ in range(m):
        row = [0]*d
        indices = random.sample(range(d), k)
        for i in indices:
            row[i] = 1
        design.append(row)
    return design

def compute_fourier_coefficient(f, n):
    max_coeff = 0
    for U in range(1, 2**n):
        coeff = 0
        for i in range(n):
            if U & (1 << i):
                coeff += f[i]
        max_coeff = max(max_coeff, abs(coeff))
    return max_coeff

def compute_bias(d, design, f, T):
    bias = 0
    for s in range(2**d):
        parity = sum(s >> i & 1 for i in T) % 2
        bias += (-1)**parity * f[s]
    return abs(bias / (2**d))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k_values = [3, 4, 5]
    m_values = [4, 5, 6, 7, 8]
    t_values = [1, 2]
    eta_values = [0.25, 0.5]
    T_values = [set(T) for T in combinations(range(1, 6), 1)] + \
               [set(T) for T in combinations(range(1, 6), 2)]
    
    results = []
    for k in k_values:
        for m in m_values:
            for t in t_values:
                d = 2 * k
                design = generate_design(d, m, k, t)
                f_values = [random.choices([0, 1], k=2**d) for _ in range(20)]
                for f in f_values:
                    max_coeff = compute_fourier_coefficient(f, d)
                    if max_coeff != eta_values[0] and max_coeff != eta_values[1]:
                        continue
                    for T in T_values:
                        bias = compute_bias(d, design, f, T)
                        results.append({
                            "metric_name": "bias",
                            "metric_value": bias,
                            "instances_tested": 1,
                            "conjecture_holds": abs(bias) <= eta_values[0]**len(T) * 2**(t*math.comb(len(T), 2)) * (1 + zeckendorf_length(sum(design[i][j] for j in T)) / k)**-1,
                            "counterexample": ""
                        })
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric_value": total_metric_value / len(results),
        "std_metric_value": 0,  # Not computing std for simplicity
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(result["mean_metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.95) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction too low")