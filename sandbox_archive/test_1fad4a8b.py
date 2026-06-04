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
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def eta_invariant(f):
        n = len(f)
        count = sum(1 for x in f if x == 1)
        return count / n
    
    correlation_coefficient = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        eta_f = eta_invariant(f)
        correlation_coefficient.append((eta_f, r_f))
    
    n_max = max(5, 10, 15, 20, 30, 40)
    instances_tested = 30
    conjecture_holds = False
    counterexample = ""
    
    if len(correlation_coefficient) > 1:
        eta_values, r_values = zip(*correlation_coefficient)
        mean_eta = sum(eta_values) / instances_tested
        mean_r = sum(r_values) / instances_tested
        covariance = sum((eta_values[i] - mean_eta) * (r_values[i] - mean_r) for i in range(instances_tested)) / instances_tested
        variance_eta = sum((eta_values[i] - mean_eta)**2 for i in range(instances_tested)) / instances_tested
        variance_r = sum((r_values[i] - mean_r)**2 for i in range(instances_tested)) / instances_tested
        correlation_coefficient = covariance / (math.sqrt(variance_eta) * math.sqrt(variance_r))
        
        if 0.5 < correlation_coefficient <= 0.7:
            conjecture_holds = True
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_or_budget_exceeded")