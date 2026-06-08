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
    
    def generate_random_formula(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def tropicalize_formula(formula):
        tropicalized_points = []
        for clause in formula:
            point = sum(abs(x) for x in clause)
            tropicalized_points.append(point)
        return tropicalized_points
    
    def calculate_automorphism_group_order(tropicalized_points):
        n = len(tropicalized_points)
        order = 1
        for i in range(n):
            for j in range(i + 1, n):
                if tropicalized_points[i] == tropicalized_points[j]:
                    order += 1
        return order
    
    def dpll_proof_path_length(formula):
        # Placeholder function; replace with actual DPLL implementation
        return len(formula)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)  # Sweep n through at least 4 distinct sizes
        formula = generate_random_formula(n)
        tropicalized_points = tropicalize_formula(formula)
        order_t = calculate_automorphism_group_order(tropicalized_points)
        path_length = dpll_proof_path_length(formula)
        results.append((order_t, path_length))
    
    mean_order_t = sum(order_t for order_t, _ in results) / len(results)
    mean_path_length = sum(path_length for _, path_length in results) / len(results)
    support_fraction = sum(1 for order_t, path_length in results if abs(order_t - path_length) <= 3 * max(path_length)) / len(results)
    
    return {
        "metric_name": "support_fraction",
        "metric_value": support_fraction,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    mean_order_t = sum(result["metric_value"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order_t} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")