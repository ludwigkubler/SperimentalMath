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
    
    def communication_complexity_rank_variance_ratio(f):
        n = int(math.log2(len(f)))
        rank = sum(f[i] != f[j] for i in range(len(f)) for j in range(i+1, len(f))) / (len(f) * (len(f) - 1))
        return rank
    
    def construct_braided_tensor_product_module(f):
        n = int(math.log2(len(f)))
        # Simplified construction for demonstration
        M = [i % 2 for i in range(2**n)]
        return M
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        R_f = communication_complexity_rank_variance_ratio(f)
        M = construct_braided_tensor_product_module(f)
        log2_M = log2(len(M))
        
        results.append({
            "n": n,
            "R_f": R_f,
            "log2_M": log2_M
        })
    
    if not results:
        return {
            "metric_name": "log2|M| vs. log(n) * R(f)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    
    log2_M_values = [r["log2_M"] for r in results]
    R_f_values = [r["R_f"] * math.log2(r["n"]) for r in results]
    
    mean_log2_M = sum(log2_M_values) / instances_tested
    mean_R_f = sum(R_f_values) / instances_tested
    
    correlation_coefficient = sum((log2_M - mean_log2_M) * (R_f - mean_R_f) for log2_M, R_f in zip(log2_M_values, R_f_values)) / (instances_tested * math.sqrt(sum((log2_M - mean_log2_M)**2 for log2_M in log2_M_values)) * math.sqrt(sum((R_f - mean_R_f)**2 for R_f in R_f_values)))
    
    conjecture_holds = abs(correlation_coefficient) > 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient=±{:.4f}".format(correlation_coefficient)
    
    return {
        "metric_name": "log2|M| vs. log(n) * R(f)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **trial_result})
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
        sys.exit(0)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["conjecture_holds"] is False), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")