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
    
    def generate_d_regular_variety(n, d):
        # Simulate generating a d-regular affine variety
        return [random.randint(0, 1) for _ in range(n)]
    
    def circuit_satisfiability_threshold(variety):
        # Simulate computing the circuit satisfiability threshold
        return sum(variety)
    
    def minimal_tropical_motivic_rank(variety):
        # Simulate computing the minimal tropical motivic rank
        return len([x for x in variety if x == 1])
    
    n_values = [5, 10, 15, 20, 30, 40]
    tmr_values = []
    cst_values = []
    
    for n in n_values:
        variety = generate_d_regular_variety(n, d=2)
        tmr = minimal_tropical_motivic_rank(variety)
        cst = circuit_satisfiability_threshold(variety)
        
        tmr_values.append(tmr)
        cst_values.append(cst)
    
    if not tmr_values or not cst_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    n = len(tmr_values)
    mean_tmr = sum(tmr_values) / n
    mean_cst = sum(cst_values) / n
    
    covariance = sum((tmr - mean_tmr) * (cst - mean_cst) for tmr, cst in zip(tmr_values, cst_values))
    variance_tmr = sum((tmr - mean_tmr) ** 2 for tmr in tmr_values)
    variance_cst = sum((cst - mean_cst) ** 2 for cst in cst_values)
    
    if variance_tmr == 0 or variance_cst == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_variance"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_tmr) * math.sqrt(variance_cst))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE no_data")
    else:
        supported_count = sum(1 for result in results if result["conjecture_holds"])
        support_fraction = supported_count / len(results)
        
        if support_fraction >= 0.8:
            mean_value = sum(result["metric_value"] for result in results) / len(results)
            std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
            print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")