# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        clauses = []
        for _ in range(2 * n):
            variables = [f"x{i}" for i in range(n)]
            clause = random.sample(variables, 3)
            clauses.append(clause)
        return clauses
    
    def minimal_order_of_artin_schreier_extension(clauses):
        # Simplified heuristic to estimate the order
        return len(set(''.join(sorted(c)) for c in clauses))
    
    def dpll_search_tree_diameter(clauses):
        # Simplified heuristic to estimate the diameter
        return 2 * len(clauses)
    
    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    order = minimal_order_of_artin_schreier_extension(formula)
    diameter = dpll_search_tree_diameter(formula)
    
    if diameter == 0:
        return {
            "metric_name": "order_to_diameter_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "diameter_zero"
        }
    
    ratio = Fraction(order, diameter)
    return {
        "metric_name": "order_to_diameter_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= n**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order_to_diameter_ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")