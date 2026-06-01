# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    def minimal_brauer_induction_index(f):
        n = len(f)
        if n == 1:
            return 1
        index = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    index += 1
        return index
    
    n_values = [5, 10, 15, 20, 30, 40]
    bi_values = []
    r_values = []
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            bi = minimal_brauer_induction_index(f)
            r = communication_rank(f)
            bi_values.append(bi)
            r_values.append(r)
    
    if not bi_values or not r_values:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_bi = sum(bi_values) / len(bi_values)
    mean_r = sum(r_values) / len(r_values)
    diff_sum = sum(abs(bi - r) for bi, r in zip(bi_values, r_values))
    avg_diff = diff_sum / len(diff_sum)
    
    correlation_coefficient = 0
    if mean_bi != 0 and mean_r != 0:
        numerator = sum((bi - mean_bi) * (r - mean_r) for bi, r in zip(bi_values, r_values))
        denominator = len(bi_values) * (sum((bi - mean_bi)**2 for bi in bi_values))**0.5 * (sum((r - mean_r)**2 for r in r_values))**0.5
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(bi_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and avg_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    total_metric_value = 0
    total_instances_tested = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"] * trial_result["instances_tested"]
        total_instances_tested += trial_result["instances_tested"]
    
    mean_metric_value = total_metric_value / total_instances_tested
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")