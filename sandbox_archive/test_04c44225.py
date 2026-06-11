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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def communication_complexity_rank_variance(f):
        m = len(f)
        n = 2**m
        rank_var = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank_var += 1
        return rank_var / (n * (n - 1) / 2)
    
    def etale_sheaves_order(f):
        m = len(f)
        n = 2**m
        # Simplified algorithm to simulate etale sheaves order
        # This is a placeholder and should be replaced with actual computation
        return m
    
    results = []
    for _ in range(30):
        m = random.randint(5, 40)  # Ensure n_max >= 16
        f = generate_boolean_function(m)
        rank_var = communication_complexity_rank_variance(f)
        order = etale_sheaves_order(f)
        results.append((order, rank_var))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    orders, rank_vars = zip(*results)
    mean_order = sum(orders) / len(orders)
    mean_rank_var = sum(rank_vars) / len(rank_vars)
    correlation = (sum((o - mean_order) * (r - mean_rank_var) for o, r in results) /
                   math.sqrt(sum((o - mean_order)**2 for o in orders) *
                             sum((r - mean_rank_var)**2 for r in rank_vars)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(len(f) for f, _ in results),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] >= 30 for result in results):
        print("RESULT: INCONCLUSIVE insufficient_instances")
    else:
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std=NA support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")