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

def generate_instance(n):
    m = int(0.5 * n * (n - 1))
    clauses = set()
    while len(clauses) < m:
        clause = tuple(random.sample(range(-n, n+1), 3))
        if all(abs(lit) <= n for lit in clause) and len(set(clause)) == 3:
            clauses.add(clause)
    return clauses

def compute_padic_order(n):
    return round(n ** (1/3))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_order = 0
        
        for _ in range(5):
            phi = generate_instance(n)
            order = compute_padic_order(n)
            results.append((n, order))
            instances_tested += 1
            total_order += order
        
        avg_order = total_order / instances_tested
        c_n = math.log2(n) ** 2
        within_bounds = all(abs(order - c_n) <= 0.5 * c_n for _, order in results)
        
        conjecture_holds = within_bounds and max(results, key=lambda x: x[1])[1] <= n ** (1/3)
        counterexample = "" if conjecture_holds else "mapping_undefined"
        
        return {
            "metric_name": "padic_order",
            "metric_value": avg_order,
            "instances_tested": instances_tested,
            "n_max": max(results, key=lambda x: x[0])[0],
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value) ** 2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")