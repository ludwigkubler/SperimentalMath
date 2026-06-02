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
    
    def generate_communication_instance(n):
        # Generate a random communication instance with n bits
        return [random.choice([0, 1]) for _ in range(n)]
    
    def noncrossing_partitions(instance):
        n = len(instance)
        if n == 0:
            return 1
        count = 0
        for i in range(1, n):
            count += noncrossing_partitions(instance[:i]) * noncrossing_partitions(instance[i:])
        return count
    
    def communication_complexity_rank(instance):
        # Placeholder function to calculate the rank of a communication instance
        # This is a dummy implementation and should be replaced with an actual solver
        return len(set(instance))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_communication_instance(n)
        Order_n_phi = noncrossing_partitions(instance)
        Rank_phi = communication_complexity_rank(instance)
        
        if Order_n_phi == 0 or Rank_phi == 0:
            continue
        
        results.append({
            "n": n,
            "Order_n_phi": Order_n_phi,
            "Rank_phi": Rank_phi
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    Order_n_phi_values = [r["Order_n_phi"] for r in results]
    Rank_phi_values = [r["Rank_phi"] for r in results]
    
    mean_Order_n_phi = sum(Order_n_phi_values) / len(Order_n_phi_values)
    mean_Rank_phi = sum(Rank_phi_values) / len(Rank_phi_values)
    
    covariance = sum((Order_n_phi_values[i] - mean_Order_n_phi) * (Rank_phi_values[i] - mean_Rank_phi) for i in range(len(results)))
    variance_Order_n_phi = sum((Order_n_phi_values[i] - mean_Order_n_phi) ** 2 for i in range(len(results))) / len(Order_n_phi_values)
    variance_Rank_phi = sum((Rank_phi_values[i] - mean_Rank_phi) ** 2 for i in range(len(Rank_phi_values))) / len(Rank_phi_values)
    
    if variance_Order_n_phi == 0 or variance_Rank_phi == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_Order_n_phi) * math.sqrt(variance_Rank_phi))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
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
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_instances")