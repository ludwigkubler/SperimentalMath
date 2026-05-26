# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def read_twice_branching_program(width):
    if width == 1:
        return [[0]]
    
    program = []
    current_level = [0]
    for _ in range(width - 1):
        next_level = []
        for node in current_level:
            choices = [random.randint(0, 1) for _ in range(len(current_level))]
            next_level.extend(choices)
        program.append(next_level)
        current_level = next_level
    return program

def groupoid_cohomology(program):
    if not program:
        return 0
    
    n = len(program[-1])
    cohomology = [0] * n
    for level in reversed(program):
        for i, choice in enumerate(level):
            cohomology[i] += choice
    return max(cohomology)

def spearman_rank_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    x_sorted = sorted(range(n), key=lambda i: x[i])
    y_sorted = sorted(range(n), key=lambda i: y[i])
    
    rank_x = [x_sorted.index(i) for i in range(n)]
    rank_y = [y_sorted.index(i) for i in range(n)]
    
    d_squared_sum = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
    rho_numerator = 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
    return rho_numerator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    widths = [5, 10, 15, 20, 30, 40]
    results = []
    
    for width in widths:
        program = read_twice_branching_program(width)
        cohomology = groupoid_cohomology(program)
        log_width = math.log(width)
        
        results.append((cohomology, log_width))
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_program"
        }
    
    cohomology_values, log_widths = zip(*results)
    rho = spearman_rank_correlation(cohomology_values, log_widths)
    median_cohomology = sorted(cohomology_values)[len(cohomology_values) // 2]
    std_dev = (sum((x - median_cohomology) ** 2 for x in cohomology_values) / len(cohomology_values)) ** 0.5
    
    expected_median = sum(math.log(w) for w in widths) / len(widths)
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho > 0.7 and abs(median_cohomology - expected_median) <= std_dev,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 prime numbers
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        std_dev_rho = (sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_dev_rho} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_trials_passed")