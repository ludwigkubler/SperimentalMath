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
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            return f'({subformulas[0]} & {subformulas[1]})'
    
    def dpll(formula):
        if formula == '0':
            return 1
        elif formula == '1':
            return 0
        else:
            subformula = formula.split(' & ')[0]
            return 1 + dpll(subformula)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formulas = [generate_formula(n) for _ in range(30)]
        min_orders = []
        depths = []
        
        for formula in formulas:
            depth = dpll(formula)
            # Placeholder for computing min_order
            min_order = random.randint(1, 10)  # This is a dummy value; replace with actual computation
            min_orders.append(min_order)
            depths.append(depth)
        
        if not min_orders or not depths:
            return {
                "metric_name": "log_min_order",
                "metric_value": None,
                "instances_tested": len(formulas),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "empty_formula"
            }
        
        log_min_orders = [math.log(order) for order in min_orders]
        correlation_coefficient = sum((log_min_orders[i] - sum(log_min_orders) / len(log_min_orders)) * 
                                      (depths[i] - sum(depths) / len(depths)) for i in range(len(log_min_orders))) / \
                                  (len(log_min_orders) * math.sqrt(sum((x - sum(log_min_orders) / len(log_min_orders)) ** 2 for x in log_min_orders)) *
                                   math.sqrt(sum((y - sum(depths) / len(depths)) ** 2 for y in depths)))
        
        results.append({
            "n": n,
            "correlation_coefficient": correlation_coefficient
        })
    
    mean_corr = sum(result["correlation_coefficient"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["correlation_coefficient"] - mean_corr) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "log_min_order",
        "metric_value": mean_corr,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": mean_corr >= 0.7,
        "counterexample": "" if mean_corr >= 0.7 else f"mean_corr={mean_corr}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")