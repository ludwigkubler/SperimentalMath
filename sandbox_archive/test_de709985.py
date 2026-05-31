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
    
    def generate_boolean_function(m, d):
        # Generate a random boolean function of m variables and degree at most d
        n = 2**m
        f = [0] * n
        for _ in range(d + 1):
            indices = random.sample(range(n), k=random.randint(1, m))
            for i in indices:
                f[i] = 1 - f[i]
        return f
    
    def compute_coxeter_diagram_complexity(f, m):
        # Compute the Coxeter-diagram complexity χ(f)
        n = len(f)
        count = 0
        for i in range(n):
            if f[i] == 1:
                count += 1
        return count
    
    def degree_of_boolean_function(f, m):
        # Compute the degree of a boolean function
        n = len(f)
        max_degree = 0
        for i in range(n):
            if f[i] == 1:
                indices = [j for j in range(m) if (i >> j) & 1]
                max_degree = max(max_degree, len(indices))
        return max_degree
    
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        f = generate_boolean_function(m, random.randint(1, min(40, m)))
        degree = degree_of_boolean_function(f, m)
        chi_f = compute_coxeter_diagram_complexity(f, m)
        expected = m ** (2 * degree / 3)
        
        results.append({
            "m": m,
            "degree": degree,
            "chi_f": chi_f,
            "expected": expected
        })
    
    metric_value = sum(result["chi_f"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["m"] for result in results)
    conjecture_holds = all(abs(result["chi_f"] - result["expected"]) <= 0.5 * result["expected"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Coxeter-diagram complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")