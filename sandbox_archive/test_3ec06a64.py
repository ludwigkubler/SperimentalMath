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
    
    def geometric_complexity(f):
        n = int(math.log2(len(f)))
        count = [f.count(i) for i in range(2**n)]
        return sum(count[i] * math.log(count[i], 2) for i in range(2**n))
    
    def communication_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            bits = [f[j] for j in range(2**n) if (j >> i) & 1]
            rank += max(bits.count(0), bits.count(1))
        return rank
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean)**2 for x in lst) / len(lst)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        f = generate_boolean_function(n)
        gc = geometric_complexity(f)
        cr = communication_rank(f)
        results.append((gc, cr))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    gc_values, cr_values = zip(*results)
    mean_gc = sum(gc_values) / len(gc_values)
    mean_cr = sum(cr_values) / len(cr_values)
    cov = sum((gc - mean_gc) * (cr - mean_cr) for gc, cr in results) / len(results)
    var_gc = variance(gc_values)
    
    if var_gc == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_of_gc_is_zero"
        }
    
    pearson_corr = cov / math.sqrt(var_gc * variance(cr_values))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_metric_value = None
        std_metric_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")