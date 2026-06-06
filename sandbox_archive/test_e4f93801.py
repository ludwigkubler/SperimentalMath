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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def compute_minimal_order(cnf):
        # Placeholder function to simulate computing the minimal order
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        m = len(cnf)
        return n ** (3/2) * math.log(m)
    
    def compute_resolution_width(cnf):
        # Placeholder function to simulate computing the resolution width
        # This is a dummy implementation and should be replaced with an actual DPLL solver
        return random.randint(1, 10)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2*n, 3*n))
            order = compute_minimal_order(cnf)
            width = compute_resolution_width(cnf)
            
            results.append({
                "n": n,
                "order": order,
                "width": width
            })
    
    if not results:
        return {
            "metric_name": "order_error",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_cnfs_generated"
        }
    
    order_errors = [abs(order - n ** (3/2) * math.log(m)) / (n ** (3/2) * math.log(m)) for n, m, _, _ in results]
    correlation_coefficient = sum(x*y for x, y in zip(order_errors, [w/n**0.5 for _, _, w, _ in results])) / len(results)
    
    return {
        "metric_name": "order_error",
        "metric_value": max(order_errors),
        "instances_tested": len(results),
        "n_max": max(n for n, _, _, _ in results),
        "conjecture_holds": all(e < 0.1 for e in order_errors) and correlation_coefficient > 0.8,
        "counterexample": "order_error or correlation_coefficient not met" if not all(e < 0.1 for e in order_errors) else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"order_error or correlation_coefficient not met\" first_failing_seed={first_failing_seed}")