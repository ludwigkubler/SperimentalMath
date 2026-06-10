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
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank_var = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank_var += 1
        return rank_var / (n * (n - 1) / 2)
    
    def twisted_tensor_product_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        R_tw = twisted_tensor_product_rank(f)
        R_var = communication_complexity_rank_variance(f)
        results.append((R_tw, R_var))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    R_tw_values, R_var_values = zip(*results)
    correlation_coefficient = sum((R_tw - mean(R_tw_values)) * (R_var - mean(R_var_values)) for R_tw, R_var in results) / (len(results) * std(R_tw_values) * std(R_var_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(f) for f, _ in results),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.8,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.8 else str(correlation_coefficient)
    }

def mean(values):
    return sum(values) / len(values)

def std(values):
    avg = mean(values)
    return math.sqrt(sum((x - avg) ** 2 for x in values) / len(values))

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_value = std([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] < 0.8) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample={r['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")