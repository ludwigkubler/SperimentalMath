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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_communication = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    max_communication += 1
        return max_communication
    
    def algebraic_k_group_rank(f):
        n = int(math.log2(len(f)))
        k_group_rank = 0
        for i in range(2**n):
            if sum(f[j] for j in range(i, 2**n, 2)) == len([j for j in range(i, 2**n, 2) if f[j]]):
                k_group_rank += 1
        return k_group_rank
    
    def log_growth_rate(rank):
        if rank == 0:
            return 0
        return math.log(rank)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            communication_rank = communication_complexity(f)
            k_group_rank = algebraic_k_group_rank(f)
            log_growth = log_growth_rate(k_group_rank)
            
            if communication_rank == 0 or k_group_rank == 0:
                continue
            
            results.append({
                "n": n,
                "communication_rank": communication_rank,
                "k_group_rank": k_group_rank,
                "log_growth": log_growth
            })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_results"
        }
    
    communication_ranks = [r["communication_rank"] for r in results]
    log_growth_rates = [r["log_growth"] for r in results]
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    
    if n_max < 16:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    mean_communication = sum(communication_ranks) / len(communication_ranks)
    mean_log_growth = sum(log_growth_rates) / len(log_growth_rates)
    
    covariance = sum((c - mean_communication) * (lg - mean_log_growth) for c, lg in zip(communication_ranks, log_growth_rates)) / len(communication_ranks)
    variance_communication = sum((c - mean_communication)**2 for c in communication_ranks) / len(communication_ranks)
    variance_log_growth = sum((lg - mean_log_growth)**2 for lg in log_growth_rates) / len(log_growth_rates)
    
    correlation_coefficient = covariance / math.sqrt(variance_communication * variance_log_growth)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_results")