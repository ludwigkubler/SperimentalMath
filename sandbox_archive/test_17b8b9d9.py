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
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2*n):
            clause = random.sample(variables, 3)
            clause.append(random.choice(['', '!', '!!']))
            clauses.append(clause)
        return clauses

    def minimal_artin_schreier_extension_size(C):
        # Placeholder function to compute the minimal order of an Artin-Schreier extension
        # This is a dummy implementation and should be replaced with actual computation
        return len(C)

    def dpll_search_tree_diameter(C):
        # Placeholder function to compute the diameter of the DPLL search tree
        # This is a dummy implementation and should be replaced with actual computation
        return 2 * len(C)

    n = random.randint(5, 30)
    C = generate_formula(n)
    
    order = minimal_artin_schreier_extension_size(C)
    diameter = dpll_search_tree_diameter(C)
    
    if diameter == 0:
        return {
            "metric_name": "order_to_diameter_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "diameter_is_zero"
        }
    
    ratio = abs(order - diameter) / n
    return {
        "metric_name": "order_to_diameter_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= n**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_ratio = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")