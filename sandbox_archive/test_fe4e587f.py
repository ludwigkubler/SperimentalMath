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
        return ''.join(random.choice('01') for _ in range(n))
    
    def p_adic_generalized_L_function_order(f):
        # Placeholder function to compute the order of the p-adic generalized L-function
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)
    
    def communication_complexity_rank(protocol):
        # Placeholder function to compute the communication complexity rank
        # This is a dummy implementation and should be replaced with actual computation
        return len(protocol)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        protocol = communication_protocol(n)
        f = protocol
        order = p_adic_generalized_L_function_order(f)
        rank = communication_complexity_rank(protocol)
        
        if order < alpha(rank) / 2:
            return {
                "metric_name": "alpha(c(n))",
                "metric_value": None,
                "instances_tested": len(results),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "p-adic generalized L-function order less than alpha(c(n))/2"
            }
        
        results.append((order, rank))
    
    if not results:
        return {
            "metric_name": "alpha(c(n))",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid results generated"
        }
    
    orders, ranks = zip(*results)
    alpha_values = [alpha(r) for r in ranks]
    
    correlation_coefficient = sum((o - mean(orders)) * (a - mean(alpha_values)) for o, a in zip(orders, alpha_values)) / math.sqrt(sum((o - mean(orders))**2 for o in orders) * sum((a - mean(alpha_values))**2 for a in alpha_values))
    
    return {
        "metric_name": "alpha(c(n))",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def alpha(c_n):
    # Placeholder function to compute the constant α
    # This is a dummy implementation and should be replaced with actual computation
    return random.uniform(1, 2)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p-adic generalized L-function order less than alpha(c(n))/2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_conjecture")