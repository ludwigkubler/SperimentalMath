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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = len(f)
        poly = [0] * (n + 1)
        poly[0] = 1
        for i in range(n):
            if f[i]:
                poly = add_polynomials(poly, multiply_polynomial(poly, [0, -2*i-1]))
        return poly
    
    def add_polynomials(p1, p2):
        n = max(len(p1), len(p2))
        result = [0] * n
        for i in range(n):
            if i < len(p1):
                result[i] += p1[i]
            if i < len(p2):
                result[i] += p2[i]
        return result
    
    def multiply_polynomial(p, q):
        n = len(p)
        m = len(q)
        result = [0] * (n + m - 1)
        for i in range(n):
            for j in range(m):
                result[i + j] += p[i] * q[j]
        return result
    
    def evaluate_polynomial(poly, x):
        n = len(poly)
        result = 0
        for i in range(n):
            result += poly[i] * (x ** i)
        return result
    
    def elliptic_curve_integration(poly):
        n = len(poly)
        integral = [0] * (n + 1)
        integral[0] = 0
        for i in range(n):
            integral[i + 1] = poly[i] / (i + 1)
        return integral
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            if f[i]:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        poly = characteristic_polynomial(f)
        integral = elliptic_curve_integration(poly)
        lii = evaluate_polynomial(integral, 1j)  # Using complex number for integration
        r_f = communication_complexity_rank(f)
        
        results.append({
            "n": n,
            "lii": lii.real,  # Taking real part as the metric value
            "r_f": r_f,
            "instances_tested": 1
        })
    
    if len(results) < 30:
        return {
            "metric_name": "LII",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([res["n"] for res in results]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    lii_values = [res["lii"] for res in results]
    r_f_values = [res["r_f"] for res in results]
    
    mean_lii = sum(lii_values) / len(lii_values)
    mean_r_f = sum(r_f_values) / len(r_f_values)
    std_lii = math.sqrt(sum((x - mean_lii) ** 2 for x in lii_values) / len(lii_values))
    
    correlation_coefficient = sum((lii_values[i] - mean_lii) * (r_f_values[i] - mean_r_f) for i in range(len(lii_values))) / (len(lii_values) * std_lii * math.sqrt(sum((x - mean_r_f) ** 2 for x in r_f_values)))
    
    return {
        "metric_name": "LII",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([res["n"] for res in results]),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_lii - mean_r_f) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len([res for res in results if res["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results if res["metric_value"] is not None) / len([res for res in results if res["metric_value"] is not None]))
    
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")