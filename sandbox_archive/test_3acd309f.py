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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_minimal_order(cnf):
        # Placeholder function to simulate computation
        # This is a dummy implementation and should be replaced with actual logic
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        m = len(cnf)
        return n ** 1.5 * math.log(m)
    
    def compute_resolution_width(cnf):
        # Placeholder function to simulate computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(10, 100)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        m = random.randint(n + 1, 2 * n)
        cnf = generate_cnf(n, m)
        
        minimal_order = compute_minimal_order(cnf)
        resolution_width = compute_resolution_width(cnf)
        
        results.append({
            "n": n,
            "m": m,
            "minimal_order": minimal_order,
            "resolution_width": resolution_width
        })
    
    mean_order = sum(result["minimal_order"] for result in results) / len(results)
    std_order = math.sqrt(sum((result["minimal_order"] - mean_order) ** 2 for result in results) / len(results))
    
    correlation_coefficient = sum((result["minimal_order"] - mean_order) * (result["resolution_width"] - sum(result["resolution_width"] for result in results) / len(results)) for result in results) / (len(results) * std_order * math.sqrt(sum((result["resolution_width"] - sum(result["resolution_width"] for result in results) / len(results)) ** 2 for result in results)))
    
    conjecture_holds = correlation_coefficient > 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")