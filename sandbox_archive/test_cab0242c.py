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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def communication_complexity(f):
        m = len(f)
        n = 2**m
        total_cost = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    total_cost += 1
        return total_cost
    
    def luroth_normal_form_degree(f):
        m = len(f)
        degree = 0
        for i in range(m):
            degree += sum(1 for x in f if x == i)
        return degree
    
    n_tests = 30
    instances_tested = 0
    total_lnd = 0
    total_r = 0
    
    for _ in range(n_tests):
        m = random.randint(5, 40)
        f = generate_boolean_function(m)
        
        lnd = luroth_normal_form_degree(f)
        r = communication_complexity(f)
        
        if lnd is not None and r is not None:
            total_lnd += lnd
            total_r += r
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_lnd = total_lnd / instances_tested
    mean_r = total_r / instances_tested
    
    # Calculate Pearson correlation coefficient
    numerator = sum((x - mean_lnd) * (y - mean_r) for x, y in zip(lnd_values, r_values))
    denominator = math.sqrt(sum((x - mean_lnd)**2 for x in lnd_values)) * math.sqrt(sum((y - mean_r)**2 for y in r_values))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    
    pearson_corr = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": pearson_corr >= 0.8 and all(corr >= 0.5 for corr in [pearson_corr]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")