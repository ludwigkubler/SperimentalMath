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
    
    def generate_k_sat_instance(n, k):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(k):
            clause = random.sample(literals, 3)
            clauses.append(" or ".join(clause))
        return " and ".join(clauses)
    
    def polynomial_to_coefficients(poly):
        if not poly:
            return [0]
        elif poly == "1":
            return [1]
        elif poly.startswith("~"):
            return [-1] * len(polynomial_to_coefficients(poly[2:]))
        else:
            coeffs = []
            for term in poly.split(" or "):
                if term.startswith("~"):
                    coeffs.extend([-1] * len(polynomial_to_coefficients(term[2:])))
                else:
                    coeffs.extend([1] * len(polynomial_to_coefficients(term)))
            return coeffs
    
    def p_adic_order(coeff, p):
        count = 0
        while coeff % p == 0:
            coeff //= p
            count += 1
        return count
    
    def resolution_width(instance):
        # Placeholder for actual resolution width calculation
        # This is a dummy implementation for the sake of testing
        return len(instance.split(" and ")) + len(instance.split(" or "))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, n)
        instance = generate_k_sat_instance(n, k)
        coeffs = polynomial_to_coefficients(instance)
        
        min_p_adic_order = float('inf')
        for coeff in coeffs:
            if coeff != 0:
                p = 2
                while p <= n:
                    order = p_adic_order(coeff, p)
                    if order < min_p_adic_order:
                        min_p_adic_order = order
                    p += 1
        
        width = resolution_width(instance)
        results.append({"n": n, "min_p_adic_order": min_p_adic_order, "width": width})
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_p_adic_orders = [r["min_p_adic_order"] for r in results]
    widths = [r["width"] for r in results]
    
    if len(min_p_adic_orders) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(min_p_adic_orders),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = (sum((x[i] - mean_x) ** 2 for i in range(n)) / n) ** 0.5
        std_y = (sum((y[i] - mean_y) ** 2 for i in range(n)) / n) ** 0.5
        return cov / (std_x * std_y)
    
    correlation = pearson_correlation(min_p_adic_orders, widths)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(min_p_adic_orders),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "correlation_threshold_not_met"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)