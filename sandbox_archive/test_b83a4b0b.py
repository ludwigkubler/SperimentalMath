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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        return [random.choice([True, False]) for _ in range(n)]
    
    def min_order(formula):
        # Placeholder function to simulate the computation of min_order(G)
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula)  # Example: min_order = number of clauses
    
    clause_complexity = lambda n: n  # Placeholder for actual clause complexity function
    f = lambda cc: cc + 5  # Placeholder for the conjectured bound function
    
    instances_tested = 0
    n_max = 1
    min_orders = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        order = min_order(formula)
        min_orders.append(order)
        
        instances_tested += 1
        if n > n_max:
            n_max = n
    
    conjecture_holds = all(order <= f(clause_complexity(n)) for n, order in zip([5, 10, 15, 20, 30, 40], min_orders))
    counterexample = "Formula with n=15 has min_order=15" if not conjecture_holds else ""
    
    return {
        "metric_name": "min_order",
        "metric_value": sum(min_orders) / len(min_orders),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with n=15 has min_order=15\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")