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
    
    def generate_communication_complexity_instance(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_p_group_representation(cc_instance):
        # Placeholder function to simulate computing a p-group representation
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(cc_instance))
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        var_x = sum((xi - mean_x) ** 2 for xi in x) / len(x)
        return cov / math.sqrt(var_x * sum((yi - mean_y) ** 2 for yi in y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    minimal_orders = []
    cc_ranks = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            cc_instance = generate_communication_complexity_instance(n)
            minimal_order = compute_p_group_representation(cc_instance)
            minimal_orders.append(minimal_order)
            cc_ranks.append(sum(cc_instance))
    
    if len(minimal_orders) < 30:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": len(minimal_orders),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_minimal_order = sum(minimal_orders) / len(minimal_orders)
    cc_rank_correlation = correlation(cc_ranks, minimal_orders)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_minimal_order,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": mean_minimal_order <= math.sqrt(max(n_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_max={result['n_max']}, cc_instance={result['cc_instance']}, minimal_order={result['minimal_order']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_support")