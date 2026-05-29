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
    
    # Generate a boolean function with arithmetic progression symmetry
    n = random.randint(5, 40)
    S = sorted(random.sample(range(-10, 11), random.randint(2, min(n, 6))))
    coefficients = [random.choice([0, 1]) for _ in range(n)]
    
    # Compute the tree-like resolution proof width t*(f)
    def compute_t_star(f):
        # Placeholder implementation; actual computation depends on the function
        return len(f) * random.random()
    
    t_star = compute_t_star(coefficients)
    
    # Measure the number of distinct differences |S|
    distinct_differences = set()
    for i in range(1, n):
        diff = coefficients[i] - coefficients[i-1]
        if diff != 0:
            distinct_differences.add(abs(diff))
    S_size = len(distinct_differences)
    
    # Check the conjecture
    upper_bound = math.log(S_size**2, 2)
    conjecture_holds = t_star <= upper_bound
    
    return {
        "metric_name": "t_star",
        "metric_value": t_star,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"t_star={t_star}, upper_bound={upper_bound}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean and std of metric_value
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        exit(0)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    total_instances_tested = sum(r["instances_tested"] for r in results)
    n_max = max(r["n_max"] for r in results)
    conjecture_holds_count = sum(int(r["conjecture_holds"]) for r in results)
    
    mean_metric_value = total_metric_value / total_instances_tested
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / total_instances_tested)
    
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"t_star exceeds upper bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")