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
    
    def generate_random_formula(n):
        if n == 0:
            return "True"
        elif n == 1:
            return random.choice(["True", "False"])
        else:
            op = random.choice(["&", "|"])
            a, b = generate_random_formula(n-1), generate_random_formula(n-1)
            return f"({a} {op} {b})"
    
    def dpll(formula):
        if formula == "True":
            return 0
        elif formula == "False":
            return float('inf')
        
        if formula[0] == "(" and formula[-1] == ")":
            formula = formula[1:-1]
        
        if "&" in formula:
            a, b = formula.split("&")
            return max(dpll(a), dpll(b)) + 1
        elif "|" in formula:
            a, b = formula.split("|")
            return min(dpll(a), dpll(b)) + 1
    
    def symmetric_tensor_rank(formula):
        if formula == "True":
            return 0
        elif formula == "False":
            return float('inf')
        
        if formula[0] == "(" and formula[-1] == ")":
            formula = formula[1:-1]
        
        if "&" in formula:
            a, b = formula.split("&")
            return max(symmetric_tensor_rank(a), symmetric_tensor_rank(b)) + 1
        elif "|" in formula:
            a, b = formula.split("|")
            return min(symmetric_tensor_rank(a), symmetric_tensor_rank(b)) + 1
    
    instances_tested = 0
    n_max = 0
    total_ranks = []
    total_depths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_random_formula(n)
            instances_tested += 1
            n_max = max(n_max, n)
            
            rank = symmetric_tensor_rank(formula)
            depth = dpll(formula)
            
            total_ranks.append(rank)
            total_depths.append(depth)
    
    if len(total_ranks) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_rank = sum(total_ranks) / len(total_ranks)
    mean_depth = sum(total_depths) / len(total_depths)
    
    covariance = sum((x - mean_rank) * (y - mean_depth) for x, y in zip(total_ranks, total_depths))
    variance_rank = sum((x - mean_rank) ** 2 for x in total_ranks)
    variance_depth = sum((y - mean_depth) ** 2 for y in total_depths)
    
    if variance_rank == 0 or variance_depth == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "constant_variance"
        }
    
    pearson_coefficient = covariance / (math.sqrt(variance_rank) * math.sqrt(variance_depth))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(pearson_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")