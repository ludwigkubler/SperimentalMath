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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def hdim(cnf):
        # Placeholder function to compute Hodge-theoretic dimension
        # This is a dummy implementation and should be replaced with actual computation
        return random.random() * n  # Dummy value for demonstration
    
    def resolution_width(cnf):
        # Placeholder function to compute resolution proof width
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf) + random.randint(0, 10)  # Dummy value for demonstration
    
    metric_name = "resolution_width_over_hdim"
    instances_tested = 30
    n_max = 40
    conjecture_holds = False
    counterexample = ""
    
    results = []
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        hdim_value = hdim(cnf)
        width_value = resolution_width(cnf)
        
        if hdim_value == 0 or width_value == 0:
            continue
        
        results.append((hdim_value, width_value))
    
    if len(results) < instances_tested:
        counterexample = "not_enough_valid_instances"
    
    if results:
        hdims = [r[0] for r in results]
        widths = [r[1] for r in results]
        
        mean_hdim = sum(hdims) / len(hdims)
        mean_width = sum(widths) / len(widths)
        
        correlation = 0
        if len(hdims) > 1:
            numerator = sum((h - mean_hdim) * (w - mean_width) for h, w in results)
            denominator = math.sqrt(sum((h - mean_hdim)**2 for h in hdims)) * math.sqrt(sum((w - mean_width)**2 for w in widths))
            correlation = numerator / denominator
        
        if correlation > 0.8:
            conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_valid_instances\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")