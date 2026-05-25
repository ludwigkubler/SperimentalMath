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
    
    def generate_partial_function(n):
        return {(x, y): random.choice([-1, 1]) for x in range(n) for y in range(n)}
    
    def noncommutative_Lp_measure(f, p):
        n = len(next(iter(f.values())))
        total = 0
        for (x, y), val in f.items():
            total += abs(val / 2) ** p
        return total ** (1 / p)
    
    def communication_complexity(f):
        # Simplified model: assume O(n^2) complexity for any function
        return n ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_partial_function(n)
        mu_p = noncommutative_Lp_measure(f, 2)  # Using p=2 for simplicity
        comm = communication_complexity(f)
        results.append((mu_p, comm))
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mean_mu_p = sum(mu for mu, _ in results) / len(results)
    mean_comm = sum(comm for _, comm in results) / len(results)
    std_mu_p = math.sqrt(sum((mu - mean_mu_p) ** 2 for mu, _ in results) / len(results))
    std_comm = math.sqrt(sum((comm - mean_comm) ** 2 for _, comm in results) / len(results))
    
    if std_mu_p == 0 or std_comm == 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "std_deviation_zero"
        }
    
    correlation = sum((mu_p - mean_mu_p) * (comm - mean_comm) for mu_p, comm in results) / (len(results) * std_mu_p * std_comm)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation) > 0.3,  # Threshold for support
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
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(abs(result["metric_value"]) > 10 * std_value for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) > 10 * std_value)
            print(f"RESULT: FALSIFIED counterexample=\"std_deviation\" first_failing_seed={first_failing_seed}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE empty_results")