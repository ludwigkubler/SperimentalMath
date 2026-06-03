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
        # Simplified version of communication complexity rank
        return sum(f[i] != f[j] for i in range(len(f)) for j in range(i+1, len(f))) / (len(f) * (len(f) - 1))
    
    def local_indeterminacy(f):
        n = int(math.log2(len(f)))
        # Simplified version of local indeterminacy
        return sum(1 for i in range(n) if f[i] != f[(i + 1) % n]) / n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        il = local_indeterminacy(f)
        results.append((r_f, il))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    r_f_values, il_values = zip(*results)
    mean_r_f = sum(r_f_values) / len(r_f_values)
    mean_il = sum(il_values) / len(il_values)
    covariance = sum((r_f - mean_r_f) * (il - mean_il) for r_f, il in results) / len(results)
    variance_r_f = sum((r_f - mean_r_f)**2 for r_f in r_f_values) / len(r_f_values)
    variance_il = sum((il - mean_il)**2 for il in il_values) / len(il_values)
    
    if variance_r_f == 0 or variance_il == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "Variance of r(f) or IL is zero"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_r_f) * math.sqrt(variance_il))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": pearson_corr > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("metric_value" not in result or math.isnan(result["metric_value"]) for result in results):
        print("RESULT: INCONCLUSIVE No valid metric values found")
    else:
        mean_metric = sum(result["metric_value"] for result in results) / len(results)
        std_metric = math.sqrt(sum((result["metric_value"] - mean_metric)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        elif any("counterexample" in result for result in results):
            counterexample = next(result["counterexample"] for result in results if "counterexample" in result)
            first_failing_seed = next(result["seed"] for result in results if "conjecture_holds" not in result or not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE Not enough support for the conjecture")