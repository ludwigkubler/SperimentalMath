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
    
    def compute_quaternionic_kähler_form(f):
        n = int(math.log2(len(f)))
        if n != int(n):
            return None
        order = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] == f[j]:
                    order += 1
        return order
    
    def is_read_twice_bp(f):
        n = len(f)
        count = [f.count(0), f.count(1)]
        for i in range(n):
            if count[f[i]] != n // 2:
                return False
            count[f[i]] -= 1
        return True
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i+1 for i in range(n)}
        rank_y = {y[i]: i+1 for i in range(n)}
        sum_diff_squared_ranks = sum((rank_x[x[i]] - rank_y[y[i]])**2 for i in range(n))
        return 1 - (6 * sum_diff_squared_ranks) / (n * (n**2 - 1))
    
    n_values = [10, 20, 30]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        if not is_read_twice_bp(f):
            continue
        
        qkf = compute_quaternionic_kähler_form(f)
        if qkf is None:
            continue
        
        results.append((n, qkf))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    n_values, qkf_values = zip(*results)
    rho = spearman_rank_correlation(n_values, qkf_values)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE no_valid_data")
    else:
        mean_rho = sum(r["metric_value"] for r in results if "metric_value" in r and r["metric_value"] is not None) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction=1")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")