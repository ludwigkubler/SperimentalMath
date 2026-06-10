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

def generate_formula(n):
    if n == 1:
        return "A"
    elif n == 2:
        return "(A & B)"
    else:
        left = generate_formula(random.randint(1, min(n-2, 3)))
        right = generate_formula(random.randint(1, min(n-2, 3)))
        operator = random.choice(["&", "|"])
        return f"({left} {operator} {right})"

def incidence_poset(formula):
    if formula == "A":
        return {"A"}
    elif formula == "(A & B)":
        return {"A", "B", "A&B"}
    else:
        left, operator, right = formula.split()
        poset_left = incidence_poset(left)
        poset_right = incidence_poset(right)
        if operator == "&":
            return poset_left.union(poset_right)
        elif operator == "|":
            return poset_left.union(poset_right).union({"A&B"})

def ehrhart_semigroup(poset):
    n = len(poset)
    semigroup = []
    for i in range(1 << n):
        subset = [poset[j] for j in range(n) if (i & (1 << j))]
        if all(x in poset for x in subset):
            semigroup.append(len(subset))
    return sorted(semigroup)

def resolution_width(formula):
    # Simplified model of resolution width
    return len(formula.split())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        poset = incidence_poset(formula)
        semigroup = ehrhart_semigroup(poset)
        width = resolution_width(formula)
        
        if not semigroup or width <= 0:
            return {
                "metric_name": "resolution_width",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "empty_semigroup_or_zero_width"
            }
        
        results.append({
            "semigroup_size": len(semigroup),
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    semigroup_sizes = [r["semigroup_size"] for r in results]
    widths = [r["width"] for r in results]
    
    mean_semigroup_size = sum(semigroup_sizes) / len(semigroup_sizes)
    mean_width = sum(widths) / len(widths)
    abs_diff = sum(abs(a - b) for a, b in zip(semigroup_sizes, widths)) / len(results)
    
    correlation_coefficient = 0
    if len(set(widths)) > 1 and len(set(semigroup_sizes)) > 1:
        numerator = sum((a - mean_semigroup_size) * (b - mean_width) for a, b in zip(semigroup_sizes, widths))
        denominator = math.sqrt(sum((a - mean_semigroup_size) ** 2 for a in semigroup_sizes)) * math.sqrt(sum((b - mean_width) ** 2 for b in widths))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={sum(run_trial(seed)['metric_value'] for seed in seeds)/len(seeds)} std=0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        first_failing_seed = next(seed for seed, result in enumerate([run_trial(seed) for seed in seeds], start=min(seeds)) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_metric")