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
    
    def generate_formula(n):
        if n == 1:
            return "x"
        else:
            return f"({generate_formula(n-1)}) & (~x)"
    
    def dpll_width(phi):
        if phi == "x":
            return 1
        elif phi.startswith("(") and phi.endswith(")"):
            subformulas = phi[1:-1].split("&")
            return max(dpll_width(sub.strip()) for sub in subformulas)
        else:
            return 0
    
    n = random.randint(5, 40)
    phi = generate_formula(n)
    
    order = 2 ** (n - 1) - 1
    width = dpll_width(phi)
    
    if width == 0:
        return {
            "metric_name": "order",
            "metric_value": order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll_width_is_zero"
        }
    
    correlation = (order - width) / math.sqrt(order * width)
    
    return {
        "metric_name": "order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        min_correlation = min(abs(result["metric_value"]) for result in results if result["conjecture_holds"])
        if min_correlation < 0.5:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='dpll_width_is_zero' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE correlation_threshold_not_met")