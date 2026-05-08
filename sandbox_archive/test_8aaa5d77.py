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
    
    def generate_read_twice_bp(n):
        bp = []
        for _ in range(2 * n):
            layer = [random.choice([0, 1]) for _ in range(n)]
            bp.append(layer)
        return bp
    
    def inner_product_mod_2(x, y):
        return sum(xi * yi for xi, yi in zip(x, y)) % 2
    
    def polynomial_degree(poly):
        if not poly:
            return 0
        max_degree = 0
        for term in poly:
            degree = sum(1 for coeff in term if coeff != 0)
            if degree > max_degree:
                max_degree = degree
        return max_degree
    
    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    ip2_value = inner_product_mod_2([random.choice([0, 1]) for _ in range(n)], [random.choice([0, 1]) for _ in range(n)])
    
    def is_invariant(poly, bp):
        for i in range(len(bp)):
            new_poly = []
            for term in poly:
                new_term = [term[j] if j != i else (1 - term[j]) for j in range(len(term))]
                new_poly.append(new_term)
            if polynomial_degree(new_poly) > 0 and not any(polynomial_degree(poly) == 0 for poly in new_poly):
                return False
        return True
    
    def find_min_invariant_degree(bp, ip2_value):
        degree = 1
        while True:
            invariant_found = False
            for poly in generate_polynomials(degree):
                if is_invariant(poly, bp) and polynomial_degree(poly) > 0:
                    invariant_found = True
                    break
            if invariant_found:
                degree += 1
            else:
                return degree - 1
    
    def generate_polynomials(degree):
        terms = []
        for i in range(degree + 1):
            for j in range(degree - i + 1):
                term = [0] * (degree - i - j) + [1] * i + [2] * j
                terms.append(term)
        return terms
    
    min_invariant_degree = find_min_invariant_degree(bp, ip2_value)
    
    if n == 2:
        expected_ip2_degree = 1
    else:
        expected_ip2_degree = n
    
    conjecture_holds = min_invariant_degree <= expected_ip2_degree
    counterexample = "" if conjecture_holds else f"IP_2 degree {expected_ip2_degree}, BP degree {min_invariant_degree}"
    
    return {
        "metric_name": "Invariant Degree",
        "metric_value": min_invariant_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"IP_2 degree {expected_ip2_degree}, BP degree {min_invariant_degree}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")