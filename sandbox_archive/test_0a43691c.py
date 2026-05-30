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
        formula = []
        for _ in range(n):
            if random.choice([True, False]):
                formula.append("¬")
            formula.append(f"X{i}")
            if random.choice([True, False]):
                formula.append("∨")
        return " ∧ ".join(formula).replace("∧∨", "∨").replace("∨∧", "∧")

    def resolution_width(phi):
        # Simplified resolution width calculation
        return len(phi.split()) ** 2

    def non_arithmetic_curve_norm(n):
        # Simplified non-arithmetic curve norm calculation
        return n ** (1/4)

    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_formula(n)
    width = resolution_width(phi)
    C_norm = non_arithmetic_curve_norm(n)
    
    if C_norm**(1/4) > n**2 / width:
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Non-arithmetic curve too complex: C^(1/4) = {C_norm**(1/4)} > n^2 / width"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.95:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Non-arithmetic curve too complex\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")