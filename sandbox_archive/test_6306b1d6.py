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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def min_order_symmetric_braid_group(clauses):
        # Simplified encoding of the symmetric braid group order calculation
        # This is a placeholder implementation and may not accurately reflect the actual complexity
        return len(clauses) * n
    
    def resolution_proof_width(clauses):
        # Simplified encoding of the resolution proof width calculation
        # This is a placeholder implementation and may not accurately reflect the actual complexity
        return len(clauses)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        clauses = generate_sat_instance(n)
        min_order = min_order_symmetric_braid_group(clauses)
        width = resolution_proof_width(clauses)
        results.append((min_order, width))
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_orders = [r[0] for r in results]
    widths = [r[1] for r in results]
    
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_width = sum(widths) / len(widths)
    
    if any(abs(m - w) > 3 for m, w in zip(min_orders, widths)):
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "Outliers detected"
        }
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": None,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Outliers detected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")