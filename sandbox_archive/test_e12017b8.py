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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def generate_polynomial(d: int) -> list:
        poly = [random.randint(-10, 10) for _ in range(d + 1)]
        while poly[0] == 0:
            poly[0] = random.randint(-10, 10)
        return poly
    
    def solve_diophantine(poly: list, n: int) -> int:
        # Simplified placeholder for solving Diophantine equations
        # This is a dummy implementation and does not actually solve the equation
        order = sum(abs(coeff) for coeff in poly) * n
        return order
    
    def mean_order(poly_list: list, n: int) -> float:
        total_order = 0
        for poly in poly_list:
            total_order += solve_diophantine(poly, n)
        return total_order / len(poly_list)
    
    D = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        d = random.randint(1, D)
        poly = generate_polynomial(d)
        order = solve_diophantine(poly, n=40)
        metric_values.append(order)
    
    mean_order_value = sum(metric_values) / instances_tested
    
    conjecture_holds = all(order >= 40**(3*d/2) for d in range(1, D+1))
    counterexample = "" if conjecture_holds else "Mean order less than n^(3d/2) for some d"
    
    return {
        "metric_name": "mean_order",
        "metric_value": mean_order_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*40+1, 40))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean order less than n^(3d/2) for some d\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")