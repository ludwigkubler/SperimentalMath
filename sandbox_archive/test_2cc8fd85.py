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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def p_adic_log(x, p):
    if x <= 0:
        return float('inf')
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    protocols = []
    for _ in range(30):
        protocol = [random.randint(1, 2**n) for _ in range(n)]
        protocols.append(protocol)
    
    rank_variances = []
    p_adic_logs = []
    
    for protocol in protocols:
        # Calculate rank variance
        rank_variance = sum(x - (sum(protocol) // n) for x in protocol) ** 2 / n
        rank_variances.append(rank_variance)
        
        # Calculate p-adic logarithmic growth
        p_adic_log_sum = sum(p_adic_log(x, 2) for x in protocol)
        p_adic_logs.append(p_adic_log_sum)
    
    if not rank_variances or not p_adic_logs:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(protocols),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_protocol"
        }
    
    # Calculate correlation coefficient
    mean_rv = sum(rank_variances) / len(rank_variances)
    mean_pal = sum(p_adic_logs) / len(p_adic_logs)
    numerator = sum((rv - mean_rv) * (pal - mean_pal) for rv, pal in zip(rank_variances, p_adic_logs))
    denominator = math.sqrt(sum((rv - mean_rv) ** 2 for rv in rank_variances)) * math.sqrt(sum((pal - mean_pal) ** 2 for pal in p_adic_logs))
    correlation_coefficient = numerator / denominator if denominator != 0 else float('nan')
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(protocols),
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8 and correlation_coefficient <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    metric_mean = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len([result for result in results if result["metric_value"] is not None])
    
    if support_fraction >= 0.8 and all(0 <= x <= 3 for x in [result["metric_value"] for result in results if result["metric_value"] is not None]):
        print(f"RESULT: SUPPORTED mean={metric_mean} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")