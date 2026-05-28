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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def and_or_tree_width(f):
        n = len(f)
        if n == 1:
            return 1
        left_half = f[:n//2]
        right_half = f[n//2:]
        left_width = and_or_tree_width(left_half)
        right_width = and_or_tree_width(right_half)
        return max(left_width, right_width) + 1
    
    def birational_geometry_invariant(f):
        n = len(f)
        if n == 1:
            return abs(f[0])
        left_half = f[:n//2]
        right_half = f[n//2:]
        left_inv = birational_geometry_invariant(left_half)
        right_inv = birational_geometry_invariant(right_half)
        return max(left_inv, right_inv) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        width = and_or_tree_width(f)
        inv = birational_geometry_invariant(f)
        results.append((n, width, inv))
    
    max_inv = max(inv for _, _, inv in results)
    c = 1.0  # Example constant, adjust as needed
    bound = math.log(max_inv) ** c
    
    metric_name = "maximal_order_of_invariant"
    metric_value = max_inv
    instances_tested = len(results)
    conjecture_holds = all(inv <= bound for _, _, inv in results)
    counterexample = "" if conjecture_holds else f"n={n}, width={width}, inv={inv}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")