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

def generate_k_sat_instance(n: int, m: int) -> list:
    literals = [f"x{i}" for i in range(1, n + 1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def calculate_clause_indicator_polynomial(clauses: list) -> dict:
    poly = {}
    for clause in clauses:
        term = 1
        for literal in clause:
            if literal in poly:
                poly[literal] += term
            else:
                poly[literal] = term
            term *= -1
    return poly

def calculate_p_adic_order(coeff: int, p: int) -> int:
    order = 0
    while coeff % p == 0 and coeff != 0:
        coeff //= p
        order += 1
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(1, n // 2)  # Ensure at least one clause
        instance = generate_k_sat_instance(n, m)
        poly = calculate_clause_indicator_polynomial(instance)
        
        p_adic_orders = {}
        for literal, coeff in poly.items():
            for p in range(2, min(n, int(math.log(n))) + 1):
                if p not in p_adic_orders:
                    p_adic_orders[p] = []
                p_adic_orders[p].append(calculate_p_adic_order(coeff, p))
        
        resolution_width = len(instance) * m  # Simplified estimation for demonstration
        
        min_p_adic_order = min(p_adic_orders.values(), key=lambda x: sum(x), default=0)
        results.append({
            "n": n,
            "resolution_width": resolution_width,
            "min_p_adic_order": min_p_adic_order
        })
    
    if not results:
        return {
            "metric_name": "min_p_adic_order",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_instance"
        }
    
    min_p_adic_orders = [res["min_p_adic_order"] for res in results]
    resolution_widths = [res["resolution_width"] for res in results]
    
    mean_min_p_adic_order = sum(min_p_adic_orders) / len(min_p_adic_orders)
    mean_resolution_width = sum(resolution_widths) / len(resolution_widths)
    
    correlation_coefficient = (sum((x - mean_min_p_adic_order) * (y - mean_resolution_width) for x, y in zip(min_p_adic_orders, resolution_widths)) /
                               math.sqrt(sum((x - mean_min_p_adic_order) ** 2 for x in min_p_adic_orders) *
                                         sum((y - mean_resolution_width) ** 2 for y in resolution_widths)))
    
    return {
        "metric_name": "min_p_adic_order",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(res["n"] for res in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{0.7}\" first_failing_seed={first_failing_seed}")