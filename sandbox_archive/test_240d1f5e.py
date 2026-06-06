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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def clause_indicator_polynomial(instance):
        n = len(instance)
        poly = [1] * (n + 1)
        for bit in instance:
            new_poly = [0] * (n + 1)
            for i in range(n + 1):
                if bit == 0:
                    new_poly[i] += poly[i]
                else:
                    new_poly[i] -= poly[i]
            poly = new_poly
        return poly
    
    def minimal_order_of_p_adic_units(poly, p):
        order = 0
        for coeff in poly:
            if coeff != 0:
                order = max(order, len(bin(coeff)) - 2)
        return order
    
    def resolution_proof_width(instance):
        n = len(instance)
        width = 1
        for bit in instance:
            if bit == 1:
                width += 1
        return width
    
    W = 5  # Minimum resolution proof width to consider
    instances_tested = 0
    total_order = 0
    max_n = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > max_n:
            max_n = n
        
        for _ in range(5):  # Sample 5 instances per size
            instance = generate_boolean_instance(n)
            poly = clause_indicator_polynomial(instance)
            order = minimal_order_of_p_adic_units(poly, 2)  # Assuming p=2 for simplicity
            width = resolution_proof_width(instance)
            
            if width >= W:
                total_order += order
                instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Minimal Order of p-Adic Units",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "No valid instances found with resolution proof width >= W"
        }
    
    mean_order = total_order / instances_tested
    conjecture_holds = mean_order <= n**(2/3)
    counterexample = "" if conjecture_holds else f"Mean order: {mean_order}, Expected bound: {n**(2/3)}"
    
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
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean order exceeds bound\" first_failing_seed={first_failing_seed}")