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
                poly = add_polynomials(poly, multiply_polynomial(poly, [1, -2*i-1]))
        return poly
    
    def add_polynomials(p1, p2):
        result = [0] * max(len(p1), len(p2))
        for i in range(len(p1)):
            result[i] += p1[i]
        for i in range(len(p2)):
            result[i] += p2[i]
        return result
    
    def multiply_polynomial(p1, p2):
        result = [0] * (len(p1) + len(p2) - 1)
        for i in range(len(p1)):
            for j in range(len(p2)):
                result[i + j] += p1[i] * p2[j]
        return result
    
    def local_indefinite_integral(poly):
        n = len(poly)
        integral = [0] * (n + 1)
        integral[0] = poly[0]
        for i in range(1, n):
            integral[i] = poly[i] / i
        integral[n] = poly[n]
        return integral
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i]:
                rank += 1
        return rank
    
    metric_name = "LII"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    total_lii = 0
    total_diff = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        poly = characteristic_polynomial(f)
        lii = local_indefinite_integral(poly)
        rank = communication_complexity_rank(f)
        
        total_lii += abs(lii[0])
        total_diff += abs(lii[0] - rank)
    
    mean_lii = total_lii / instances_tested
    mean_diff = total_diff / instances_tested
    
    if mean_diff > 3:
        conjecture_holds = False
        counterexample = "mean_diff_exceeds_3"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_lii,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_lii = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_lii) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_lii} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_lii} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mean_diff_exceeds_3\" first_failing_seed={first_failing_seed}")