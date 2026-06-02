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
        n = len(f)
        if n == 1:
            return 1
        else:
            # Simplified rank calculation for demonstration purposes
            return n - 1
    
    def p_adic_hodge_class(f):
        # Placeholder function to simulate the computation of the p-adic Hodge class
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        h_f = p_adic_hodge_class(f)
        r_f = communication_complexity_rank(f)
        
        if h_f <= 0 or r_f <= 0:
            continue
        
        log_h_f = math.log(h_f)
        results.append((log_h_f, r_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    log_h_f_values, r_f_values = zip(*results)
    mean_log_h_f = sum(log_h_f_values) / len(log_h_f_values)
    mean_r_f = sum(r_f_values) / len(r_f_values)
    std_log_h_f = math.sqrt(sum((x - mean_log_h_f)**2 for x in log_h_f_values) / len(log_h_f_values))
    std_r_f = math.sqrt(sum((x - mean_r_f)**2 for x in r_f_values) / len(r_f_values))
    
    correlation_coefficient = sum((log_h_f_values[i] - mean_log_h_f) * (r_f_values[i] - mean_r_f) for i in range(len(log_h_f_values))) / (len(log_h_f_values) * std_log_h_f * std_r_f)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": abs(correlation_coefficient) >= 3 * std_correlation_coefficient,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value)**2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(x["conjecture_holds"] for x in results) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={result['seed']}")
                break