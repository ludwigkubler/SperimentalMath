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

def generate_boolean_formula(n):
    if n == 0:
        return "True"
    elif n == 1:
        return "False"
    
    op = random.choice(["&", "|"])
    left = generate_boolean_formula(random.randint(0, n//2))
    right = generate_boolean_formula(n - len(left.split("&")) - len(right.split("|")))
    return f"({left} {op} {right})"

def min_order(n):
    if n == 1:
        return 1
    else:
        return 2 * min_order(n // 2) + 1

def frege_proof_depth(formula):
    if formula in ["True", "False"]:
        return 0
    elif "&" in formula:
        left, right = formula.split("&")
        return max(frege_proof_depth(left), frege_proof_depth(right)) + 1
    else:
        left, right = formula.split("|")
        return max(frege_proof_depth(left), frege_proof_depth(right)) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "correlation_coefficient"
    instances_tested = 0
    n_max = 0
    min_order_values = []
    frege_depth_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_boolean_formula(n)
        if formula:
            instances_tested += 1
            n_max = max(n_max, n)
            min_order_value = min_order(n)
            frege_depth_value = frege_proof_depth(formula)
            min_order_values.append(min_order_value)
            frege_depth_values.append(frege_depth_value)
    
    if not min_order_values or not frege_depth_values:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_min_order = sum(min_order_values) / len(min_order_values)
    mean_frege_depth = sum(frege_depth_values) / len(frege_depth_values)
    correlation_coefficient = (len(min_order_values) * sum(a * b for a, b in zip(min_order_values, frege_depth_values)) -
                                sum(min_order_values) * sum(frege_depth_values)) / \
                               math.sqrt((len(min_order_values) * sum(x**2 for x in min_order_values) - sum(min_order_values)**2) *
                                         (len(frege_depth_values) * sum(y**2 for y in frege_depth_values) - sum(frege_depth_values)**2))
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.95 and all(corr >= 0.8 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["metric_value"] < 0.8 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")