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
from math import sqrt, pow

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def is_quasi_morphism(f, q):
    n = int(log2(len(f)))
    for i in range(2**n):
        for j in range(i + 1, 2**n):
            if q[i] ^ q[j] != f[i] ^ f[j]:
                return False
    return True

def quasi_morphism_rank(f):
    n = int(log2(len(f)))
    min_rank = 0
    while True:
        candidates = [i for i in range(2**n) if is_quasi_morphism([f[i]] * min_rank)]
        if len(candidates) == 2**n:
            return min_rank
        min_rank += 1

def communication_complexity(f):
    n = int(log2(len(f)))
    max_comm = 0
    for i in range(2**n):
        for j in range(i + 1, 2**n):
            comm = sum(f[i] ^ f[j])
            if comm > max_comm:
                max_comm = comm
    return max_comm

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        r = quasi_morphism_rank(f)
        c = communication_complexity(f)
        results.append((r, c))
    
    mean_r = sum(r for r, _ in results) / len(results)
    mean_c = sum(c for _, c in results) / len(results)
    std_dev = sqrt(sum((r - mean_r)**2 + (c - mean_c)**2 for r, c in results) / len(results))
    
    correlation_coefficient = sum((r - mean_r) * (c - mean_c) for r, c in results) / (len(results) * std_dev * std_dev)
    
    conjecture_holds = abs(correlation_coefficient) >= 0.8 and all(abs(r - c) <= 10 for r, c in results)
    counterexample = "" if conjecture_holds else "correlation_coefficient_out_of_bounds"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"]) > 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")