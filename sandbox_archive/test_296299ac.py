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
    
    def generate_communication_protocol(n):
        protocol = []
        for _ in range(n):
            protocol.append(random.randint(1, 10))
        return protocol
    
    def communication_complexity_rank(protocol):
        rank = 0
        for i in range(len(protocol)):
            for j in range(i + 1, len(protocol)):
                if protocol[i] != protocol[j]:
                    rank += 1
        return rank
    
    def noncommutative_crossed_product_order(protocol):
        order = sum(1 for x in protocol if x > 5)
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        protocol = generate_communication_protocol(n)
        rank = communication_complexity_rank(protocol)
        order = noncommutative_crossed_product_order(protocol)
        
        results.append({
            "n": n,
            "protocol": protocol,
            "rank": rank,
            "order": order
        })
    
    if len(results) < 30:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    ranks = [result["rank"] for result in results]
    orders = [result["order"] for result in results]
    
    mean_rank = sum(ranks) / len(ranks)
    mean_order = sum(orders) / len(orders)
    
    covariance = sum((r - mean_rank) * (o - mean_order) for r, o in zip(ranks, orders))
    variance_rank = sum((r - mean_rank) ** 2 for r in ranks)
    variance_order = sum((o - mean_order) ** 2 for o in orders)
    
    correlation_coefficient = covariance / math.sqrt(variance_rank * variance_order)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": 0.3 < correlation_coefficient <= 0.7,
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
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_trials_supported")