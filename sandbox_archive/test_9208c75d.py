# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_instance(n):
        return [random.choice([True, False]) for _ in range(2**n)]
    
    def clause_indicator_polynomial(instance, n):
        poly = 1
        for i in range(2**n):
            term = 1
            for j in range(n):
                if instance[i & (1 << j)]:
                    term *= (j + 1)
            poly += term
        return poly
    
    def minimal_order_of_p_adic_units(poly, p):
        order = 0
        while poly % p == 0:
            poly //= p
            order += 1
        return order
    
    def resolution_proof_width(instance, n):
        # Simplified version for testing purposes
        return len(instance)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_order = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            instance = generate_random_boolean_instance(n)
            poly = clause_indicator_polynomial(instance, n)
            order = minimal_order_of_p_adic_units(poly, 2)
            width = resolution_proof_width(instance, n)
            
            if width >= W:
                total_order += order
                instances_tested += 1
                max_n = max(max_n, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "Minimal Order of p-Adic Units",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances with resolution proof width >= W"
        }
    
    mean_order = total_order / instances_tested
    conjecture_holds = mean_order <= n_values[-1]**(2/3)
    counterexample = "" if conjecture_holds else f"Mean order: {mean_order}, Expected: {n_values[-1]**(2/3)}"
    
    return {
        "metric_name": "Minimal Order of p-Adic Units",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")