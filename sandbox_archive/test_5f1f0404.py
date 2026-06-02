# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        for x in range(1, p):
            if (x * x) % p == a:
                return True
        return False
    
    def communication_complexity_rank(f):
        n = len(f)
        # Simplified rank calculation using random sampling
        samples = [f(tuple(random.getrandbits(1) for _ in range(n))) for _ in range(10)]
        unique_samples = set(samples)
        return len(unique_samples)
    
    def minimal_order_of_quadratic_residue(f):
        n = len(f)
        p = 2
        while True:
            if all(is_quadratic_residue(f(x), p) for x in range(2**n)):
                return p
            p += 1
    
    trials = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = lambda x: random.choice([0, 1])
            ord_f = minimal_order_of_quadratic_residue(f)
            r_f = communication_complexity_rank(f)
            trials.append((ord_f, r_f))
    
    if not trials:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ord_values = [t[0] for t in trials]
    r_values = [t[1] for t in trials]
    
    mean_ord = sum(ord_values) / len(ord_values)
    mean_r = sum(r_values) / len(r_values)
    
    if len(ord_values) < 2:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    covariance = sum((ord_values[i] - mean_ord) * (r_values[i] - mean_r) for i in range(len(ord_values))) / len(ord_values)
    variance_ord = sum((ord_values[i] - mean_ord) ** 2 for i in range(len(ord_values))) / len(ord_values)
    variance_r = sum((r_values[i] - mean_r) ** 2 for i in range(len(r_values))) / len(r_values)
    
    if variance_ord == 0 or variance_r == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_correlation_coefficient = covariance / (math.sqrt(variance_ord) * math.sqrt(variance_r))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation_coefficient,
        "instances_tested": len(ord_values),
        "n_max": max(5, 10, 15, 20, 30, 40),
        "conjecture_holds": pearson_correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")