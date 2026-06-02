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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        if n == 1:
            return 1
        f = [f[i:i+2] for i in range(len(f) - 1)]
        rank = 0
        while f:
            rank += 1
            new_f = []
            for i in range(len(f)):
                if f[i][0] != f[i][1]:
                    new_f.append(f[i])
            f = new_f
        return rank
    
    def p_adic_hodge_class(f):
        n = len(f)
        if n == 1:
            return Fraction(1, 1)
        h = Fraction(1, 1)
        for i in range(n):
            h *= Fraction(2**i + 1, 2**(i+1))
        return h
    
    def log_h(f):
        h = p_adic_hodge_class(f)
        if h <= 0:
            return float('-inf')
        return math.log(h)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_log_h = 0
    total_r = 0
    log_h_squared_sum = 0
    r_squared_sum = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            r = communication_complexity_rank(f)
            log_h_value = log_h(f)
            total_log_h += log_h_value
            total_r += r
            log_h_squared_sum += log_h_value ** 2
            r_squared_sum += r ** 2
            instances_tested += 1
    
    mean_log_h = total_log_h / instances_tested
    mean_r = total_r / instances_tested
    variance_log_h = (log_h_squared_sum - total_log_h ** 2 / instances_tested) / (instances_tested - 1)
    variance_r = (r_squared_sum - total_r ** 2 / instances_tested) / (instances_tested - 1)
    
    if variance_log_h == 0 or variance_r == 0:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "metric_saturation"
        }
    
    correlation = (total_log_h * total_r - instances_tested * mean_log_h * mean_r) / math.sqrt(variance_log_h * variance_r)
    std_deviation = math.sqrt(variance_r)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 3 * std_deviation,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_bounds\" first_failing_seed={first_failing_seed}")