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

def generate_random_read_twice_bp(n: int) -> list:
    bp = []
    for _ in range(2**n):
        row = [random.choice([0, 1]) for _ in range(n)]
        bp.append(row)
    return bp

def inner_product_mod_2(x: list, y: list) -> int:
    return sum(xi * yi for xi, yi in zip(x, y)) % 2

def polynomial_degree(poly: dict) -> int:
    return max(degree for degree, _ in poly.items())

def is_invariant(poly: dict, bp: list) -> bool:
    n = len(bp[0])
    for i in range(n):
        new_bp = []
        for row in bp:
            new_row = [row[j] if j != i else (1 - row[j]) for j in range(n)]
            new_bp.append(new_row)
        new_value = inner_product_mod_2([new_bp[row][i] for row in range(len(bp))], [poly[(i,)]])
        if new_value != poly[(i,)]:
            return False
    return True

def find_min_invariant_degree(bp: list, ip2_value: int) -> int:
    n = len(bp[0])
    degree = 1
    while True:
        poly = {}
        for i in range(n):
            poly[(i,)] = random.choice([0, 1])
        if is_invariant(poly, bp) and polynomial_degree(poly) > 0:
            return degree
        degree += 1

def run_trial(seed: int) -> dict:
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        random.seed(seed)
        bp = generate_random_read_twice_bp(n)
        ip2_value = inner_product_mod_2([random.choice([0, 1]) for _ in range(n)], [random.choice([0, 1]) for _ in range(n)])
        min_invariant_degree = find_min_invariant_degree(bp, ip2_value)
        results.append({
            "n": n,
            "min_invariant_degree": min_invariant_degree
        })
    metric_name = "Min Invariant Degree"
    metric_value = sum(result["min_invariant_degree"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["min_invariant_degree"] <= math.log(2**n, 2) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")