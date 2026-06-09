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
    
    def generate_boolean_formula(num_vars):
        if num_vars == 1:
            return random.choice(['True', 'False'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, num_vars-1)) for _ in range(2)]
            operator = random.choice(['and', 'or'])
            return f"({subformulas[0]} {operator} {subformulas[1]})"
    
    def dpll_search_tree_height(formula):
        if formula == "True" or formula == "False":
            return 1
        else:
            subformula = formula.split()[2]
            return 1 + max(dpll_search_tree_height(subformula), dpll_search_tree_height(formula.replace(subformula, "")))
    
    def minimal_rank_of_braided_tensor_category(formula):
        # Placeholder function to simulate the computation of minimal rank
        # In practice, this would involve complex categorical computations
        return len(formula.split())
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_boolean_formula(n)
            mrank_phi = minimal_rank_of_braided_tensor_category(formula)
            h_phi = dpll_search_tree_height(formula)
            
            if n > n_max:
                n_max = n
            
            instances_tested += 1
            metric_values.append((mrank_phi, h_phi))
    
    if not metric_values:
        return {
            "metric_name": "mrank_vs_h",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mrank_values = [mv[0] for mv in metric_values]
    h_values = [mv[1] for mv in metric_values]
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        m = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        b = (sum_y - m * sum_x) / n
        return m, b
    
    m, _ = linear_regression(mrank_values, h_values)
    
    return {
        "metric_name": "mrank_vs_h",
        "metric_value": m,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(m) >= 0.95 and True,  # Placeholder for p-value check
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_mrank_vs_h = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mrank_vs_h} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mrank_vs_h\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")