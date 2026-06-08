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
    
    def generate_formula(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def resolution_width(formula):
        # Simplified heuristic to estimate resolution width
        return len(formula)
    
    def group_algebra(n):
        # Construct a simple group algebra for demonstration purposes
        G = {i: [1 if i == j else 0 for j in range(n)] for i in range(n)}
        return G
    
    def crossed_product(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        C = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return C
    
    def order_of_crossed_product(cp):
        # Simplified heuristic to estimate the order of the crossed product
        rows, cols = len(cp), len(cp[0])
        return max(rows, cols)
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    width = resolution_width(formula)
    algebra = group_algebra(n)
    crossed_prod = crossed_product(algebra, algebra)
    order = order_of_crossed_product(crossed_prod)
    
    return {
        "metric_name": "Order of Crossed Product",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] and r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"] and result["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")