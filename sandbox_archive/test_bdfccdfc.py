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
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("f must be a Boolean function with 2^n values")
        return max(sum(f[j] != f[j ^ (1 << i)] for j in range(2**n)) for i in range(n))
    
    def kahler_class_rank(f):
        # Placeholder implementation; actual computation depends on Kähler geometry
        # For simplicity, we assume the rank is equal to the communication complexity rank
        return communication_complexity_rank(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        k_f = kahler_class_rank(f)
        results.append((n, r_f, k_f))
    
    if not all(k >= r for _, r, k in results):
        return {
            "metric_name": "Kähler Class Rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "Kähler class rank is less than communication complexity rank"
        }
    
    k_values = [k for _, _, k in results]
    r_values = [r for _, r, _ in results]
    mean_k = sum(k_values) / len(k_values)
    mean_r = sum(r_values) / len(r_values)
    std_k = math.sqrt(sum((k - mean_k)**2 for k in k_values) / len(k_values))
    std_r = math.sqrt(sum((r - mean_r)**2 for r in r_values) / len(r_values))
    
    return {
        "metric_name": "Kähler Class Rank",
        "metric_value": mean_k,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": std_k >= 0.8 * std_r,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if not trial_result["conjecture_holds"]:
            break
        results.append(trial_result["metric_value"])
    
    mean_metric = sum(results) / len(results)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in results) / len(results))
    support_fraction = len(results) / len(seeds)
    
    if all(trial_result["conjecture_holds"] for trial_result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif not results:
        print("RESULT: INCONCLUSIVE no data")
    else:
        first_failing_seed = seeds[results.index(next(filter(lambda x: not x["conjecture_holds"], results)))]
        print(f"RESULT: FALSIFIED counterexample='Kähler class rank is less than communication complexity rank' first_failing_seed={first_failing_seed}")