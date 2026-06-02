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
    
    def twistor_space_order(phi):
        n = len(phi)
        count = 0
        for i in range(2**n):
            if phi[i] == 1:
                count += 1
        return count
    
    def communication_complexity_rank(phi):
        n = len(phi)
        rank = 0
        for i in range(n):
            if all(phi[j] == phi[j ^ (1 << i)] for j in range(2**n)):
                rank += 1
        return rank
    
    metrics = []
    instances_tested = 30
    n_max = 40
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        phi = generate_boolean_function(n)
        min_order = twistor_space_order(phi)
        c_phi = communication_complexity_rank(phi)
        metrics.append((min_order, c_phi))
    
    if not metrics:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_orders, c_phis = zip(*metrics)
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_c_phi = sum(c_phis) / len(c_phis)
    covariance = sum((x - mean_min_order) * (y - mean_c_phi) for x, y in metrics) / len(metrics)
    variance_min_order = sum((x - mean_min_order)**2 for x in min_orders) / len(min_orders)
    variance_c_phi = sum((y - mean_c_phi)**2 for y in c_phis) / len(c_phis)
    
    if variance_min_order == 0 or variance_c_phi == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_correlation = covariance / (math.sqrt(variance_min_order) * math.sqrt(variance_c_phi))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")