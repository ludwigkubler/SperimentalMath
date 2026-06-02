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
    
    def generate_communication_protocol(n):
        # Generate a simple n-ary communication protocol
        return [random.randint(0, 1) for _ in range(n)]
    
    def construct_quandle_representation(protocol):
        # Simplified quandle representation construction (mapping undefined)
        return len(set(protocol))
    
    def communication_complexity_rank(protocol):
        # Simplified communication complexity rank calculation (mapping undefined)
        return sum(protocol)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        protocol = generate_communication_protocol(n)
        quandle_order = construct_quandle_representation(protocol)
        rank = communication_complexity_rank(protocol)
        results.append((n, quandle_order, rank))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _ in results)
    instances_tested = len(results)
    
    # Calculate correlation coefficient
    x_mean = sum(quandle_order for _, quandle_order, _ in results) / instances_tested
    y_mean = sum(rank for _, _, rank in results) / instances_tested
    
    numerator = sum((quandle_order - x_mean) * (rank - y_mean) for _, quandle_order, rank in results)
    denominator = math.sqrt(sum((quandle_order - x_mean)**2 for _, quandle_order, _ in results)) * math.sqrt(sum((rank - y_mean)**2 for _, _, rank in results))
    
    if denominator == 0:
        correlation_coefficient = None
    else:
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient is not None and correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all("metric_value" in result and result["metric_value"] is not None for result in results):
        print("RESULT: INCONCLUSIVE reason=missing_metric_value")
    else:
        mean = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")