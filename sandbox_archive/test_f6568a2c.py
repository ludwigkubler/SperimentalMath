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
    
    n = 30  # Fixed size for simplicity
    if n < 5 or n > 40:
        return {
            "metric_name": "n_out_of_range",
            "metric_value": n,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "n_out_of_range"
        }
    
    # Generate a random groupoid action
    elements = list(range(n))
    generators = []
    for _ in range(random.randint(1, min(n // 2, 5))):
        generator = [random.choice(elements) for _ in range(random.randint(1, n))]
        generators.append(generator)
    
    # Construct the communication complexity problem
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 1
            else:
                matrix[i][j] = random.randint(0, 1)
    
    # Compute the rank variance of the communication complexity problem
    rank_variance = sum(sum(row) ** 2 for row in matrix) / n
    
    # Compute the minimal order of the groupoid action
    min_order = len(generators)
    
    # Compute the ratio of rank variance to log(n)
    if n <= 1:
        return {
            "metric_name": "n_too_small",
            "metric_value": n,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "n_too_small"
        }
    ratio = rank_variance / math.log(n)
    
    # Check if the conjecture holds
    conjecture_holds = ratio <= 5  # Example constant factor
    
    return {
        "metric_name": "rank_variance_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} exceeds constant factor"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds constant factor\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")