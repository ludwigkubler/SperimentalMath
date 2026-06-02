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
    
    def characteristic_polynomial(f):
        n = len(f)
        poly = [0] * (n + 1)
        poly[0] = 1
        for i in range(n):
            if f[i]:
                for j in range(n, -1, -1):
                    poly[j] = (poly[j] << 1) % 2
                    if j > 0:
                        poly[j-1] += poly[j]
        return poly
    
    def elliptic_curve_integration(poly):
        n = len(poly)
        integral = [0] * (n + 1)
        for i in range(n):
            integral[i+1] = poly[i] / (i + 1)
        return integral
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            if f[i]:
                rank += 1
        return rank
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        poly = characteristic_polynomial(f)
        integral = elliptic_curve_integration(poly)
        rank = communication_complexity_rank(f)
        
        if len(integral) != len(poly):
            return {
                "metric_name": "LII",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "integration_length_mismatch"
            }
        
        metric_values.append((integral[-1], rank))
    
    if not metric_values:
        return {
            "metric_name": "LII",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_metric_values"
        }
    
    lii_values, ranks = zip(*metric_values)
    mean_lii = sum(lii_values) / len(lii_values)
    mean_rank = sum(ranks) / len(ranks)
    abs_diff_mean = abs(mean_lii - mean_rank)
    
    correlation_coefficient = 0
    if len(lii_values) > 1:
        numerator = sum((lii_values[i] - mean_lii) * (ranks[i] - mean_rank) for i in range(len(lii_values)))
        denominator = math.sqrt(sum((lii_values[i] - mean_lii)**2 for i in range(len(lii_values)))) * math.sqrt(sum((ranks[i] - mean_rank)**2 for i in range(len(ranks))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "LII",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and abs_diff_mean <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_sufficiently_high\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_correlation_too_low")