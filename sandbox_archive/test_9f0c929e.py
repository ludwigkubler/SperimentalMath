# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools
import collections

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            op = random.choice(['&', '|'])
            return f'({left} {op} {right})'
    
    def dpll_search_tree_depth(formula):
        if formula in {'0', '1'}:
            return 1
        else:
            left, op, right = formula.split()
            return max(dpll_search_tree_depth(left), dpll_search_tree_depth(right)) + 1
    
    def tropical_hodge_index(formula):
        if formula == '0':
            return 0
        elif formula == '1':
            return 1
        else:
            left, op, right = formula.split()
            if op == '&':
                return max(tropical_hodge_index(left), tropical_hodge_index(right))
            elif op == '|':
                return max(tropical_hodge_index(left), tropical_hodge_index(right)) + 1
    
    n_max = 40
    instances_tested = 30
    thi_values = []
    dpll_depths = []
    
    for _ in range(instances_tested):
        formula = generate_formula(n_max)
        thi_value = tropical_hodge_index(formula)
        dpll_depth = dpll_search_tree_depth(formula)
        
        if thi_value is not None and dpll_depth is not None:
            thi_values.append(thi_value)
            dpll_depths.append(dpll_depth)
    
    if len(thi_values) == 0 or len(dpll_depths) == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_thi = sum(thi_values) / len(thi_values)
    mean_dpll = sum(dpll_depths) / len(dpll_depths)
    covariance = sum((thi - mean_thi) * (dpll - mean_dpll) for thi, dpll in zip(thi_values, dpll_depths)) / len(thi_values)
    variance_thi = sum((thi - mean_thi) ** 2 for thi in thi_values) / len(thi_values)
    variance_dpll = sum((dpll - mean_dpll) ** 2 for dpll in dpll_depths) / len(dpll_depths)
    
    if variance_thi == 0 or variance_dpll == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_thi) * math.sqrt(variance_dpll))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")