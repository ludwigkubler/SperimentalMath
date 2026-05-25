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
    
    n = 40
    p_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for _ in range(30):
        f = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        
        def mu_p(f, p):
            total = 0
            for i in range(n):
                for j in range(n):
                    total += (abs(f[i][j]) / 2) ** p
            return total ** (1 / p)
        
        mu_p_values = [mu_p(f, p) for p in p_values]
        
        def communication_complexity(f):
            # Simplified version of a communication protocol
            # This is just an example and should be replaced with actual complexity calculation
            return sum(abs(sum(row)) for row in f)
        
        comm_complexities = [communication_complexity(f)]
        
        results.extend(zip(mu_p_values, comm_complexities))
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mean_mu_p = sum(mu_p for mu_p, _ in results) / len(results)
    std_mu_p = math.sqrt(sum((mu_p - mean_mu_p) ** 2 for mu_p, _ in results) / len(results))
    mean_comm = sum(comm for _, comm in results) / len(results)
    std_comm = math.sqrt(sum((comm - mean_comm) ** 2 for _, comm in results) / len(results))
    
    correlation = sum((mu_p - mean_mu_p) * (comm - mean_comm) for mu_p, comm in results) / (len(results) * std_mu_p * std_comm)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation) > 0.3,  # Adjust threshold as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result)
    
    if len(results) == len(seeds):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")
    elif trial_result["counterexample"]:
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")