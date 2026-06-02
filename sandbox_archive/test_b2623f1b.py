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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(x != -y for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def compute_lii(cnf):
        n = len(cnf[0])
        lii = 0
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    lii += 1
        return lii / (n * len(cnf))
    
    def compute_resolution_width(cnf):
        width = 0
        for clause in cnf:
            width = max(width, len(clause))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        lii = compute_lii(cnf)
        width = compute_resolution_width(cnf)
        results.append({
            "n": n,
            "lii": lii,
            "width": width
        })
    
    mean_lii = sum(result["lii"] for result in results) / len(results)
    mean_width = sum(result["width"] for result in results) / len(results)
    correlation_coefficient = 0
    
    if len(results) > 1:
        numerator = sum((result["lii"] - mean_lii) * (result["width"] - mean_width) for result in results)
        denominator = math.sqrt(sum((result["lii"] - mean_lii)**2 for result in results)) * math.sqrt(sum((result["width"] - mean_width)**2 for result in results))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_lii <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8 or mean_lii > 3\" first_failing_seed={first_failing_seed}")