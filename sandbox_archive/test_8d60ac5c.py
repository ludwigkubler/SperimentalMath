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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if all(f[i*2+j] == f[j*2+i] for j in range(2**(n-i-1))):
                    rank += 1
        return rank
    
    def lie_algebra_simple_ideals(f):
        n = int(math.log2(len(f)))
        ideals = []
        for i in range(n+1):
            ideal = [f[j] for j in range(2**n) if (j & ((1 << i) - 1)) == 0]
            ideals.append(ideal)
        return ideals
    
    def coadjointness_index(ideals):
        n = len(ideals[0])
        index = 0
        for ideal in ideals:
            for j in range(n):
                if all(ideal[j] == ideal[(j + k) % n] for k in range(n)):
                    index += 1
        return index
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        ideals = lie_algebra_simple_ideals(f)
        index = coadjointness_index(ideals)
        results.append((r_f, index))
    
    if len(results) < 30:
        return {
            "metric_name": "coadjointness_index",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    r_f_values, index_values = zip(*results)
    correlation = pearson_correlation(r_f_values, index_values)
    
    return {
        "metric_name": "coadjointness_index",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    conjecture_holds = all(r["conjecture_holds"] for r in results if r["metric_value"] is not None)
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")