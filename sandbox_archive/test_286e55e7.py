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
        # Generate a random n-bit communication protocol
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def p_adic_l_function_order(f):
        # Placeholder function to compute the order of the p-adic L-function
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)
    
    def communication_complexity_rank(protocol):
        # Placeholder function to compute the communication complexity rank
        # This is a dummy implementation and should be replaced with actual computation
        return len(protocol)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        protocol = communication_protocol(n)
        f = protocol
        order = p_adic_l_function_order(f)
        c_n = communication_complexity_rank(protocol)
        
        if order < alpha(c_n) / 2:
            return {
                "metric_name": "alpha_c_n",
                "metric_value": None,
                "instances_tested": len(results),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "p-adic L-function order less than alpha(c(n))/2"
            }
        
        results.append({
            "n": n,
            "order": order,
            "c_n": c_n
        })
    
    if len(results) < 30:
        return {
            "metric_name": "alpha_c_n",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    alpha_values = [result["order"] for result in results]
    c_n_values = [result["c_n"] for result in results]
    
    mean_alpha = sum(alpha_values) / len(alpha_values)
    std_alpha = math.sqrt(sum((x - mean_alpha)**2 for x in alpha_values) / len(alpha_values))
    correlation_coefficient = sum((alpha_values[i] - mean_alpha) * (math.log(result["c_n"], 10) - math.log(results[0]["c_n"], 10)) for i, result in enumerate(results)) / (len(alpha_values) * std_alpha * math.sqrt(sum((math.log(result["c_n"], 10) - math.log(results[0]["c_n"], 10))**2 for result in results)))
    
    return {
        "metric_name": "alpha_c_n",
        "metric_value": correlation_coefficient,
        "instances_tested": len(alpha_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len([result for result in results if result["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None)) / len([result for result in results if result["metric_value"] is not None])
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")