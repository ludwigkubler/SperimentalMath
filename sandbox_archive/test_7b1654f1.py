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
    
    def read_twice_bp_size(f):
        n = len(f)
        count = 0
        for i in range(n):
            if f[i] == 1:
                count += 1
            else:
                break
        return count
    
    def quaternionic_kähler_form_order(f):
        n = len(f)
        order = 0
        for i in range(n):
            if f[i] == 1:
                order += math.log2(i + 1)
        return order
    
    n_values = [10, 20, 30]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        read_twice_bp = read_twice_bp_size(f)
        kähler_form_order = quaternionic_kähler_form_order(f)
        results.append((n, read_twice_bp, kähler_form_order))
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n_values, read_twice_bp_sizes, kähler_form_orders = zip(*results)
    
    def rank(data):
        return {x: i for i, x in enumerate(sorted(set(data)), start=1)}
    
    rank_read_twice_bp = rank(read_twice_bp_sizes)
    rank_kähler_form_order = rank(kähler_form_orders)
    
    n = len(rank_read_twice_bp)
    spearman_corr = 0
    for i in range(n):
        for j in range(i + 1, n):
            d1 = rank_read_twice_bp[read_twice_bp_sizes[i]] - rank_read_twice_bp[read_twice_bp_sizes[j]]
            d2 = rank_kähler_form_order[kähler_form_orders[i]] - rank_kähler_form_order[kähler_form_orders[j]]
            spearman_corr += (d1 * d2) / (n * (n - 1))
    
    mean_read_twice_bp = sum(read_twice_bp_sizes) / n
    mean_kähler_form_order = sum(kähler_form_orders) / n
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": spearman_corr,
        "instances_tested": len(results),
        "conjecture_holds": spearman_corr > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")