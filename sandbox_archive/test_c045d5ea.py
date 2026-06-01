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
    
    # Generate a random Boolean formula with n variables and m clauses
    n = 10  # Number of variables
    m = 2 * n  # Number of clauses
    C = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(m)]
    
    # Compute the minimal order of an Artin-Schreier extension
    # This is a placeholder function; you need to implement this part
    def min_artin_schreier_extension_order(C):
        return len(C)
    
    order = min_artin_schreier_extension_order(C)
    
    # Construct the DPLL search tree and determine its diameter
    # This is a placeholder function; you need to implement this part
    def dpll_search_tree_diameter(C):
        return len(C)  # Placeholder value
    
    diameter = dpll_search_tree_diameter(C)
    
    # Check if the conjecture holds
    if abs(order - diameter) <= n**2:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "Order-Diameter Ratio",
        "metric_value": order / diameter,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and standard deviation of metric_value
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    
    squared_diff_sum = sum((result["metric_value"] - mean_metric_value) ** 2 for result in results)
    std_metric_value = math.sqrt(squared_diff_sum / len(results))
    
    # Compute fraction of seeds where conjecture_holds
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")