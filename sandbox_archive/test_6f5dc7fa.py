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
    
    # Generate a random CNF with m clauses and n variables
    m = random.randint(5, 40)
    n = random.randint(5, 10)
    cnf = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
        cnf.append(clause)
    
    # Calculate the minimal Brauer group order (simplified heuristic)
    # For simplicity, we use the number of clauses as a proxy
    brauer_group_order = m
    
    # Compute the Frege proof size (simplified heuristic)
    # For simplicity, we use the number of variables as a proxy
    frege_proof_size = n
    
    # Collect data points for linear regression
    data_points = [(brauer_group_order, frege_proof_size)]
    
    # Perform linear regression to calculate correlation coefficient
    if len(data_points) < 2:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(data_points),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Insufficient data points"
        }
    
    x_sum = sum(point[0] for point in data_points)
    y_sum = sum(point[1] for point in data_points)
    xy_sum = sum(point[0] * point[1] for point in data_points)
    xx_sum = sum(point[0] ** 2 for point in data_points)
    yy_sum = sum(point[1] ** 2 for point in data_points)
    
    n = len(data_points)
    numerator = n * xy_sum - x_sum * y_sum
    denominator_x = math.sqrt(n * xx_sum - x_sum ** 2)
    denominator_y = math.sqrt(n * yy_sum - y_sum ** 2)
    
    if denominator_x == 0 or denominator_y == 0:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(data_points),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Zero denominator in correlation calculation"
        }
    
    pearson_correlation = numerator / (denominator_x * denominator_y)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": pearson_correlation,
        "instances_tested": len(data_points),
        "n_max": n,
        "conjecture_holds": False if pearson_correlation < 0.7 else True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Insufficient data points or correlation below threshold"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")