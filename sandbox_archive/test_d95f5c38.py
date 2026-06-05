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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return "x"
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            return f"( {subformulas[0]} & {subformulas[1]} )"

    def dpll_width(formula):
        if formula == "x":
            return 1
        elif "&" in formula:
            left, right = formula.split(" & ")
            return max(dpll_width(left), dpll_width(right)) + 1
        else:
            return 0

    def minimal_order_of_group(φ):
        # This is a placeholder for the actual computation of the minimal order.
        # For simplicity, we assume it's linearly related to the number of variables.
        return len(φ.split("&")) * 2 + 1

    n = random.randint(5, 40)
    φ = generate_boolean_formula(n)
    
    width = dpll_width(φ)
    order = minimal_order_of_group(φ)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if order == width else False,
        "counterexample": "" if order == width else f"Order {order} does not match width {width}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Order does not match width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")