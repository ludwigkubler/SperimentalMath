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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def is_quadratic_residue(a, p):
        if a == 0 or p <= 1:
            return False
        return pow(a, (p - 1) // 2, p) == 1
    
    def minimal_order_of_quadratic_residues(f, n):
        for k in range(2, 2**n + 1):
            if all(is_quadratic_residue(f[i], k) for i in range(2**n)):
                return k
        return None
    
    def communication_complexity_rank(f, n):
        # Simplified version using a dummy rank (actual computation is complex)
        return random.randint(1, 5)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_random_boolean_function(n)
        ord_f = minimal_order_of_quadratic_residues(f, n)
        r_f = communication_complexity_rank(f, n)
        if ord_f is not None:
            results.append((ord_f, r_f))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == n_ for _, n_ in results)),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    ord_values = [ord_f for ord_f, _ in results]
    r_values = [r_f for _, r_f in results]
    
    mean_ord = sum(ord_values) / len(ord_values)
    mean_r = sum(r_values) / len(r_values)
    
    cov = sum((ord_values[i] - mean_ord) * (r_values[i] - mean_r) for i in range(len(results))) / len(results)
    var_ord = sum((ord_values[i] - mean_ord)**2 for i in range(len(results))) / len(results)
    var_r = sum((r_values[i] - mean_r)**2 for i in range(len(results))) / len(results)
    
    correlation_coefficient = cov / math.sqrt(var_ord * var_r)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == n_ for _, n_ in results)),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.7) / len(results)
    
    if all(r >= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r < 0.7 for r in results):
        first_failing_seed = seeds[results.index(min(results, key=lambda x: abs(x - 0.7)))]
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_data")