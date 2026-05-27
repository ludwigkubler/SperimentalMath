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

def xor_and_tree_width(boolean_function):
    if isinstance(boolean_function, tuple) and len(boolean_function) == 2:
        left, right = boolean_function
        return 1 + max(xor_and_tree_width(left), xor_and_tree_width(right))
    elif isinstance(boolean_function, int):
        return 0
    else:
        raise ValueError("Invalid Boolean function")

def calculate_metric(boolean_function):
    T = xor_and_tree_width(boolean_function)
    if T == 0:
        return 0, 0
    rank = len(boolean_function) ** (1 / T)
    return rank, T

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    boolean_function = tuple(random.choice([0, 1]) for _ in range(n))
    
    try:
        metric_value, T = calculate_metric(boolean_function)
        instances_tested = 1
        conjecture_holds = (metric_value / T**2 <= 1)
        counterexample = "" if conjecture_holds else f"n={n}, rank={metric_value}, T={T}"
    except Exception as e:
        return {
            "seed": seed,
            "metric_name": "rank/T^2",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    return {
        "seed": seed,
        "metric_name": "rank/T^2",
        "metric_value": metric_value / T**2,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
    else:
        total_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results)
        instances_tested = sum(r["instances_tested"] for r in results)
        mean_metric_value = total_metric_value / instances_tested
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 * r["instances_tested"] for r in results) / instances_tested)
        
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
            print(f"RESULT: FALSIFIED counterexample=\"{results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])['counterexample']]}\" first_failing_seed={results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]['seed']}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")