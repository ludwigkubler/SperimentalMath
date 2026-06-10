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
        rank = sum(1 for i in range(2**n) if f[i] == 1)
        return (rank / (2**n)) * ((2**n - rank) / (2**n))
    
    def twisted_tensor_product_rank(f):
        n = len(f)
        rank = sum(1 for i in range(2**n) if f[i] == 1)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        R_tw = twisted_tensor_product_rank(f)
        R_var = communication_complexity_rank_variance(f)
        results.append((R_tw, R_var))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    R_tw_list = [r[0] for r in results]
    R_var_list = [r[1] for r in results]
    
    mean_R_tw = sum(R_tw_list) / len(R_tw_list)
    mean_R_var = sum(R_var_list) / len(R_var_list)
    
    correlation_coefficient = 0
    for i in range(len(results)):
        correlation_coefficient += (R_tw_list[i] - mean_R_tw) * (R_var_list[i] - mean_R_var)
    correlation_coefficient /= math.sqrt(sum((x - mean_R_tw)**2 for x in R_tw_list)) * math.sqrt(sum((y - mean_R_var)**2 for y in R_var_list))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(cc >= 0.5 for cc in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and min(r["metric_value"] for r in results if r["metric_value"] is not None) < 0.5:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")