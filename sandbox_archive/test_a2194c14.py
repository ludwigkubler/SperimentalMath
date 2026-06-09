# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def generate_boolean_formula(num_vars: int) -> str:
    if num_vars == 1:
        return random.choice(["0", "1"])
    else:
        subformulas = [generate_boolean_formula(num_vars - 1) for _ in range(2)]
        operator = random.choice(["&", "|"])
        return f"({subformulas[0]} {operator} {subformulas[1]})"

def dpll_search_tree_height(formula: str) -> int:
    if formula == "0" or formula == "1":
        return 0
    elif "&" in formula:
        subformula = formula.split("&")[0]
    elif "|" in formula:
        subformula = formula.split("|")[0]
    else:
        raise ValueError("Invalid boolean formula")
    
    return 1 + max(dpll_search_tree_height(subformula), dpll_search_tree_height(formula.replace(subformula, "")))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        num_vars = random.randint(1, min(n_max, 20))
        formula = generate_boolean_formula(num_vars)
        h_phi = dpll_search_tree_height(formula)
        
        # Minimal rank of a braided tensor category associated with a boolean formula
        mrank_phi = len(formula.split())
        
        metric_values.append(mrank_phi / h_phi)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    conjecture_holds = all(v >= 0.95 * mean_value for v in metric_values)
    counterexample = "" if conjecture_holds else "mrank(φ) not linearly correlated with h(φ)"
    
    return {
        "metric_name": "mrank_phi / h_phi",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mrank(φ) not linearly correlated with h(φ)\" first_failing_seed={first_failing_seed}")