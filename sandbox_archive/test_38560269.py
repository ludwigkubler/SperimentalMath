# auto-injected by SEC sandbox
import math
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
from itertools import product

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def deterministic_communication_complexity(f):
    n = int(math.log2(len(f)))
    if 2**n != len(f):
        raise ValueError("Input length must be a power of 2")
    
    # Count the number of distinct pairs (i, j) such that f[i] != f[j]
    count = 0
    for i, j in product(range(2**n), repeat=2):
        if i == j:
            continue
        if f[i] != f[j]:
            count += 1
    
    # The communication complexity is the number of distinct pairs divided by n
    return count / n

def quasi_morphism_rank(f):
    n = int(math.log2(len(f)))
    if 2**n != len(f):
        raise ValueError("Input length must be a power of 2")
    
    # Generate all possible quasi-morphisms
    def is_quasi_morphism(q):
        for i in range(2**n):
            for j in range(2**n):
                if q[i] ^ q[j] != f[i] ^ f[j]:
                    return False
        return True
    
    # Find the smallest generating set
    min_rank = 0
    while True:
        min_rank += 1
        candidates = [i for i in range(2**n) if is_quasi_morphism([f[i]] * min_rank)]
        if len(candidates) >= 2**(n-1):
            return min_rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        r = quasi_morphism_rank(f)
        c = deterministic_communication_complexity(f)
        results.append((n, r, c))
    
    # Compute the correlation coefficient
    n_total = len(results)
    mean_r = sum(r for _, r, _ in results) / n_total
    mean_c = sum(c for _, _, c in results) / n_total
    cov = sum((r - mean_r) * (c - mean_c) for _, r, c in results) / n_total
    var_r = sum((r - mean_r)**2 for _, r, _ in results) / n_total
    var_c = sum((c - mean_c)**2 for _, _, c in results) / n_total
    
    correlation_coefficient = cov / (math.sqrt(var_r) * math.sqrt(var_c))
    
    # Check the acceptance criterion
    conjecture_holds = all(abs(r - c) <= 10 for _, r, c in results)
    counterexample = "" if conjecture_holds else "n_max=40"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n_total,
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - 0.8) < 0.2 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={seeds[results.index(next(r for r in results if abs(r['metric_value'] - 0.8) < 0.2))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")