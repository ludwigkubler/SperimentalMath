# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from math import log2, ceil
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_communication_protocol(n):
        # Generate a random communication protocol with n elements
        return [random.randint(1, 100) for _ in range(n)]
    
    def calculate_rank_variance(protocol):
        # Calculate the rank variance of the protocol
        mean = sum(protocol) / len(protocol)
        variance = sum((x - mean) ** 2 for x in protocol) / len(protocol)
        return variance
    
    def calculate_median_rank(protocol):
        # Calculate the median rank of the protocol
        sorted_protocol = sorted(protocol)
        n = len(sorted_protocol)
        if n % 2 == 1:
            return sorted_protocol[n // 2]
        else:
            return (sorted_protocol[n // 2 - 1] + sorted_protocol[n // 2]) / 2
    
    def calculate_local_coherence_index(protocol):
        # Calculate the local coherence index of the protocol
        n = len(protocol)
        if n == 0:
            return 0
        max_value = max(protocol)
        min_value = min(protocol)
        return (max_value - min_value) / (n * (n - 1))
    
    def calculate_ratio(V, R):
        # Calculate the ratio of median rank to average rank
        if R == 0:
            return float('inf')
        return V / R
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        protocol = generate_communication_protocol(n)
        V = calculate_rank_variance(protocol)
        R = calculate_median_rank(protocol)
        I = calculate_local_coherence_index(protocol)
        ratio = calculate_ratio(V, R)
        
        if R == 0:
            continue
        
        results.append((I, ratio))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_data"
        }
    
    n = len(results)
    mean_I = sum(I for I, _ in results) / n
    mean_ratio = sum(ratio for _, ratio in results) / n
    
    # Perform linear regression to determine correlation
    numerator = sum((I - mean_I) * (ratio - mean_ratio) for I, ratio in results)
    denominator = sum((I - mean_I) ** 2 for I, _ in results)
    
    if denominator == 0:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    
    correlation = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) > 0.95,  # Threshold for significance
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(result)]}")