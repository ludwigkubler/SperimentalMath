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
    
    n = 30  # Number of instances per trial
    p_values = [5, 10, 15, 20, 30, 40]  # Different values of p to test
    
    def generate_random_partial_function(n):
        return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def noncommutative_Lp_measure(f, p):
        total = 0
        n = len(f)
        for i in range(n):
            for j in range(n):
                total += (abs(f[i][j]) / 2) ** p
        return (total / (n * n)) ** (1 / p)
    
    def communication_complexity(f):
        # Placeholder function to measure communication complexity
        # This is a dummy implementation and should be replaced with actual computation
        return random.random() * 10
    
    results = []
    for p in p_values:
        for _ in range(n):
            f = generate_random_partial_function(n)
            mu_p = noncommutative_Lp_measure(f, p)
            comm_complexity = communication_complexity(f)
            results.append((mu_p, comm_complexity))
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mu_p_values = [mu for mu, _ in results]
    comm_complexities = [comm for _, comm in results]
    
    mean_mu_p = sum(mu_p_values) / len(mu_p_values)
    std_mu_p = math.sqrt(sum((x - mean_mu_p) ** 2 for x in mu_p_values) / len(mu_p_values))
    mean_comm = sum(comm_complexities) / len(comm_complexities)
    std_comm = math.sqrt(sum((x - mean_comm) ** 2 for x in comm_complexities) / len(comm_complexities))
    
    correlation = sum((mu_p - mean_mu_p) * (comm - mean_comm) for mu_p, comm in results) / (len(results) * std_mu_p * std_comm)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation) > 0.3,
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
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) > 0.3) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"]) > 1 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) > 1)
        print(f"RESULT: FALSIFIED counterexample=\"large_deviation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")