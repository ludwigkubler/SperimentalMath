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
    
    def communication_protocol(n):
        # Placeholder for actual protocol generation logic
        return [random.randint(0, 1) for _ in range(n)]
    
    def p_adic_generalized_L_function_order(f):
        # Placeholder for actual L-function order calculation
        return len(f)
    
    def communication_complexity_rank(protocol):
        # Placeholder for actual rank calculation
        return sum(protocol)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        protocol = communication_protocol(n)
        f_n = p_adic_generalized_L_function_order(protocol)
        c_n = communication_complexity_rank(protocol)
        
        if c_n == 0:
            continue
        
        alpha_c_n = math.log(c_n, n)
        results.append({
            "n": n,
            "alpha_c_n": alpha_c_n
        })
    
    if not results:
        return {
            "metric_name": "alpha(c(n))",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid communication protocols generated"
        }
    
    alpha_values = [r["alpha_c_n"] for r in results]
    log_n_values = [math.log(r["n"], r["n"]) for r in results]
    
    correlation_coefficient = sum(a * b for a, b in zip(alpha_values, log_n_values)) / (len(alpha_values) * sum(x**2 for x in alpha_values))
    
    return {
        "metric_name": "alpha(c(n))",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient > 0.7 and all(a >= alpha_c_n / 2 for a, alpha_c_n in zip(alpha_values, log_n_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")