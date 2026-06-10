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
    
    def compute_rank(f):
        n = len(f)
        matrix = [[f[i ^ j] for j in range(2**n)] for i in range(2**n)]
        rank = 0
        for row in matrix:
            if any(row[j] != 0 for j in range(rank, 2**n)):
                rank += 1
        return rank
    
    def compute_communication_complexity_rank_variance(f):
        n = len(f)
        matrix = [[f[i ^ j] for j in range(2**n)] for i in range(2**n)]
        variance = 0
        for row in matrix:
            variance += sum(row[j]**2 for j in range(2**n))
        return variance / (2**(2*n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        R_tw = compute_rank(f)
        R_var = compute_communication_complexity_rank_variance(f)
        results.append((n, R_tw, R_var))
    
    correlation_coefficient = sum((R_tw - mean_R_tw) * (R_var - mean_R_var) for n, R_tw, R_var in results) / len(results)
    mean_R_tw = sum(R_tw for n, R_tw, R_var in results) / len(results)
    mean_R_var = sum(R_var for n, R_tw, R_var in results) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.8,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.8 else "correlation_coefficient_outside_range"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(0.5 <= r["metric_value"] < 0.8 for r in results) / len(results)
    
    if all(0.5 <= r["metric_value"] < 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif any(r["counterexample"] == "correlation_coefficient_outside_range" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "correlation_coefficient_outside_range")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")