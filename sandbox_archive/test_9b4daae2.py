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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_algebraic_variety(f):
        n = len(f)
        x = 'x'
        poly = sum(f[i] * (x ** i) for i in range(n))
        # Simplify polynomial to get the degree
        degree = 0
        for term in poly.split('+'):
            if 'x' in term:
                coeff, exp = term.split('x^')
                degree = max(degree, int(exp))
        return degree
    
    def communication_complexity_rank(f):
        n = len(f)
        # Simplistic rank calculation based on the number of 1s
        return sum(1 for bit in f if bit == 1)
    
    instances_tested = 0
    total_diameter = 0
    total_rank = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        d_X_f = construct_algebraic_variety(f)
        r_f = communication_complexity_rank(f)
        
        total_diameter += d_X_f
        total_rank += r_f
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "d(X_f) vs. r(f)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max([5, 10, 15, 20, 30, 40]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_diameter = total_diameter / instances_tested
    mean_rank = total_rank / instances_tested
    
    correlation_coefficient = (instances_tested * sum(d_X_f * r_f for d_X_f, r_f in zip([construct_algebraic_variety(generate_boolean_function(n)) for n in [5, 10, 15, 20, 30, 40]], [communication_complexity_rank(generate_boolean_function(n)) for n in [5, 10, 15, 20, 30, 40]])) - instances_tested * mean_diameter * mean_rank) / (instances_tested * sum((d_X_f - mean_diameter)**2 for d_X_f in [construct_algebraic_variety(generate_boolean_function(n)) for n in [5, 10, 15, 20, 30, 40]]) * sum((r_f - mean_rank)**2 for r_f in [communication_complexity_rank(generate_boolean_function(n)) for n in [5, 10, 15, 20, 30, 40]]))
    
    return {
        "metric_name": "d(X_f) vs. r(f)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(correlation_coefficient >= 0.6 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.6\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")