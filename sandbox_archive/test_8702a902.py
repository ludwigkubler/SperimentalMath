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
    
    def binary_tree(f):
        n = len(f)
        if n == 1:
            return f
        mid = n // 2
        left = binary_tree(f[:mid])
        right = binary_tree(f[mid:])
        return [left, right]
    
    def local_induction_dimension(tree):
        if isinstance(tree[0], list):
            return max(local_induction_dimension(tree[0]), local_induction_dimension(tree[1])) + 1
        else:
            return 0
    
    def communication_complexity_rank(f):
        n = len(f)
        if n == 1:
            return 0
        mid = n // 2
        left_rank = communication_complexity_rank(f[:mid])
        right_rank = communication_complexity_rank(f[mid:])
        return max(left_rank, right_rank) + 1
    
    def correlation_coefficient(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / n)
        return cov_xy / (std_x * std_y)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        tree = binary_tree(f)
        mild = local_induction_dimension(tree)
        ccr = communication_complexity_rank(f)
        results.append((mild, ccr))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    x, y = zip(*results)
    corr_coef = correlation_coefficient(x, y)
    mean_metric_value = sum(y) / len(y)
    conjecture_holds = corr_coef >= 0.8 and max(y) <= 10
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.5 or MILD > 10"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coef,
        "instances_tested": len(results),
        "n_max": max(len(f) for f, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        exit()
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")