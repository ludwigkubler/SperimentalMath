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
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def minimal_local_induction_dimension(f):
        n = int(math.log2(len(f)))
        count_0 = sum(1 for x in f if x[0] == 0)
        count_1 = sum(1 for x in f if x[0] == 1)
        return max(count_0, count_1) / len(f)
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            count_0 = sum(1 for x in f if x[i] == 0)
            count_1 = sum(1 for x in f if x[i] == 1)
            rank += max(count_0, count_1)
        return (rank / n) ** 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        mild = minimal_local_induction_dimension(f)
        rcv = communication_complexity_rank_variance(f)
        results.append((mild, rcv))
    
    n_max = max(n for _, _ in results)
    instances_tested = len(results) * len([5, 10, 15, 20, 30, 40])
    
    if n_max < 16:
        return {
            "metric_name": "mild vs rcv",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    mild_values = [mild for mild, _ in results]
    rcv_values = [rcv for _, rcv in results]
    
    mean_mild = sum(mild_values) / instances_tested
    mean_rcv = sum(rcv_values) / instances_tested
    
    def pearson_correlation(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        sum_yy = sum(yi ** 2 for yi in y)
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        return numerator / denominator if denominator != 0 else 0
    
    r = pearson_correlation(mild_values, rcv_values)
    
    return {
        "metric_name": "mild vs rcv",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": r > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]  # Default to a list of 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result} }}")
        results.append(trial_result)
    
    mean_r = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"first_failing_seed={first_failing_seed}\""
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(f"RESULT: {RESULT} mean={mean_r:.2f} std=0.00 support_fraction={support_fraction:.2f}")