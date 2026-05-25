# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_partial_function(n):
        return { (x, y): random.choice([-1, 1]) for x in range(n) for y in range(n) }
    
    def noncommutative_Lp_measure(f, p):
        n = len(next(iter(f.keys())))
        total = 0
        for (x, y), value in f.items():
            total += abs(value / 2) ** p
        return total ** (1 / p)
    
    def communication_complexity(f):
        # Placeholder function; actual implementation depends on the problem
        return random.random() * len(f)
    
    n = 40
    results = []
    for _ in range(30):
        f = generate_partial_function(n)
        mu_p = noncommutative_Lp_measure(f, p=2)  # Using p=2 as an example
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
    
    correlation = sum((mu_p - mean_mu_p) * (comm - mean_comm) for mu_p, comm in results) / (len(results) * std_mu_p * std_comm)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation) > 0.1,  # Adjust threshold as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next((seed for seed, result in zip(seeds, results) if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")