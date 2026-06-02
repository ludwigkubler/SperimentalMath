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
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        # Generate a random communication complexity problem instance
        φ = ''.join(random.choice('01') for _ in range(n))
        
        # Compute the minimal order of noncrossing partitions (Order(n, φ))
        def is_noncrossing_partition(partition):
            for i in range(len(partition)):
                for j in range(i + 2, len(partition) + 1):
                    if any(partition[k] < partition[i] and partition[k] >= partition[j] for k in range(i + 1, j)):
                        return False
            return True
        
        def find_minimal_order(φ):
            n = len(φ)
            min_order = float('inf')
            
            for i in range(n):
                for j in range(i + 1, n + 1):
                    partition = [i] * (j - i) + [j]
                    if is_noncrossing_partition(partition):
                        min_order = min(min_order, len(partition))
            
            return min_order
        
        Order_n_phi = find_minimal_order(φ)
        
        # Calculate the communication complexity rank (Rank(φ))
        def calculate_rank(φ):
            rank = 0
            for i in range(n):
                if φ[i] == '1':
                    rank += 1
            return rank
        
        Rank_phi = calculate_rank(φ)
        
        results.append({
            "n": n,
            "Order_n_phi": Order_n_phi,
            "Rank_phi": Rank_phi
        })
    
    # Compute the correlation coefficient
    if len(results) < 2:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    n_values = [r["n"] for r in results]
    Order_n_phi_values = [r["Order_n_phi"] for r in results]
    Rank_phi_values = [r["Rank_phi"] for r in results]
    
    mean_Order_n_phi = sum(Order_n_phi_values) / len(Order_n_phi_values)
    mean_Rank_phi = sum(Rank_phi_values) / len(Rank_phi_values)
    
    covariance = sum((Order_n_phi_values[i] - mean_Order_n_phi) * (Rank_phi_values[i] - mean_Rank_phi) for i in range(len(results))) / len(results)
    variance_Order_n_phi = sum((Order_n_phi_values[i] - mean_Order_n_phi) ** 2 for i in range(len(results))) / len(results)
    variance_Rank_phi = sum((Rank_phi_values[i] - mean_Rank_phi) ** 2 for i in range(len(results))) / len(results)
    
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
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")