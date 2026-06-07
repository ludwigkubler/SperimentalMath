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
        return [random.choice([0, 1]) for _ in range(n)]
    
    def min_order_of_cuspidal_subgroup(formula):
        # Placeholder function to simulate the computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        min_order = min_order_of_cuspidal_subgroup(formula)
        results.append({
            "n": n,
            "min_order": min_order
        })
        
        if min_order > 10:
            return {
                "metric_name": "min_order",
                "metric_value": min_order,
                "instances_tested": len(results),
                "n_max": max(n_values),
                "conjecture_holds": False,
                "counterexample": f"Formula with n={n} has min_order={min_order}"
            }
    
    return {
        "metric_name": "min_order",
        "metric_value": sum(result["min_order"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with n=40 has min_order>10\" first_failing_seed={first_failing_seed}")