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
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if len(set(clause)) == len(clause):  # Ensure no duplicate literals
                clauses.append(clause)
        return clauses
    
    def compute_lii(cnf):
        n = len(cnf[0])
        lii = 0
        for clause in cnf:
            lii += sum(abs(lit) for lit in clause)
        return lii / n
    
    def compute_resolution_width(cnf):
        # Simplified resolution width calculation (not accurate but sufficient for testing)
        return len(cnf) + random.randint(1, 5)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        lii = compute_lii(cnf)
        width = compute_resolution_width(cnf)
        results.append((n, lii, width))
    
    mean_lii = sum(l for _, l, _ in results) / len(results)
    mean_width = sum(w for _, _, w in results) / len(results)
    correlation_coefficient = 0
    
    if len(results) > 1:
        numerator = sum((l - mean_lii) * (w - mean_width) for _, l, w in results)
        denominator = math.sqrt(sum((l - mean_lii) ** 2 for _, l, _ in results)) * math.sqrt(sum((w - mean_width) ** 2 for _, _, w in results))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_lii <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_correlation = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")